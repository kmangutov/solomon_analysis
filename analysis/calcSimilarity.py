# -*- coding: utf-8 -*-

from pattern.vector import Document, Vector, distance, normalize
from dataInterface import loadJSON, loadJSONs, loadData
import json
from pprint import pprint
import os
import conditions
import sys
from pprint import pprint
from formatting.csvUtil import CSVFile
import itertools



def printElapsedStats(array, title=""):
  sumElapsed = 0.0
  for value in array:
    sumElapsed += float(value)

  meanElapsedTime = sumElapsed / len(array)

  sumElapsedDev = 0
  for value in array:
    sumElapsedDev += (float(value) - meanElapsedTime)**2

  variance = sumElapsedDev / len(array)
  std = variance**0.5

  pprint(title + " Mean: " + str(meanElapsedTime) + " StdDev: " + str(std))

def mapMapSet(hashmap, key1, key2, value):
  hashmap[key1][key2] = value

def mapArrayAppend(hashmap, key, value):
  if key in hashmap:
    hashmap[key].append(value)
  else:
    hashmap[key] = [value]

def mapArrayAppendKeys(hashmap, keys, value):
  for key in keys:
    mapArrayAppend(hashmap, key, value)

def labelFeedback(history, modality, design=""):
  key = "history" + str(session['history']) + "-modality" + str(session['modality'])
  if len(design) > 0:
   key +="-" + design
  return key

def label(session):
  key = "history" + str(session['history']) + "-modality" + str(session['modality'])
  return key

def labels(session):
  #history = "history" + str(session['history'])
  
  history = "history" if session['history'] else "nohistory"

  modality = str(session['modality']) 
  design = str(session['imgCondition'])

  combs = [
    [history, modality, design],
    [history, modality],
    #[modality, design],
    [history],
    [modality],
    [design]
  ]

  keys = []
  for combo in combs:
    keys.append("-".join(combo))

  return keys

def nonEmpty(session):
  nonEmptyAnnot = session['modality'] == '2d' and len(session['myVals']) > 0
  nonEmptyText = session['modality'] == 'text' and len(session['myVals']['val']) > 0
  return nonEmptyAnnot or nonEmptyText


def mapInc(hashmap, key):
  if not key in hashmap:
    hashmap[key] = 1
  else:
    hashmap[key] = hashmap[key] + 1

def mapIncKeys(hashmap, keys):
  for key in keys:
    mapInc(hashmap, key)


def exportConditions(stat, hashmap, keys):
  print "#################################################"
  csvFile = CSVFile("d3/" + stat)

  header = ""
  for key in keys:
    header += key + ","
  header = header[0:-1]
  csvFile.write(header)

  for i in range(len(hashmap[keys[0]])):
    ret = ""
    for key in keys:
      ret += str(hashmap[key][i]) + ","
    csvFile.write(ret[0:-1])

  csvFile.close()

def exportAnova(stat, hashmap, keyA, keyB):
  print "#################################################"
  csvFile = CSVFile("anova/" + stat)

  for A in keyA:
    for B in keyB:
      key = A + "-" + B
      for i in range(len(hashmap[key])):
        ret = A + "," + B + "," + str(hashmap[key][i])
        csvFile.write(ret)

  csvFile.close()

def exportOneWayAnova(stat, hashmap, keyA, doOutliers=True):
  print "#################################################"
  csvFile = CSVFile("anova/" + stat)

  pprint(keyA)

  lens = {len(hashmap[key]) for key in keyA}
  pprint(lens)
  lensMin = min(lens)

  def outliers(arr):
    arr.sort()
    arrLen = len(arr)
    cutLen = int(round(arrLen * 0.025))
    pprint("cutlen: " + str(cutLen))
    if cutLen == 0:
      return arr
    return arr[cutLen:-cutLen]


  sanitized = {}
  header = ""
  for key in keyA:
    if doOutliers:
      sanitized[key] = outliers(hashmap[key][0:lensMin])
    else:
      sanitized[key] = hashmap[key][0:lensMin]

  pprint(sanitized)

  for A in keyA:
    print "EXPORTONEWAY KEY " + A
    for i in range(len(sanitized[A])):
      ret = A + "," + str(sanitized[A][i])
      csvFile.write(ret)

  csvFile.close()

def similarity(a, b):

  docA = Document(a)
  docB = Document(b)

  vecA = normalize(docA.vector)
  vecB = normalize(docB.vector)

  #print docA.vector
  return 1 - distance(vecA, vecB)




 ###############
 
data = loadData()#loadJSONs(conditions.ALL)#loadJSONs(conditions.TEXT)#loadJSONs(conditions.ALL)
mapSimilarity = {}
simMax = 0
simMin = 1


def avgSimilarity(feedback, feedbacks):
  ret = 0.0
  count = len(feedbacks)
  for item in feedbacks:
    ret += similarity(feedback['text'], item['text'])

  if count == 0:
    return 0

  return ret / count

def avgTextSimilarity(text, texts):
  ret = 0.0
  count = len(texts)
  for item in texts:
    ret += similarity(text, item)

  if count == 0:
    return 0

  return ret / count


