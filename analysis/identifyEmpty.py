
from dataInterface import loadJSON, loadJSONs
import json
from pprint import pprint
import os
import conditions


def mapInc(hashmap, key):
  if not key in hashmap:
    hashmap[key] = 1
  else:
    hashmap[key] = hashmap[key] + 1







codesEncountered = []
def encounterCode(code):
  if code not in codesEncountered:
    codesEncountered.append(code)
    return
  else:
    pprint("What, encounter " + code + " twice")







#EMPTY ANNOTATION CONDITION
countEmpty = {}
count = {}

data = loadJSONs(conditions.ANNOTATION)

for session in data:
  fileName = session['file']

  encounterCode(session['code'])

  if len(session['myVals']) == 0:
    mapInc(countEmpty, fileName)
    pprint(session['code'] + 
      " is a empty session from " + fileName)
  else:
    mapInc(count, fileName)

pprint("EMPTY:")
pprint(countEmpty)
pprint("GOOD:")
pprint(count)


###########################


#EMPTY TEXT CONDITION
countEmpty = {}
count = {}

data = loadJSONs(conditions.TEXT)

for session in data:
  fileName = session['file']

  encounterCode(session['code'])

  if len(session['myVals']['val']) == 0:
    mapInc(countEmpty, fileName)
    pprint(session['code'] + 
      " is a empty session from " + session['file'])
  else:
    mapInc(count, fileName)


pprint("EMPTY:")
pprint(countEmpty)
pprint("GOOD:")
pprint(count)


###################


data = loadJSONs(conditions.ALL)
pprint("all length: " + str(len(data)))



