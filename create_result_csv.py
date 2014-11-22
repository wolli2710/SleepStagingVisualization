import matplotlib
import matplotlib.pyplot as plt
import numpy as np

positions = ["_right_arm", "_mattrass"]

separator = ";"

for vp in range(26, 32):
    for pos in positions:
        inputFile = open("result_data_vp"+str(vp)+pos+"/VP"+str(vp)+pos+"_30sec_chunks.csv", "r")
        outputFile = open("result_data_vp"+str(vp)+pos+"/VP"+str(vp)+"_results.csv", "w")
        lines = inputFile.readlines()

        def printBlock(l, allValues, name):
            outputFile.write(name+separator)
            l1 = len([x for x in l if x > np.mean(allValues)]) 
            l2 = len([x for x in l if x < np.mean(allValues)])
            outputFile.write( str(l1) +separator )
            outputFile.write( str(l2) +separator )
            outputFile.write( str( len( l ) )+separator )
            outputFile.write( str( round(100/float(len( l )) * l1, 2) )+separator )
            outputFile.write( str( round(100/float(len( l )) * l2, 2 ) ) )
            outputFile.write("\n")

        def printValues(x):
            firstLine = True
            constant = []
            wakeUp = []
            wakeUp2 = []
            fallASleep = []
            allValues = []
            wakeUpDictExtended = {}
            wakeUpDictExtended2 = {}
            cnt = 0
            previous_value = 0
            previous_stage = 0
            n = False
            n2 = False
            for i in lines:
                cnt += 1
                if not firstLine:
                    currentLine = i.split(",")
                    allValues.append( float(currentLine[x]) )
                    if(n):
                        wakeUpDictExtended[str(cnt-1)].append( float(currentLine[x]) )
                        n = False
                    if(n2):
                        wakeUpDictExtended2[str(cnt-1)].append( float(currentLine[x]) )
                        n2 = False
                    if( currentLine[1] == "constant"):
                        constant.append( float(currentLine[x]) )
                    if( currentLine[1] == "wake up"):
                        if(previous_stage == 2 and int(currentLine[0]) == 0 ):
                            wakeUpDictExtended2[str(cnt)] = []
                            wakeUpDictExtended2[str(cnt)].append( float(currentLine[x]) )
                            wakeUpDictExtended2[str(cnt)].append( float(previous_value) )
                            n2 = True
                            wakeUp2.append( float(currentLine[x]) )

                        wakeUp.append( float(currentLine[x]) )
                        wakeUpDictExtended[str(cnt)] = []
                        wakeUpDictExtended[str(cnt)].append( float(currentLine[x]) )
                        wakeUpDictExtended[str(cnt)].append( float(previous_value) )
                        n = True
                    if( currentLine[1] == "fall asleep"):
                        fallASleep.append( float(currentLine[x]) )
                    previous_value = float(currentLine[x])
                    previous_stage = int(currentLine[0])
                else:
                    firstLine = False

            outputFile.write(separator+" Median:"+separator+str( round(np.median(allValues), 5)))
            outputFile.write(separator+" Mean: "+separator+str( round(np.mean(allValues), 5)))
            outputFile.write("\n")

            outputFile.write("Description"+separator+" Above mean"+separator+" Under mean"+separator+" All"+separator+"Above mean %"+separator+"Under mean %\n")
            printBlock(constant, allValues, "constant")
            printBlock(wakeUp, allValues, "wakeUp")
            printBlock(wakeUp2, allValues, "wakeUp2")
            printBlock(fallASleep, allValues, "fallASleep")

            outputFile.write("extended wakeUp"+separator)
            l1 = len( [ max(wakeUpDictExtended[x]) for x in wakeUpDictExtended if max(wakeUpDictExtended[x]) > np.mean(allValues) ] )
            l2 = len( [ max(wakeUpDictExtended[x]) for x in wakeUpDictExtended if max(wakeUpDictExtended[x]) < np.mean(allValues) ] )
            outputFile.write( str(l1)+separator )
            outputFile.write( str(l2)+separator )
            outputFile.write( str( len( wakeUpDictExtended ) )+separator )
            outputFile.write( str( round( 100/float(len( wakeUpDictExtended )) * l1, 2) ) +separator )
            outputFile.write( str( round( 100/float(len( wakeUpDictExtended )) * l2, 2) ) )
            outputFile.write("\n")

            outputFile.write("extended wakeUp2"+separator)
            l1 = len( [ max(wakeUpDictExtended2[x]) for x in wakeUpDictExtended2 if max(wakeUpDictExtended2[x]) > np.mean(allValues) ] )
            l2 = len( [ max(wakeUpDictExtended2[x]) for x in wakeUpDictExtended2 if max(wakeUpDictExtended2[x]) < np.mean(allValues) ] )
            outputFile.write( str(l1)+separator )
            outputFile.write( str(l2)+separator )
            outputFile.write( str( len( wakeUpDictExtended2 ) )+separator )
            outputFile.write( str( round( 100/float(len( wakeUpDictExtended2 )) * l1, 2) ) +separator )
            outputFile.write( str( round( 100/float(len( wakeUpDictExtended2 )) * l2, 2) ) )
            outputFile.write("\n")
            outputFile.write("\n")



        for x in [2,3,6,7]:
            name = ""
            if x == 2:
                name = "audio_means"
            if x == 3:
                name = "audio_max"
            if x == 6:
                name = "acceleration_means"
            if x == 7:
                name = "acceleration_max"
            outputFile.write(name+separator)
            printValues(x)


#Data Format
# sleep_stage  change_classifier   audio_means     audio_max   audio_count     acceleration_count  acceleration_means  acceleration_max
# 0   constant    10.44615879 475 3111    5685    0.120823328 1.225754754
# 0   constant    9.247013239 753 3097    5662    0.07189092  1.369119017
# 0   constant    8.246376812 145 3105    5688    0.054382854 0.190117007
# 0   constant    8.476918075 164 3076    5656    0.055246809 0.205181913
