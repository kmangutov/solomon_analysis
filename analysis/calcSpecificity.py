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
from specificity import countStopWords
from specificity2 import countAvgHypernyms, calcSpecificity




###SPECIFICITY
specificities = {}
specNoDesign = {}

stops = {}
stopsND = {}

data = loadData()

texts = []
bad = []

for session in data:
  keys = [labelDesign(session, True)]
 
  ###2d MODALITY
  if session['modality'] == '2d' and len(session['myVals']) > 0:

    corpus = ""

    for feedback in session['myVals']:
      corpus += feedback['text'] + ". "

    specificity = calcSpecificity(corpus)
    #specificity = countAvgHypernyms(corpus)

    if specificity != None and specificity > -1:
      mapArrayAppendKeys(specificities, keys, specificity)
      mapArrayAppendKeys(specNoDesign, [labelDesign(session)], specificity)

      t = {}
      t['text'] = corpus
      t['val'] = specificity
      t['id'] = session['code']
      texts.append(t)
    else:
      t = {}
      t['text'] = corpus
      t['id'] = session['code']
      bad.append(t)


    stopWords = countStopWords(corpus)
    if stopWords >= 0:
      mapArrayAppendKeys(stops, keys, stopWords)
      mapArrayAppendKeys(stopsND, [labelDesign(session)], stopWords)





  ###TEXT MODALITY
  elif session['modality'] == 'text' and len(session['myVals']['val']) > 0: 

    corpus = session['myVals']['val']


    specificity = calcSpecificity(corpus)
    #specificity = countAvgHypernyms(corpus)

    if specificity != None and specificity > -1:
      mapArrayAppendKeys(specificities, keys, specificity)
      mapArrayAppendKeys(specNoDesign, [labelDesign(session)], specificity)

      t = {}
      t['text'] = corpus
      t['val'] = specificity
      t['id'] = session['code']
      texts.append(t)
    else:
      t = {}
      t['text'] = corpus
      t['id'] = session['code']
      bad.append(t)

    stopWords = countStopWords(corpus)
    if stopWords >= 0:
      mapArrayAppendKeys(stops, keys, stopWords)
      mapArrayAppendKeys(stopsND, [labelDesign(session)], stopWords)

pprint(specificities)

ss = normalizeMap(specificities)
ss2 = normalizeMap(specNoDesign)
#ss = specificities
#ss2 = specNoDesign

#ss = specificities
#ss = cutMapValueArrayLength(specificities)
#ss = cutMapValueArrayOutliers(ss)
#ss = normalizeMap(ss)

#ss2 = specNoDesign
#ss2 = cutMapValueArrayLength(specNoDesign)
#ss2 = cutMapValueArrayOutliers(ss2)
#ss2 = normalizeMap(ss2)

print(ss)

exportThreeWayAnova('specificity.csv', ss, 
  ['history', 'nohistory'],
  ['text', '2d'],
  ['a', 'b', 'c'])

pprint(ss2)
#keys = ['history-text', 'history-2d', 'nohistory-2d', 'nohistory-text']
#exportConditions('specificity.csv', ss2, keys)




exportThreeWayAnova('stopwords.csv', stops,   
  ['history', 'nohistory'],
  ['text', '2d'],
  ['a', 'b', 'c'])
keys = ['history-text', 'history-2d', 'nohistory-2d', 'nohistory-text']
exportConditions('stopwords.csv', stopsND, keys)




##########bad = [776, 1406, 1483, ]

sort = sorted(texts, key= lambda k: k['val'])
pprint(sort)

#print "BAD \n\n"
#for b in bad:
#  pprint(b)
#  pprint(calcSpecificity(b['text']))

