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




###SPECIFICITY
specificities = {}
specNoDesign = {}
data = loadData()

for session in data:
  keys = [labelDesign(session, True)]
 
  ###2d MODALITY
  if session['modality'] == '2d' and len(session['myVals']) > 0:

    corpus = ""

    for feedback in session['myVals']:
      corpus += feedback['text'] + " "

    specificity = average_specificity2(corpus)

    if specificity != -1:
      mapArrayAppendKeys(specificities, keys, specificity)
      mapArrayAppendKeys(specNoDesign, [labelDesign(session)], specificity)

  ###TEXT MODALITY
  
  #elif len(session['myVals']['val']) > 0:
  elif session['modality'] == 'text' and len(session['myVals']['val']) > 0: 

    corpus = session['myVals']['val']
    #print corpus
    #system.exit()

    specificity = average_specificity2(corpus)

    if specificity != -1:
      mapArrayAppendKeys(specificities, keys, specificity)
      mapArrayAppendKeys(specNoDesign, [labelDesign(session)], specificity)

pprint(specificities)

ss = cutMapValueArrayLength(specificities)
ss = cutMapValueArrayOutliers(ss)
ss = normalizeMap(ss)

ss2 = cutMapValueArrayLength(specNoDesign)
ss2 = cutMapValueArrayOutliers(ss2)
ss2 = normalizeMap(ss2)

print(ss)

exportThreeWayAnova('specificity.csv', ss, 
  ['history', 'nohistory'],
  ['text', '2d'],
  ['a', 'b', 'c'])

pprint(ss2)

keys = ['history-text', 'history-2d', 'nohistory-2d', 'nohistory-text']
exportConditions('specificity.csv', ss2, keys)

#pprint("---Conditions Specificity")
#for k,v in specificities.iteritems():
#  printElapsedStats(v, k)


#keys = ['history-2d', 'nohistory-2d', 'history-text', 'nohistory-text']
#exportConditions("specificity.csv", specificities, keys)
#exportAnova("text-specificity.csv", specificities,  ['nohistory', 'history'], ['text','2d'])

#keys = ['history', 'nohistory', '2d', 'text']
#exportConditions("overview-specificity.csv", specificities, keys)

