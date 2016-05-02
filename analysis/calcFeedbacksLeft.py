
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
from specificity import average_specificity2




#######################
##feedbacks opened

data = loadData()
feedbacks = {}
feedbacksND = {}

for session in data:
  keys = [labelDesign(session, True)]
  keysND = [labelDesign(session, False)]


  if session['modality'] != 'text':

    pprint(session['myVals'])
    feedbacksLeft = len(session['myVals'])

    mapArrayAppendKeys(feedbacks, keys, feedbacksLeft)
    mapArrayAppendKeys(feedbacksND, keysND, feedbacksLeft)



###
ss = cutMapValueArrayLength(feedbacks)
ss = cutMapValueArrayOutliers(ss)
#ss = normalizeMap(ss)

ss2 = cutMapValueArrayLength(feedbacksND)
ss2 = cutMapValueArrayOutliers(ss2)
#ss2 = normalizeMap(ss2)


keys = ['history-2d', 'nohistory-2d']
exportConditions("feedbacks-left.csv", ss2, keys)
exportThreeWayAnova("feedbacks-left.csv", ss, 
  ['history', 'nohistory'], ['2d'], ['a', 'b', 'c'])


pprint("---Feedbacks left")
for k,v in feedbacks.iteritems():
  printElapsedStats(v, k)

