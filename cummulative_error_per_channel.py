import numpy as np
from itertools import product
from functools import partial
from multiprocessing import Pool, Process
import pickle
import sys

b = np.load("the_data.npz")
arr_errors = []

actual_val = []
predicted_val = []

DELTA = 0
#NUM_CHANNELS = 19
ION_CHANNEL = int(sys.argv[1])
NUM_REGIONS = 20
ROUNDING = 1

region_val = {}
##for i in range(NUM_CHANNELS):
#    actual_val.append([])
#    predicted_val.append([])
#    arr_errors.append([])
#    region_val["channel"+str(i)] = {}
region_val["channel"+str(ION_CHANNEL)] = {}

global delta_region 
delta_region = float(2.0/NUM_REGIONS)

global region_dictionary
region_dictionary = {}

temp = 0
other_temp = 0
for i in range(NUM_REGIONS):
    if(i==0):
        temp = -1.0
        other_temp = float(temp)

    other_temp += delta_region
    other_temp = round(other_temp, ROUNDING)
    region_dictionary["Region "+str(i)] = [temp, other_temp]
    temp = round(other_temp,1)

#for i in range(NUM_CHANNELS):
for i in range(1):
    for q in range(NUM_REGIONS):
        region_val["channel"+str(ION_CHANNEL)]["Region "+str(q)] = [] 


def parallelize(qq, num, bval1, bval2):
    if(abs(bval1 - bval2) > DELTA):
        for key, value in region_dictionary.items():
            if(bval1 >= value[0] and bval1 <= value[1]):
                region_val["channel"+str(qq)][key].append((bval1, abs(bval1 - bval2)))
        return abs(bval1-bval2)
    else:
        return 0

if __name__ == '__main__':

    a = np.array([])
    b1 = np.array([])
    counter = 0
    for num in range(70000):
        the_list = []
        lister = []

        #for i in range(NUM_CHANNELS):
        print(b['actual_val'][0][0])
        bval1 = b['actual_val'][num][ION_CHANNEL]
        bval2 = b['predicted_val'][num][ION_CHANNEL]

        if(abs(bval1 - bval2) > DELTA):
            counter += 1
            a = np.append(a, bval1)
            b1 = np.append(b1, (bval1-bval2))

            #the_list.append(Process(target=parallelize, args=(i, num, bval1, bval2)))
            #the_list[i].start()
        parallelize(ION_CHANNEL, num, bval1, bval2)

        #for i in range(NUM_CHANNELS):
        #    lister.append(the_list[i].join())

        #for i in lister:
        #    if(i == 0):
        #        counter += 1
        #        continue
        #    else:
        #       #region_val["channel"+str(qq)][key].append((bval1, bval1 - bval2))
        #        arr_errors[counter].append(i)
        #        counter += 1

    std_dev = np.std(b1)
    average = np.average(b1)
    

    cum_error = {}
    error = 0
    for i in range(1):
        cum_error["ion channel "+str(ION_CHANNEL)] = {}
        for zz in range(NUM_REGIONS):
            for iz in region_val["channel"+str(ION_CHANNEL)]["Region "+str(zz)]:
                error += iz[1]

            cum_error["ion channel "+str(ION_CHANNEL)]["Region"+str(zz)] = error
            error=0

    with open('saved_bar_chart_1_cumulative_error'+str(ION_CHANNEL)+'.pkl', 'wb') as f:
        pickle.dump(cum_error, f)

    with open('saved_line_chart_1'+str(ION_CHANNEL)+'.pkl', 'wb') as f:
        pickle.dump(region_val, f)

    with open("STD_DEV_"+str(ION_CHANNEL)+".txt", "w") as fz:
           fz.write(str(average))

    np.savez_compressed(str(ION_CHANNEL)+("_the_errors")+".npz", x=b1)
    print("here")
