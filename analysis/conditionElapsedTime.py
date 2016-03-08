
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

###ELAPSED TIME
conditionsElapsed = {}
data = loadJSONs(conditions.ALL)

for session in data:
  if nonEmpty(session):
    keys = labels(session)
    mapArrayAppendKeys(conditionsElapsed, keys, session['elapsedTime'])

pprint("---Feedback Elapsed Time")
for k,v in conditionsElapsed.iteritems():
  printElapsedStats(v, k)


###CHAR LENGTH
conditionsCharLength = {}
conditions2dFeedbacks = []
data = loadJSONs(conditions.ALL)

for session in data:
  key = label(session)
 
  ###2d MODALITY
  if session['modality'] == '2d' and len(session['myVals']) > 0:

    charSum = 0
    feedbackCount = 0

    for feedback in session['myVals']:
      charSum += len(feedback['text'])
      feedbackCount += 1

    mapArrayAppend(conditionsCharLength, key, charSum)
    conditions2dFeedbacks.append(feedbackCount)

  ###TEXT MODALITY
  
  #elif len(session['myVals']['val']) > 0:
  elif session['modality'] == 'text' and len(session['myVals']['val']) > 0: 

    chars = len(session['myVals']['val'])
    mapArrayAppend(conditionsCharLength, key, chars)


pprint("---Conditions Char Length")
for k,v in conditionsCharLength.iteritems():
  printElapsedStats(v, k)


printElapsedStats(conditions2dFeedbacks, "2d Condition # Feedbacks Left")


