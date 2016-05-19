

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




###ELAPSED TIME

elapsed = {}
elapsedND = {}
data = loadData()

for session in data:

  keys = [labelDesign(session, True)]
  keysND = [labelDesign(session, False)]

  time = session['elapsedTime']

  mapArrayAppendKeys(elapsed, keys, time)
  mapArrayAppendKeys(elapsedND, keysND, time)

###

#ss = cutMapValueArrayLength(elapsed)
#ss = cutMapValueArrayOutliers(ss, 0.025)

ss = elapsed
ss2 = elapsedND

#ss2 = cutMapValueArrayLength(elapsedND)
#ss2 = cutMapValueArrayOutliers(ss2, 0.025)

###

exportThreeWayAnova('time-elapsed.csv', ss, 
  ['history', 'nohistory'],
  ['text', '2d'],
  ['a', 'b', 'c'])

keys = ['history-text', 'history-2d', 'nohistory-2d', 'nohistory-text']
exportConditions('time-elapsed.csv', ss2, keys)

pprint("---Elapsed Time")
for k,v in elapsedND.iteritems():
  printElapsedStats(v, k)
