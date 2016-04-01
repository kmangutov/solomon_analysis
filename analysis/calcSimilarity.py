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

def similarity(a, b):

  docA = Document(a)
  docB = Document(b)

  vecA = normalize(docA.vector)
  vecB = normalize(docB.vector)

  #print docA.vector
  return 1 - distance(vecA, vecB)

for i in range(0, len(feedbacks)):
  print similarity(feedbacks[i], feedbacks2[i])
