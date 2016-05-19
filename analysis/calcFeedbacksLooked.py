
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



#######################
##feedbacks opened

data = loadData()
feedbacks = {}
feedbacksND = {}

for session in data:
  keys = [labelDesign(session, True)]
  keysND = [labelDesign(session, False)]


  if session['modality'] == 'text':

    feedbacksOpened = 0
    for history in session['stack']:
      if float(history['duration']) > 0:
        feedbacksOpened += 1

    mapArrayAppendKeys(feedbacks, keys, feedbacksOpened)
    mapArrayAppendKeys(feedbacksND, keysND, feedbacksOpened)


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
    mapArrayAppendKeys(feedbacksND, keysND, len(feedbacksOpened))



###
#ss = cutMapValueArrayLength(feedbacks)
#ss = cutMapValueArrayOutliers(ss)
#ss = normalizeMap(ss)

#ss2 = cutMapValueArrayLength(feedbacksND)
#ss2 = cutMapValueArrayOutliers(ss2)
#ss2 = normalizeMap(ss2)

ss = feedbacks
ss2 = feedbacksND

keys = ['history-2d', 'history-text']
exportConditions("feedbacks-looked.csv", ss2, keys)
exportThreeWayAnova("feedbacks-looked.csv", ss, 
  ['history'], ['text','2d'], ['a', 'b', 'c'])

