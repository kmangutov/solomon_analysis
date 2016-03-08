import json
from pprint import pprint
import os

def loadJSON(fileName):

  def jsonToStrict(s):
    return "{\"val\": [" + s[:-3] + "]}"


  with open('data1/' + fileName) as f:
    print f
    fixed = jsonToStrict(f.read())
    
    #fOut = open('write.json', 'w')
    #fOut.write(fixed)
    #fOut.close()
    #pprint(fixed)
    
    data = json.loads(fixed)
    return data



fileName = "prod-v6-history-2d-b.json"



pprint(loadJSON(fileName))