for session in data:
  keys = labels(session)

  if nonEmpty(session):
    if session['modality'] == 'text':
      
      #pass
      pprint(session)

      feedbacksOpenedId = []
      feedbacksOpenedVal = []

      feedbacksUnopenedId = []
      feedbacksUnopenedVal = []

      myVal = session['myVals']['val']

      ### aggragate corpuses
      for stackItem in session['stack']:
        stackId = stackItem['id']

        if not stackId in feedbacksOpenedId and not stackId in feedbacksUnopenedId:
          if stackItem['duration'] > 1: #1 sec cutoff
            feedbacksOpenedId.append(stackId)
            feedbacksOpenedVal.append(stackItem['val'])
          else:
            feedbacksUnopenedId.append(stackId)
            feedbacksUnopenedVal.append(stackItem['val'])

      ### calculate similarity
      sim = avgTextSimilarity(myVal, feedbacksOpenedVal)
      unseenSim = avgTextSimilarity(myVal, feedbacksUnopenedVal)


      pprint('TEXT MODALITY SIM: ' + str(sim) + ' UNSIM:' + str(unseenSim))

      if unseenSim == 0 or sim == 0:
        continue

      ### update min max
      if sim > simMax:
        simMax = sim

      if sim < simMin:
        simMin = sim

      if unseenSim > simMax:
        simMax = unseenSim

      if unseenSim < simMin:
        simMin = unseenSim

      mapArrayAppendKeys(mapSimilarity, ['primed-text'], sim);
      mapArrayAppendKeys(mapSimilarity, ['unprimed-text'], unseenSim)


    else:
      feedbacksOpenedId = []
      feedbacksOpenedVal = []

      feedbacksUnopenedId = []
      feedbacksUnopenedVal = []

      ### create feedbacksOpened corpus
      for history in session['stack']:

        #pprint(session);
        #sys.exit(0)

        ### if it's a hover, add it to feedbacksOpenedVal ("corpus")
        if history['action'] == 'hover':

          historyId = history['feedback']['id']
          if not historyId in feedbacksOpenedId:

            #novel hover feedback
            threshold = 1 #seconds

            if float(history['duration']) > threshold:
              feedbacksOpenedId.append(historyId)
              feedbacksOpenedVal.append(history['feedback']);

        ### if it's a write, calculate avg similarity to seen
        if history['action'] == 'write':

          historyId = history['feedback']['id']
          if not historyId in feedbacksOpenedId: #make sure we're not hovering one i made

            if len(feedbacksOpenedVal) == 0:
              continue

            sim = avgSimilarity(history['feedback'], feedbacksOpenedVal)

            ### calculate average similarity of all 'vals' not in feedbacksOpenedId
            unseenCorpus = []
            for oldVal in session['vals']:
              if oldVal['id'] not in feedbacksOpenedId: 
                ### this feedback was not opened
                unseenCorpus.append(oldVal)

            unseenSim = avgSimilarity(history['feedback'], unseenCorpus)




            #if sim == 0:
              #pprint("###SIM IS 0:")
              #pprint(history['feedback'])
              #pprint("OPENED:")
              #pprint(feedbacksOpenedVal)
              #pprint("###")

            if unseenSim == 0 or sim == 0:
              continue

            print 'FOR COMMENT ' + history['feedback']['text']
            print '### OPENED'
            pprint(feedbacksOpenedVal)
            print '### UNOPENED'
            pprint(unseenCorpus)

            print 'PRIMED SIM: ' + str(sim)
            print 'UNPRIMED SIM: ' + str(unseenSim)

            if sim > simMax:
              simMax = sim

            if sim < simMin:
              simMin = sim

            if unseenSim > simMax:
              simMax = unseenSim

            if unseenSim < simMin:
              simMin = unseenSim

            mapArrayAppendKeys(mapSimilarity, ['primed-' + str(session['modality'])], sim);
            mapArrayAppendKeys(mapSimilarity, ['unprimed-' + str(session['modality'])], unseenSim)

      ### create unopened corpus
      #for feedback in session['vals']:

        ### if it's not in OpenedId, put it in UnopenedId
        #feedbackId = feedback['id']
        #if not feedbackId in feedbacksOpenedVal:
        #  feedbacksUnopenedId.append(feedbackId)
        #  feedbacksUnopenedVal.append(feedback)

      ### calc similarity to unopened coprus
      #for feedback in session['myVals']:

        #if len(feedbacksUnopenedVal) == 0:
        #  continue

        #sim = avgSimilarity(feedback, feedbacksUnopenedVal)
        #mapArrayAppendKeys(mapSimilarity, ['unprimed'], sim)

      #pprint(feedbacksOpenedVal)
      #pprint(feedbacksUnopenedVal)

pprint(mapSimilarity)

def outliers(arr):
  arr.sort()
  arrLen = len(arr)
  cutLen = int(round(arrLen * 0.025))
  pprint("cutlen: " + str(cutLen))
  if cutLen == 0:
    return arr
  return arr[cutLen:-cutLen]

def normalize(arr, vMin, vMax):
  ret = []
  for item in arr:
    ret.append((float(item) - vMin) / (vMax - vMin))
  return ret

def normalizeMap(hashmap):
  vals = []
  for v in hashmap.values():
    vals += v

  pprint(vals)

  vMin = min(vals)
  vMax = max(vals)

  #print 'Min ' + vMin + ", Max " + vMax


  for key in hashmap.keys():
    hashmap[key] = normalize(hashmap[key], vMin, vMax)
  return hashmap

lens = {len(mapSimilarity[key]) for key in mapSimilarity.keys()}
minLen = min(lens)
ss = mapSimilarity

###CUT LENGHT TO SAME FOR ALL CONDITIONS
for key in ss.keys():
  ss[key] = ss[key][0:minLen]

###TAKE OUT OUTLIERS
for key in ss.keys():
  ss[key] = outliers(ss[key])

###NORMALIZE
ss = normalizeMap(ss)
#for key in ss.keys():
#  ss[key] = normalize(ss[key], simMin, simMax)


pprint(ss)
exportAnova('similarity.csv', ss, ['primed', 'unprimed'], ['text', '2d']);


keys = ['unprimed-text', 'unprimed-2d', 'primed-text', 'primed-2d']
exportConditions("similarity.csv", ss, keys)


