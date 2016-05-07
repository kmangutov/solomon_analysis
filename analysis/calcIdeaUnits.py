# -*- coding: utf-8 -*-

from pattern.vector import Document, Vector, distance, normalize
from dataInterface import lookupDemo, lookupSession, loadJSON, loadJSONs, loadData, lJSON, loadCSV
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
from memoize import Memoize


def mapPercentify(map):
  sum = 0.0
  out = {}
  for k,v in map.iteritems():
    sum += v
  for k,v in map.iteritems():
    out[k] = v/sum
  return out


###
ideas = loadCSV('idea_units/idea_units_labeled.csv')

lookupDemo = Memoize(lookupDemo)
count = 0


## {"nohistory-2d-b":{"0":"6", "1":32, ...}}
conditions = {}
conditionsAnova = {}
###


for idea in ideas:


  ### header
  if count == 0:
    count += 1
    continue


  sessionId = int(idea[0])
  session = lookupSession(sessionId)
  text = idea[1]
  labels = idea[2].split("=")

  if '' in labels:
    labels.remove('')
  for label in labels:
    if '\n' in label:
      labels.remove(label)
      labels.append(label[:-1])

  conditionLabel = labelDesign(session, False) 

  counts = {}
  if conditionLabel in conditions:
    counts = conditions[conditionLabel]
  else:
    counts = {}

  mapIncKeys(counts, labels)
  conditions[conditionLabel] = counts

  for label in labels:
    mapArrayAppendKeys(conditionsAnova, [labelDesign(session)],label)


percented = {}

for k,v in conditions.iteritems():
  percented[k] = mapPercentify(v)

for k,v in conditions.iteritems():
  print '###' + k + '###'
  pprint(conditions[k])
  pprint(percented[k])

ss = cutMapValueArrayLength(conditionsAnova)
exportAnova('idea-units.csv', ss, 
  ['history', 'nohistory'],
  ['text', '2d'])















