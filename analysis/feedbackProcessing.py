
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



def cutMapValueArrayLength(map):

  lens = {len(map[key]) for key in map.keys()}
  minLen = min(lens)
  ss = map

  for key in ss.keys():
    ss[key] = ss[key][0:minLen]
  return ss

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

def labelDesign(session, lDesign=False):

  history = "history" if session['history'] else "nohistory"
  modality = str(session['modality']) 
  design = str(session['imgCondition'])

  #key = "history" + str(session['history']) + "-modality" + str(session['modality']) + "-design" + str(session['imgCondition'])
  key = ""
  if lDesign:
    key = "-".join([history, modality, design])
  else:
    key = "-".join([history, modality])

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
      if len(hashmap[key]) > i:
        ret += str(hashmap[key][i]) + ","
      else: ret += ","
    csvFile.write(ret[0:-1])

  csvFile.close()

def exportAnova(stat, hashmap, keyA, keyB):
  print "#################################################"
  csvFile = CSVFile("anova/" + stat)

  pprint(hashmap)

  for A in keyA:
    for B in keyB:
      key = A + "-" + B
      for i in range(len(hashmap[key])):
        ret = A + "," + B + "," + str(hashmap[key][i])
        csvFile.write(ret)

  csvFile.close()

def exportThreeWayAnova(stat, hashmap, keyA, keyB, keyC):
  print "#################################################"
  csvFile = CSVFile("anova/" + stat)

  pprint(hashmap)

  for A in keyA:
    for B in keyB:
      for C in keyC:
        key = A + "-" + B + "-" + C
        for i in range(len(hashmap[key])):
          ret = A + "," + B + "," + C + "," + str(hashmap[key][i])
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

def outliers(arr, cut = 0.025):
  arr.sort()
  arrLen = len(arr)
  cutLen = int(round(arrLen * cut))
  pprint("cutlen: " + str(cutLen))
  if cutLen == 0:
    return arr
  return arr[cutLen:-cutLen]

def cutMapValueArrayOutliers(map, cut = 0.025):
  ss = map
  for key in ss.keys():
    ss[key] = outliers(ss[key], cut)
  return ss

def normalizeArr(arr, vMin, vMax):
  ret = []
  for item in arr:
    ret.append((float(item) - vMin) / (vMax - vMin))
  return ret

def normalizeMap(map):
  ss = map
  vals = []
  for v in map.values():
    vals += v

  vMin = min(vals)
  vMax = max(vals)

  for k,v in map.iteritems():
    ss[k] = normalizeArr(v, vMin, vMax)
  return ss
