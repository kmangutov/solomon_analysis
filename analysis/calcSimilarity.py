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
from feedbackProcessing import *





 ###############
 
data = loadData()#loadJSONs(conditions.ALL)#loadJSONs(conditions.TEXT)#loadJSONs(conditions.ALL)
mapSimilarity = {}
mapSimilarityDesign = {}
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

      design = session['imgCondition']
      mapArrayAppendKeys(mapSimilarityDesign, ['primed-text-' + design], sim);
      mapArrayAppendKeys(mapSimilarityDesign, ['unprimed-text-' + design], unseenSim);



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

            design = session['imgCondition']
            mapArrayAppendKeys(mapSimilarityDesign, ['primed-2d-' + design], sim);
            mapArrayAppendKeys(mapSimilarityDesign, ['unprimed-2d-' + design], unseenSim);

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

###CUT LENGHT TO SAME FOR ALL CONDITIONS
#ss = cutMapValueArrayLength(mapSimilarity)
#pprint("CUT")
#pprint(ss)
ss = mapSimilarity

###TAKE OUT OUTLIERS
#ss = cutMapValueArrayOutliers(ss)
#pprint("OUTLIERS")
#pprint(ss)

###NORMALIZE
#ss = normalizeMap(ss)
#for key in ss.keys():
#  ss[key] = normalize(ss[key], simMin, simMax)


pprint(ss)
exportAnova('similarity.csv', ss, ['primed', 'unprimed'], ['text', '2d']);


keys = ['unprimed-text', 'unprimed-2d', 'primed-text', 'primed-2d']
exportConditions("similarity.csv", ss, keys)



###THREE WAY ANOVA

pprint(mapSimilarityDesign)
#ss3 = cutMapValueArrayLength(mapSimilarityDesign)
#ss3 = cutMapValueArrayOutliers(ss3)
#ss3 = normalizeMap(ss3)
ss3 = mapSimilarityDesign

exportThreeWayAnova('similarity-three-way.csv', ss3, 
  ['unprimed', 'primed'],
  ['text', '2d'],
  ['a', 'b', 'c'])




