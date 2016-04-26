
from dataInterface import loadJSON, loadJSONs
import json
from pprint import pprint
import os
import conditions
from formatting.csvUtil import CSVFile
import sys


def mapInc(hashmap, key):
  if not key in hashmap:
    hashmap[key] = 1
  else:
    hashmap[key] = hashmap[key] + 1

def mapFile(hashmap, fileName):
  if not fileName in hashmap:
    hashmap[fileName] = CSVFile(fileName, '')
  else:
    pass
  return hashmap[fileName]


codesEncountered = []
def encounterCode(code):
  if code not in codesEncountered:
    codesEncountered.append(code)
    return
  else:
    pprint("What, encounter " + str(code) + " twice")



  #csvFile = CSVFile(name, subdir)
  #csvFile.write(header)
  #csvFile.write(ret[0:-1])
  #csvFile.close()





#EMPTY TEXT CONDITION

count = {}
files = {}

data = loadJSONs(conditions.TEXT)

for session in data:
  fileName = session['file']

  encounterCode(session['code'])

  if len(session['myVals']['val']) == 0:
    pass;
  else:
    
    fileName = session['file'][0:-5] + '.csv'
    mapInc(count, fileName)

    pprint(count)

    if count[fileName] >= 31:
      print "ALREADY GOT 30 FOR " + fileName;
      continue;

    csvFile = mapFile(files,'../data3/idea_units_pre/' + fileName);#CSVFile('../data3/idea_units/' + fileName, '')
    csvFile.write(session['myVals']['val'].replace("\n", " "))






###################





#EMPTY ANNOTATION CONDITION
countEmpty = {}
count = {}

data = loadJSONs(conditions.ANNOTATION)

for session in data:
  fileName = session['file']

  encounterCode(session['code'])

  if len(session['myVals']) == 0:
    mapInc(countEmpty, fileName)
    pprint(str(session['code']) + 
      " is a empty session from " + fileName)
  else:
    mapInc(count, fileName)



