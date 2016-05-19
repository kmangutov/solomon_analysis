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



data = loadData()
demos = loadJSON(conditions.DEMO)



def lookupDemo(code):
  for demo in demos:
    if int(demo['code']) == int(code):
      return demo
  return None


effort = {}
effortND = {}
usefulness = {}
usefulnessND = {}

missing = []
missingLabel = []
for session in data:
  demo = lookupDemo(session['code'])

  bad = [776, 1406, 1483]
  if session['code'] in bad:
    continue

  if not demo == None:
    keys = [labelDesign(session, True)]
    keysND = [labelDesign(session, False)]

    valEffort = demo['effort']
    valUsefulness = demo['usefulness']

    mapArrayAppendKeys(effort, keys, valEffort)
    mapArrayAppendKeys(effortND, keysND, valEffort)

    mapArrayAppendKeys(usefulness, keys, valUsefulness)
    mapArrayAppendKeys(usefulnessND, keysND, valUsefulness)
  else:
    missing.append(session['code'])
    missingLabel.append([labelDesign(session, True)])


#effort = cutMapValueArrayLength(effort)
#effortND = cutMapValueArrayLength(effortND)

#usefulness = cutMapValueArrayLength(usefulness)
#usefulnessND = cutMapValueArrayLength(usefulnessND)



keys = ['history-2d', 'nohistory-2d', 'history-text', 'nohistory-text']

exportConditions('effort.csv', effortND, keys)
exportThreeWayAnova('effort.csv', effort,
  ['history', 'nohistory'],
  ['text', '2d'],
  ['a', 'b', 'c'])

exportConditions('usefulness.csv', usefulnessND, keys)
exportThreeWayAnova('usefulness.csv', usefulness,
  ['history', 'nohistory'],
  ['text', '2d'],
  ['a', 'b', 'c'])



pprint("---EFFORT")
for k,v in effortND.iteritems():
  printElapsedStats(v);


pprint("---USEFULNESS")
for k,v in usefulnessND.iteritems():
  printElapsedStats(v);



