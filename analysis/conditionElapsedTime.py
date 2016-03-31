
from dataInterface import loadJSON, loadJSONs
import json
from pprint import pprint
import os
import conditions
import sys
from pprint import pprint


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






###ELAPSED TIME
conditionsElapsed = {}
goodElapsed = {}
badElapsed = {}
goodCount = {}
badCount = {}

data = loadJSONs(conditions.ALL)

for session in data:

  #if float(session['elapsedTime']) == 25.55 or float(session['elapsedTime']) == 29.01:
  #  print(session)
  #  print("---labels: ")
  #  pprint(labels(session))

  keys = labels(session)
  if nonEmpty(session):
    mapArrayAppendKeys(conditionsElapsed, keys, session['elapsedTime'])
    mapArrayAppendKeys(goodElapsed, keys, session['elapsedTime'])

    mapIncKeys(goodCount, keys)

  else:
    mapArrayAppendKeys(badElapsed, keys, session['elapsedTime'])
    mapInc(badCount, label(session))
    
    mapIncKeys(badCount, keys)



pprint("---Feedback Elapsed Time")
for k,v in conditionsElapsed.iteritems():
  printElapsedStats(v, k)

pprint("---Good Elapsed Time")
for k,v in goodElapsed.iteritems():
  printElapsedStats(v, k)

pprint("---Bad Elapsed Time")
for k,v in badElapsed.iteritems():
  printElapsedStats(v, k)

pprint("---Good Count")
pprint(goodCount)

pprint("---Bad Count")
pprint(badCount)

sys.exit()

###CHAR LENGTH
conditionsCharLength = {}
conditions2dFeedbacks = {}
data = loadJSONs(conditions.ALL)

for session in data:
  keys = labels(session)
 
  ###2d MODALITY
  if session['modality'] == '2d' and len(session['myVals']) > 0:

    charSum = 0
    feedbackCount = 0

    for feedback in session['myVals']:
      charSum += len(feedback['text'])
      feedbackCount += 1

    mapArrayAppendKeys(conditionsCharLength, keys, charSum)
    mapArrayAppendKeys(conditions2dFeedbacks, keys, feedbackCount)

  ###TEXT MODALITY
  
  #elif len(session['myVals']['val']) > 0:
  elif session['modality'] == 'text' and len(session['myVals']['val']) > 0: 

    chars = len(session['myVals']['val'])
    mapArrayAppendKeys(conditionsCharLength, keys, chars)


pprint("---Conditions Char Length")
for k,v in conditionsCharLength.iteritems():
  printElapsedStats(v, k)

pprint("---2d Condition Num Feedbacks")
for k,v in conditions2dFeedbacks.iteritems():
  printElapsedStats(v, k)


#######################
##TIME LOOKING AT FEEDBACK
feedbacks = {}

for session in data:
  keys = labels(session)

  if nonEmpty(session):

    if session['modality'] == 'text':

      feedbacksOpened = 0
      for history in session['stack']:
        if float(history['duration']) > 0:
          feedbacksOpened += 1

      mapArrayAppendKeys(feedbacks, keys, feedbacksOpened)

    else:

      feedbacksOpened = []
      for history in  session['stack']:
        if history['action'] == 'hover':

          historyId = history['feedback']['id']
          if not historyId in feedbacksOpened:

            #novel hover feedback
            threshold = 1 #seconds

            if float(history['duration']) > threshold:
              feedbacksOpened.append(historyId)

      mapArrayAppendKeys(feedbacks, keys, len(feedbacksOpened))



pprint("---Feedbacks opened")
for k,v in feedbacks.iteritems():
  printElapsedStats(v, k)







