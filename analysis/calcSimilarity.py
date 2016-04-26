# -*- coding: utf-8 -*-

from pattern.vector import Document, Vector, distance, normalize
from dataInterface import loadJSON, loadJSONs
import json
from pprint import pprint
import os
import conditions
import sys
from pprint import pprint
from formatting.csvUtil import CSVFile



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
  csvFile = CSVFile(stat)

  lens = {len(hashmap[key]) for key in keys}
  print(lens)
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
  for key in keys:
    header += key + ","
    sanitized[key] = outliers(hashmap[key][0:lensMin])

  header = header[0:-1]
  csvFile.write(header)

  for i in range(len(sanitized[keys[0]])):
    ret = ""
    for key in keys:
      ret += str(sanitized[key][i]) + ","
    csvFile.write(ret[0:-1])

  csvFile.close()

def exportAnova(stat, hashmap, keyA, keyB):
  print "#################################################"
  csvFile = CSVFile("anova/" + stat)

  keySets = []
  for A in keyA:
    for B in keyB:
      keySets.append(A + "-" + B)
          
  pprint(keySets)


  lens = {len(hashmap[key]) for key in keySets}
  print(lens)
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
  for key in keySets:
    sanitized[key] = outliers(hashmap[key][0:lensMin])

  for A in keyA:
    for B in keyB:
      key = A + "-" + B
      for i in range(len(sanitized[key])):
        ret = A + "," + B + "," + str(sanitized[key][i])
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
 
data = loadJSONs(conditions.ALL)
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


for session in data:
  keys = labels(session)

  if nonEmpty(session):
    if session['modality'] == 'text':
      
      #pass
      pprint(session)
      sys.exit(0)

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

            mapArrayAppendKeys(mapSimilarity, ['primed'], sim);
            mapArrayAppendKeys(mapSimilarity, ['unprimed'], unseenSim)

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
    ret.append((item - vMin) / (vMax - vMin))
  return ret



###CUT LENGHT TO SAME FOR ALL CONDITIONS

###TAKE OUT OUTLIERS

###NORMALIZE




#### take out outliers
mapSimilarity['primed'] = outliers(mapSimilarity['primed'])
mapSimilarity['unprimed'] = outliers(mapSimilarity['unprimed'])

### NORMALIZE
simMax = max(mapSimilarity['primed'])
simMin = min(mapSimilarity['unprimed'])
pprint("---Normalized")
ss = {'primed': normalize(mapSimilarity['primed'], simMin, simMax),
'unprimed': normalize(mapSimilarity['unprimed'], simMin, simMax)}

###SS = remove outliers, normalize
pprint(ss)


exportOneWayAnova("2d-similarity.csv", ss, ['primed', 'unprimed'], False)

keys = ['history', 'nohistory', '2d', 'text']
exportConditions("overview-specificity.csv", specificities, keys)


pprint("---Normalized")
for k,v in ss.iteritems():
  printElapsedStats(v, k)

pprint("---Similarity")
for k,v in ss.iteritems():
  printElapsedStats(v, k)
