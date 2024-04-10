import numpy as np
from itertools import product
from functools import partial
from multiprocessing import Pool, Process
import pickle
import matplotlib.pyplot as plt
import sys

b = np.load("the_data.npz")
arr_errors = []

actual_val = []
predicted_val = []

DELTA = 0
#NUM_CHANNELS = 19
ION_CHANNEL = 19
NUM_REGIONS = 20
ROUNDING = 1
##for i in range(NUM_CHANNELS):
#    actual_val.append([])
#    predicted_val.append([])
#    arr_errors.append([])
#    region_val["channel"+str(i)] = {}

global delta_region 
delta_region = float(2.0/NUM_REGIONS)

global region_dictionary
region_dictionary = {}
region_val = {}
#for i in range(NUM_CHANNELS):

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
for i in range(ION_CHANNEL):
    region_val["channel"+str(i)] = {}

for i in range(ION_CHANNEL):
    for q in range(NUM_REGIONS):
        region_val["channel"+str(i)]["Region "+str(q)] = [] 


def parallelize(qq, num, bval1, bval2):
    if(abs(bval1 - bval2) > DELTA):
        for key, value in region_dictionary.items():
            if(bval1 >= value[0] and bval1 <= value[1]):
                region_val["channel"+str(qq)][key].append((bval1, abs(bval1 - bval2)))
        return abs(bval1-bval2)
    else:
        return 0

def the_main(ION_CHANNEL):
    a = np.array([])
    b1 = np.array([])
    counter = 0
    b = np.load("the_data.npz")
    for num in range(70000):
        the_list = []
        lister = []

        bval1 = b['actual_val'][num][ION_CHANNEL]
        bval2 = b['predicted_val'][num][ION_CHANNEL]

        if(abs(bval1 - bval2) > DELTA):
            counter += 1
            a = np.append(a, bval1)
            b1 = np.append(b1, (bval1-bval2))

        parallelize(ION_CHANNEL, num, bval1, bval2)

    return region_val


if __name__ == '__main__':
    b = np.load("the_data.npz")
    pool = Pool()
    z = pool.map(the_main, range(0,ION_CHANNEL))
    x_region = []
    y_val = {}
    counter = 0
    for i in z:
        for key, value in i.items():
            for key1, value1 in value.items():
                if(counter == 0):
                    x_region.append(key1)
                    y_val[key1] = []
                    if(len(value1) > 0):
                        y_val[key1].append(value1)
                else:
                    if(len(value1) > 0):
                        y_val[key1].append(value1)
            counter += 1

    print(y_val)
    the_listerz = np.array([])
    x_region = []
    y_valz = []
    for key, value in y_val.items():
        the_listerz = np.array([])
        x_region.append(str(region_dictionary[key]))
        print(key)
        for qq in value:
            the_listerz = np.append(the_listerz, qq[0][1])
        y_valz.append(the_listerz.std())
            

    print(x_region)
    print(y_valz)
    plt.bar(x_region, y_valz, tick_label = x_region, width=0.4, color=['blue'])
    plt.xlabel('Region Value')
    plt.ylabel('STD Dev at Region')
    plt.title('Standard Deviation vs Region for all ION CHANNELS')
    plt.savefig("STD_DEV_VS_Region_all_ION_CHANNELS"+".png")
    


