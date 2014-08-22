import json

def readData():
    f = open("audio_1408627784", "r")
    f2 = open("result_audio", "w")
    jsonData = json.load(f)
    sortedA = []
    for k in jsonData:
        for x in k.keys():
            sortedA.append([int(x) / 1000.0, k[x]])
    f2.write( json.dumps(sorted(sortedA)) )
    f.close()

readData()