import json
from pprint import pprint
import os
from memoize import Memoize
import conditions


def loadJSON(fileName):

  def jsonToStrict(s):
    return "{\"val\": [" + s[:-1].replace("\n", ",") + "]}"


  with open('../data4/' + fileName) as f:
    fixed = jsonToStrict(f.read())
    
    data = json.loads(fixed)
    return data['val']


def loadData():

    demos = loadJSON(conditions.DEMO)
    def lookupDemo(code):
      for demo in demos:
        if int(demo['code']) == int(code):
          return demo
      return None

    def mapInc(hashmap, key):
        if not key in hashmap:
            hashmap[key] = 1
        else:
            hashmap[key] = hashmap[key] + 1

    def label(session):
        key = "history" + str(session['history']) + "-modality" + str(session['modality']) + "-" + str(session['imgCondition'])
        return key

    def nonEmpty(session):
        nonEmptyAnnot = session['modality'] == '2d' and len(session['myVals']) > 0
        nonEmptyText = session['modality'] == 'text' and len(session['myVals']['val']) > 0
        return nonEmptyAnnot or nonEmptyText

    count = {}
    data = loadJSONs(conditions.ALL)
    ret = []

    for session in data:

        if not nonEmpty(session) or lookupDemo(session['code']) == None:
            continue

        sessLabel = label(session)

        if sessLabel not in count:
            count[sessLabel] = 0

        if count[sessLabel] < 30:
            ret.append(session)
            mapInc(count, sessLabel)

    pprint(count)
    return ret


def loadJSON(fileName):

  def jsonToStrict(s):
    return "{\"val\": [" + s[:-1].replace("\n", ",") + "]}"


  with open('../data4/' + fileName) as f:
    fixed = jsonToStrict(f.read())
    
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
loadData = Memoize(loadData)

if __name__ == "__main__":
    #loadJSON("fake.json")
    data = loadData()
    print "loaded " + str(len(data))
