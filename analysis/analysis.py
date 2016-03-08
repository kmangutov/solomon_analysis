
from dataInterface import loadJSON
import json
from pprint import pprint
import os


fileName = "prod-v6-history-2d-b.json"
data = loadJSON(fileName)

#pprint(data['val'])
pprint(data[0]['myVals'][0]['text'])

for session in data:
  for feedback in session['myVals']:
      pprint(feedback['text'])
  pprint('----')