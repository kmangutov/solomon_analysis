import json
from pprint import pprint
import os
from memoize import Memoize


def loadJSON(fileName):

  def jsonToStrict(s):
    return "{\"val\": [" + s[:-1].replace("\n", ",") + "]}"


  with open('../data3/' + fileName) as f:
    fixed = jsonToStrict(f.read())

    
    #fOut = open('write.json', 'w')
    #fOut.write(fixed)
    #fOut.close()
    #pprint(fixed)
    
    data = json.loads(fixed)
    return data['val']

def loadJSONs(fileNames):
    ret = []
    for fileName in fileNames:
        json = loadJSON(fileName)
        for val in json:
            val["file"] = fileName
            val["history"] = "nohistory" not in fileName
            val["modality"] = "text" if ("text" in fileName) else "2d"



        ret += json
    return ret

loadJSON = Memoize(loadJSON)

if __name__ == "__main__":
    loadJSON("fake.json")
