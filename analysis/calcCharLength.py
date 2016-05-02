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




###CHAR LENGTH
charLength = {}
charLengthNoDesign = {}

data = loadData()
count = 0

for session in data:
  count += 1
  keys = [labelDesign(session, True)]
  keysND = [labelDesign(session, False)]
 
  ###2d MODALITY
  if session['modality'] == '2d':

    charSum = 0
    feedbackCount = 0

    for feedback in session['myVals']:
      charSum += len(feedback['text'])
      feedbackCount += 1

    mapArrayAppendKeys(charLength, keys, charSum)
    mapArrayAppendKeys(charLengthNoDesign, keysND, charSum)

  ###TEXT MODALITY
  
  #elif len(session['myVals']['val']) > 0:
  else:

    chars = len(session['myVals']['val'])
    mapArrayAppendKeys(charLength, keys, chars)
    mapArrayAppendKeys(charLengthNoDesign, keysND, chars)

###
ss = cutMapValueArrayLength(charLength)
ss = cutMapValueArrayOutliers(ss)
#ss = normalizeMap(ss)

ss2 = cutMapValueArrayLength(charLengthNoDesign)
ss2 = cutMapValueArrayOutliers(ss2)
#ss2 = normalizeMap(ss2)

pprint(ss2)

keys = ['history-2d', 'nohistory-2d', 'history-text', 'nohistory-text']
exportConditions("char-length.csv", ss2, keys)
exportThreeWayAnova("char-length.csv", ss, 
  ['nohistory', 'history'], ['text','2d'], ['a', 'b', 'c'])

print(count)
###
