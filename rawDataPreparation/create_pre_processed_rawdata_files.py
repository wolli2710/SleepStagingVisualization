#this file needs the filename format audio_26_mattrass instead of audio_1407157806
#this file needs the filename format acceleration_26_mattrass instead of acceleration_1407157806

import time
import json
import math
import numpy as np
import pandas as pd
import datetime

acceleration_filename = "acceleration_"
audio_filename = "audio_"
positions = [ "_mattrass","_right_arm"]
outputFormat = "csv"
separator = ","
hz = 500
interval = 1.0


def calculate_distance(vec1, vec2):
    return math.sqrt( math.pow( (vec1[0]-vec2[0]), 2) + math.pow( (vec1[1]-vec2[1]), 2) + math.pow( (vec1[2]-vec2[2]), 2) )

def interpolateAcceleration(array):
    n = [np.nan]*hz
    l = float(len(n)) / len(array)
    for i in range(0, len(array)):
        j = int(math.floor(i*l))
        n[j] = array[i] * 100
    return n

def interpolate(n, lastValue=0):
    if np.isnan(n[0]):
        n[0] = lastValue
    val1=np.nan
    i1 = 0
    for i in range(0,len(n)):
        if not np.isnan(n[i]) and not np.isnan(val1):
            interpolation = (n[i] - val1) / (i - i1)
            step = 0
            for j in range(i1, i+1):
                n[j] = val1 + (interpolation * step)
                step += 1
            val1=n[i]
            i1 = i
        if not np.isnan(n[i]) and np.isnan(val1):
            val1 = n[i]
            i1 = i
    if np.isnan(n[-1]):
        for i in range(i1, len(n)):
            n[i] = val1
    return n

def interpolateSoundValues( currentValues ):
    n = [np.nan]*hz

    l = float(len(n)) / len(currentValues)
    for i in range(0, len(currentValues)):
        j = int( math.floor(i*l) )
        n[j] = currentValues[i]
    return n

for pos in positions:
    for vp in range(26, 32):

        markerFileLines = open("../marker_files/timestamp_and_marker_"+str(vp)+".txt", "r").readlines()
        startTimestamp = int(markerFileLines[0])
        start = int(markerFileLines[1])
        current_folder = "../result_data_vp"+str(vp)+pos+"/"


        outputFile = open(current_folder+"VP"+str(vp)+pos+"_output."+outputFormat, "w")

        print("raw data started")
        for line in open("../sleep_staging_files/VP"+str(vp)+"_NAP.txt", "r").readlines():
            line = line.replace(",", ".")
            values = line.split(" ")
            values2 = []
            for i in range(start, len(values)):
                try:
                    y = float(values[i])
                    values2.append( y )
                except ValueError:
                    y
            outputFile.write(str(values[0])+separator)
            for line in values2:
                outputFile.write(str(line)+separator)
            outputFile.write("\n")



        lastVector = [0,0,0]
        nextSecond = 0
        currentDistances = []
        allValues = []
        accelerationLines = open(current_folder+acceleration_filename+str(vp)+pos, "r").readlines()
        lastValue = 0

        print("acceleration data started")
        outputFile.write("acceleration"+separator)
        cnt = 0
        for line in accelerationLines:
            line = line[0:-2]
            j = json.loads(line)
            array = j.values()
            try:
                distance = calculate_distance(lastVector, array[0])
                lastVector = array[0]
            except KeyError:
                j
            try:
                timestamp = int(j.keys()[0])
                if timestamp >= startTimestamp:
                    t = float(timestamp / 1000000000)
                    currentDistances.append(distance)

                    if( t >= nextSecond ):
                        cnt += 1
                        nextSecond = t+interval
                        n = interpolateAcceleration( currentDistances )
                        allValues = interpolate(n, lastValue)
                        lastValue = allValues[-1]
                        currentDistances = []
                        for line in allValues:
                            outputFile.write(str(line)+separator)
            except ValueError:
                print(timestamp)
        print("cnt "+str(cnt))
        outputFile.write("\n")


        currentValues = []
        soundLines = open(current_folder+audio_filename+str(vp)+pos, "r").readlines()
        nextSecond = 0


        print("sound data started")
        outputFile.write("audio"+separator)
        for line in soundLines:
            line = line[0:-2]
            j = json.loads(line)
            array = j.values()

            try:
                timestamp = int(j.keys()[0])
                value = int(array[0])
                if value == 0:
                    value = np.nan
                if timestamp >= startTimestamp:
                    t = timestamp / 1000
                    currentValues.append(value)

                    if( t >= nextSecond ):
                        nextSecond = t+interval
                        n = interpolateSoundValues( currentValues )
                        allValues = interpolate(n, lastValue)
                        lastValue = allValues[-1]
                        currentValues = []
                        for line in allValues:
                            outputFile.write(str(line)+separator)
            except ValueError:
                print(timestamp)

            
        # outputFile.write("\n")
        outputFile.close()


outputFormat = "csv"
positions = ["_right_arm", "_mattrass"]

for pos in positions:
    for vp in range(26, 32):

        filename = "VP"+str(vp)+pos+"_output."+outputFormat

        f = open(filename, "r").readlines()
        f2 = open("r_"+filename, "w")

        lines = 25
        length = len(f[0])


        print(length)

        n = [[0]*(length*10)]*(lines+1)

        for i in range(0, lines+1):
            n[i] = f[i].split(",")     
            if(len(n[i]) < length):
                length = len(n[i])

            print(length)

        cnt = 0
        for i in range(0, length):
            for j in range(0, lines+1):
                cnt += 1
                f2.write( n[j][i])
                if j==lines:
                    f2.write("\n")
                else:
                    f2.write(",")
        print(cnt)
        f2.close()


######## interpolation test cases ##############
# n1 = [1, np.nan, np.nan, 100]
# n1 = [-10, np.nan, np.nan, 100, np.nan, -200]
# n1 = [-10, np.nan, np.nan, -200, np.nan, 200]
# n1 = [np.nan, -10, np.nan, np.nan, -200, np.nan, 200]
# n1 = [np.nan, -10, np.nan, np.nan, -200, np.nan, 200, np.nan, np.nan]
# n1 = [0, np.nan, np.nan, np.nan, 100]

# print(interpolate(n1, 200))
# print(interpolate(n1))