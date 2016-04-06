
from dataInterface import loadJSON, loadJSONs
import json
from pprint import pprint
import os
import conditions
from specificity import average_specificity2
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

def exportConditions(stat, hashmap, keys):
  print "#################################################"
  csvFile = CSVFile("d3/" + stat)

  lens = {len(hashmap[key]) for key in keys}
  lensMin = min(lens)

  def outliers(arr):
    arr.sort()
    arrLen = len(arr)
    cutLen = int(round(arrLen * 0.025))
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





###SPECIFICITY
specificities = {}
data = loadJSONs(conditions.ALL)

for session in data:
  keys = labels(session)
 
  ###2d MODALITY
  if session['modality'] == '2d' and len(session['myVals']) > 0:

    corpus = ""

    for feedback in session['myVals']:
      corpus += feedback['text'] + " "

    specificity = average_specificity2(corpus)
    mapArrayAppendKeys(specificities, keys, specificity)

  ###TEXT MODALITY
  
  #elif len(session['myVals']['val']) > 0:
  elif session['modality'] == 'text' and len(session['myVals']['val']) > 0: 

    corpus = session['myVals']['val']
    print corpus
    #system.exit()

    specificity = average_specificity2(corpus)
    mapArrayAppendKeys(specificities, keys, specificity)


pprint("---Conditions Specificity")
for k,v in specificities.iteritems():
  printElapsedStats(v, k)


keys = ['history-2d', 'nohistory-2d', 'history-text', 'nohistory-text']
exportConditions("specificity.csv", specificities, keys)
exportAnova("text-specificity.csv", specificities,  ['nohistory', 'history'], ['text','2d'])

keys = ['history', 'nohistory', '2d', 'text']
exportConditions("overview-specificity.csv", specificities, keys)

