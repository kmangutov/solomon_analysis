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
#from specificity import average_specificity2




###CHAR LENGTH
charLength = {}
charLengthNoDesign = {}

data = loadData()
count = 0

textsSP = []
textsNS = []

for session in data:
  count += 1
  keys = [labelDesign(session, True)]
  keysND = [labelDesign(session, False)]
 
  ###2d MODALITY
  if session['modality'] == '2d':

    charSum = 0
    feedbackCount = 0
    corpus = ""

    for feedback in session['myVals']:
      charSum += len(feedback['text'])
      feedbackCount += 1
      corpus += feedback['text'] + ". "

    mapArrayAppendKeys(charLength, keys, charSum)
    mapArrayAppendKeys(charLengthNoDesign, keysND, charSum)

    t = {}
    t['length'] = charSum
    t['text'] = corpus
    t['id'] = session['code']
    textsSP.append(t);


  ###TEXT MODALITY
  
  #elif len(session['myVals']['val']) > 0:
  else:

    chars = len(session['myVals']['val'])
    mapArrayAppendKeys(charLength, keys, chars)
    mapArrayAppendKeys(charLengthNoDesign, keysND, chars)

    t = {}
    t['length'] = charSum
    t['text'] = session['myVals']['val']
    t['id'] = session['code']
    textsNS.append(t)

###
ss = charLength
#ss = cutMapValueArrayLength(charLength)
#ss = cutMapValueArrayOutliers(ss)
#ss = normalizeMap(ss)

ss2 = charLengthNoDesign
#ss2 = cutMapValueArrayLength(charLengthNoDesign)
#ss2 = cutMapValueArrayOutliers(ss2)
#ss2 = normalizeMap(ss2)

pprint(ss2)

keys = ['history-2d', 'nohistory-2d', 'history-text', 'nohistory-text']
exportConditions("char-length.csv", ss2, keys)
exportThreeWayAnova("char-length.csv", ss, 
  ['nohistory', 'history'], ['text','2d'], ['a', 'b', 'c'])

print(count)
###


###########

print "\n\n\n"
sort = sorted(textsSP, key= lambda k: k['length'])
pprint("Spatial-----------")
mid = len(sort) / 2
#pprint(sort[-3:])
pprint(sort[mid - 2:mid + 2])


sort = sorted(textsNS, key= lambda k: k['length'])
pprint("Non-spatial--------")
mid = len(sort) / 2
pprint(sort[mid - 2:mid + 2])



