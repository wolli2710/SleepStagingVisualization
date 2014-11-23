import datetime
from matplotlib import dates
import numpy as np
import json
import re
import math
import time
import collections
import itertools

positions = ["_right_arm", "_mattrass"]

for vp_number in range(26, 32):
    for smartphone_position in positions:

        current_folder = "result_data_vp"+str(vp_number)+smartphone_position+"/"

        sleep_stage_file = open("sleep_staging_files/VP"+str(vp_number)+"_NAP.TXT", "r")
        acceleration_value_file = open(current_folder+"result_acceleration", "r")
        audio_value_file = open(current_folder+"result_audio", "r")

        output_file = open(str(current_folder)+"VP"+str(vp_number)+smartphone_position+"_30sec_chunks.csv", "w")

        content = ""
        with open("marker_files/timestamp_and_marker_"+str(vp_number)+".txt", "r") as volume_peak_timestamp_file:
            content = volume_peak_timestamp_file.readlines()

        volume_peak_timestamp = float(content[0]) / 1000.0
        marker_index = int(content[1])

        marker_starting_point = (marker_index / 500)
        print("Marker_starting_point "+ str(marker_starting_point))

        current_timestamp = volume_peak_timestamp
        current_audio_timestamp = current_timestamp
        starting_timestamp = current_timestamp

        # prepare data of sleepstaging file
        data = [re.sub('\D','',x.split("\t")[1]) for x in sleep_stage_file]
        t_stamp = starting_timestamp
        timestamps = []
        for x in range(0,len(data)):
            t_stamp+=30.0
            timestamps.append( t_stamp )

        acceleration_json_data = json.load( acceleration_value_file )
        audio_json_data = json.load( audio_value_file )

        print( "JSON-len"+ str(len(acceleration_json_data)) )


        previous_vector = [0,0,0]
        previous_audio_vector = 0
        date_and_distance = []


        def calculate_distance(vec1, vec2):
            return math.sqrt( math.pow( (vec1[0]-vec2[0]), 2) + math.pow( (vec1[1]-vec2[1]), 2) + math.pow( (vec1[2]-vec2[2]), 2) )

        ordered_audio_dict = collections.OrderedDict()
        ordered_dict = collections.OrderedDict()
        ordered_dict_start = collections.OrderedDict()

        for x in audio_json_data:
            ordered_audio_dict[ x[0] ] = x[1]

        cnt = 0
        for x in acceleration_json_data:
            cnt += 1
            key = x.keys()[0]
            vec1 = x[key]
            distance = calculate_distance( vec1, previous_vector )
            if(distance > 0.0):
                ordered_dict[str(key)] = distance
                previous_vector = vec1


        keys = ordered_dict.keys()
        first_timestamp = min(keys, key=lambda x:abs( float(x) - current_timestamp ))


        for x in list(itertools.dropwhile(lambda k: k!= first_timestamp, ordered_dict.iterkeys() )) :
            ordered_dict_start[x] = ordered_dict[x]


        def plot_audio_data( current_x, data_length, idx ):
            global current_audio_timestamp
            keys = ordered_audio_dict.keys()

            # # get closest timestamp from audio peak timestamp
            current_audio_timestamp = min(keys, key=lambda x:abs( float(x) - float(timestamps[idx]) ))
            initial_timestamp = current_audio_timestamp

            valueList = []
            cnt = 0
            for x in list(itertools.dropwhile(lambda k: k != initial_timestamp, ordered_audio_dict.iterkeys() )) :
                if( initial_timestamp != starting_timestamp ):
                    if( float(x) < float(initial_timestamp) + 30 and float(x) > float(initial_timestamp) ):
                        cnt += 1
                        value = ordered_audio_dict[x]
                        current_audio_timestamp = float(x)
                        valueList.append(value)
                else:
                    if( float(x) < float(initial_timestamp) + (30 - int(marker_starting_point)) and float(x) > float(initial_timestamp) ):
                        current_audio_timestamp = float(x)

            output_file.write( str(np.mean(valueList))+"," )
            output_file.write( str(np.amax(valueList))+"," )
            output_file.write( str(cnt)+"," )
            current_audio_timestamp = initial_timestamp + 30
            return


        def plot_accelerometer_data( current_x, data_length, idx ):
            global current_timestamp
            keys = ordered_dict_start.keys()

            # get closest timestamp from audio peak timestamp
            current_timestamp = min(keys, key=lambda x:abs( float(x) - float(timestamps[idx]) ))
            initial_timestamp = current_timestamp

            cnt = 0
            valueList = []
            for x in list(itertools.dropwhile(lambda k: k != initial_timestamp, ordered_dict_start.iterkeys() )) :
                if( initial_timestamp != starting_timestamp ):
                    if( float(x) < float(initial_timestamp) + 30 and float(x) > float(initial_timestamp) ):
                        current_timestamp = float(x)
                        cnt += 1
                        valueList.append(ordered_dict_start[x])
                else:
                    if( float(x) < float(initial_timestamp) + (30 - int(marker_starting_point)) and float(x) > float(initial_timestamp) ):
                      current_timestamp = float(x)
            output_file.write( str(cnt)+"," )
            output_file.write( str(np.mean(valueList))+"," )
            output_file.write( str(np.amax(valueList))+"\n" )
            return

        previous_value=0
        current_x=0.0
        growth_x=1.0
        rem_phase_adjustment = 0
        rem_value = 5
        sleep_value = 6

        max_x = len(data)
        max_y = 6
        min_x = 0
        min_y = -5
        compensate = math.fabs(min_y)
        overall_height = max_y + compensate

        i = 0
        time_t = time.time()


        output_file.write("sleep_stage, change_classifier, audio_means, audio_max, audio_count, acceleration_count, acceleration_means, acceleration_max\n")
        for value in data:
            print( str(i) +"from "+ str(len(data)) )

            if( int(value) == sleep_value ):
                value = 0

            output_file.write(str(value)+",")

            print("value: "+str(value)+" prev:"+str(previous_value))
            if int(value) > int(previous_value):
                print("fall_asleep")
                output_file.write("fall asleep,")
            if int(value) < int(previous_value):
                print("wakeup")
                output_file.write("wake up,")
            if int(value) == int(previous_value):
                print("constant")
                output_file.write("constant,")
           
            previous_value = value
            plot_audio_data( current_x, max_x, i )
            plot_accelerometer_data( current_x, max_x, i )
            i+=1
            current_x += growth_x

        print( "Execution Time: " + str( time.time() - time_t) )