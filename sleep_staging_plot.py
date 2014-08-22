import matplotlib.pyplot as plt
import datetime
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import dates
import numpy as np
import json
import re
import math
import time
import collections
import itertools

plt.close('all')

vp_number = 30
# smartphone_position = "_mattrass"
smartphone_position = "_right_arm"
current_folder = "result_data_vp"+str(vp_number)+smartphone_position+"/"

sleep_stage_file = open("sleep_staging_files/VP"+str(vp_number)+"_NAP.TXT", "r")
acceleration_value_file = open(current_folder+"result_acceleration", "r")
audio_value_file = open(current_folder+"result_audio", "r")

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

previous_vector = [0,0,0]
previous_audio_vector = 0
date_and_distance = []


def calculate_distance(vec1, vec2):
    return math.sqrt( math.pow( (vec1[0]-vec2[0]), 2) + math.pow( (vec1[1]-vec2[1]), 2) + math.pow( (vec1[2]-vec2[2]), 2) )

# def get_closest_timestamp(time_stamp):
#     l = ordered_dict.keys()
#     return min(l, key=lambda x:abs( float(x) - time_stamp ))

ordered_audio_dict = collections.OrderedDict()
ordered_dict = collections.OrderedDict()
ordered_dict_start = collections.OrderedDict()

for x in audio_json_data:
    ordered_audio_dict[ x[0] ] = x[1]

for x in acceleration_json_data:
    key = x.keys()[0]
    vec1 = x[key]
    distance = calculate_distance( vec1, previous_vector )
    if(distance > 0.0):
        ordered_dict[key] = distance
        previous_vector = vec1


keys = ordered_dict.keys()
first_timestamp = min(keys, key=lambda x:abs( float(x) - current_timestamp ))


for x in list(itertools.dropwhile(lambda k: k!= first_timestamp, ordered_dict.iterkeys() )) :
    if(ordered_dict[x] > 0.1):
        ordered_dict_start[x] = ordered_dict[x]


def plot_audio_data( current_x, data_length, idx ):
    global current_audio_timestamp
    keys = ordered_audio_dict.keys()

    # # get closest timestamp from audio peak timestamp
    current_audio_timestamp = min(keys, key=lambda x:abs( float(x) - float(timestamps[idx]) )) 
    initial_timestamp = current_audio_timestamp

    for x in list(itertools.dropwhile(lambda k: k != initial_timestamp, ordered_audio_dict.iterkeys() )) :
        if( initial_timestamp != starting_timestamp ):
            if( float(x) < float(initial_timestamp) + 30 and float(x) > float(initial_timestamp) ):
                if ordered_audio_dict[x] > 0.0:
                    value = ordered_audio_dict[x] / 32768.0
                    current_audio_timestamp = float(x)
                    plt.axhline( y=(value+1)*-1 , xmin=current_x/data_length, xmax=(current_x+1.0)/data_length , color="r", linewidth=2.0 )
        else:
            if( float(x) < float(initial_timestamp) + (30 - int(marker_starting_point)) and float(x) > float(initial_timestamp) ):
                if ordered_audio_dict[x] > 0.0:
                    value = ordered_audio_dict[x] / 32768.0
                    current_audio_timestamp = float(x)

    current_audio_timestamp = initial_timestamp + 30
    return


def plot_accelerometer_data( current_x, data_length, idx ):
    global current_timestamp
    keys = ordered_dict_start.keys()

    print(current_x)
    # get closest timestamp from audio peak timestamp
    current_timestamp = min(keys, key=lambda x:abs( float(x) - float(timestamps[idx]) )) 
    initial_timestamp = current_timestamp

    for x in list(itertools.dropwhile(lambda k: k != initial_timestamp, ordered_dict_start.iterkeys() )) :
        if( initial_timestamp != starting_timestamp ):
            if( float(x) < float(initial_timestamp) + 30 and float(x) > float(initial_timestamp) ):
                if ordered_dict_start[x] > 0.12:
                    current_timestamp = float(x)
                    plt.axhline( y=(ordered_dict_start[x]+1)*-2 , xmin=current_x/data_length, xmax=(current_x+1.0)/data_length , color="g", linewidth=2.0 )
        else:
            if( float(x) < float(initial_timestamp) + (30 - int(marker_starting_point)) and float(x) > float(initial_timestamp) ):
                if ordered_dict_start[x] > 0.12:
                    current_timestamp = float(x)
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




for value in data:
    print( str(i) +"from "+ str(len(data)) )

    # TODO extract method
    if( int(value) == sleep_value ):
        value = 0

    if value != previous_value:
        if(int(value) != rem_value):
            plt.axvline(x=float(current_x), ymin=(float(previous_value)+ compensate)/overall_height, ymax=( ( float(value)+ compensate)/overall_height ) )
        else:
            plt.axvline(x=float(current_x), ymin=(float(previous_value)+ compensate)/overall_height, ymax=( ( (float(value)+ compensate)/overall_height ) - rem_phase_adjustment )) 
    
    if(int(value) != rem_value):
        plt.axhline( y=float(value), xmin=current_x/ len(data), xmax=(current_x+growth_x)/ len(data), color='b', linewidth=2.0 )
    else:
        plt.axhline( y=float(value), xmin=current_x/ len(data), xmax=(current_x+growth_x)/ len(data), color='#7F00FF', linewidth=8.0 )

    if(int(value) != rem_value):
        previous_value = value
    else:
        previous_value = rem_value - rem_phase_adjustment

    plot_accelerometer_data( current_x, max_x, i )
    plot_audio_data( current_x, max_x, i )

    i+=1

    current_x += growth_x


print( "Execution Time: " + str( time.time() - time_t) )
plt.axis([min_x,max_x,min_y,max_y])

plt.show()