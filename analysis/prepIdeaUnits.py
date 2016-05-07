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
import csv



def loadSessions():
  file = csv.writer(open('idea_units/presplit_sessions.csv', 'wb'))#("sessions.csv", "idea_units/")
  file.writerow(["session", "corpus"])


  data = sorted(loadData(), key= lambda sess: int(sess['code']))
  count = 0

  for session in data:
    keys = labels(session)


    ###2d MODALITY
    if session['modality'] == '2d':
      for feedback in session['myVals']:
        
        count += 1
        corpus = feedback['text']
        file.writerow([str(session['code']), corpus])


    else: 

      count += 1
      corpus = session['myVals']['val']
      file.writerow([str(session['code']), corpus])


  #file.close()
  print "Count: " + str(count)

#split by '###' delimeter
def splitSessions():
  with open('idea_units/split_sessions.csv', 'rbU') as fileIn:
    with open('idea_units/idea_units.csv', 'wb') as fileOut:

      writerOut = csv.writer(fileOut)
      readerIn = csv.reader(fileIn)

      for row in readerIn:
        id = row[0]
        units = row[1].split("#")

        if len(units) != 1:
          pprint(units)

        for unit in units:
          writerOut.writerow([id, unit])



#loadSessions()
splitSessions()
