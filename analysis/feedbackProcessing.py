
from dataInterface import loadJSON, loadJSONs
import json
from pprint import pprint
import os
import conditions



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