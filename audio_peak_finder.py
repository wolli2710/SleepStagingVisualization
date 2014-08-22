import json

def readData():
    f = open("audio_1408627784", "r")
    # f2 = open("result_audio", "w")
    jsonData = json.load(f)
    sortedA = []
    for k in jsonData:
        for x in k.keys():
            if k[x] > 20000:
                print(str(x)+" "+ str(k[x]) )

readData()