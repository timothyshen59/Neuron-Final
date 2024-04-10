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
    the_list = []
    x_region= []

    for key in region_val["channel"+str(ION_CHANNEL)]:
        x_region.append(str(region_dictionary[key]))
    for zz in range(NUM_REGIONS):
        the_list.append(np.std(region_val["channel"+str(ION_CHANNEL)]["Region "+str(zz)]))

    the_lister = ["gNaTs2_tbar_NaTs2_t_apical", "gSKv3_1bar_SKv3_1_apical","gImbar_Im_apical","gIhbar_Ih_dend", "gNaTa_tbar_NaTa_t_axonal", "gK_Tstbar_K_Tst_axonal", "gNap_Et2bar_Nap_Et2_axonal", "gSK_E2bar_SK_E2_axonal", "gCa_HVAbar_Ca_HVA_axonal", "gK_Pstbar_K_Pst_axonal","gCa_LVAstbar_Ca_LVAst_axonal", "g_pas_axonal", "cm_axonal", "gSKv3_1bar_SKv3_1_somatic","gNaTs2_tbar_NaTs2_t_somatic", "gCa_LVAstbar_Ca_LVAst_somatic", "g_pas_somatic", "cm_somatic", "e_pas_all"]

    y_value = the_list
    plt.figure(figsize=(25,25))
    plt.ylim(0, 4000)
    print(x_region)
    print(y_value)
    plt.bar(x_region, y_value, tick_label = x_region, width=0.5, color=['blue'])
    plt.xlabel('Region')
    plt.ylabel('STD DEV Value')
    plt.title('STD Dev on Region basis for ION_CHANNEL '+the_lister[ION_CHANNEL])
    plt.savefig('ION_CHANNEL_STD_DEV_REGION_BY_REGION_CHANNEL_'+the_lister[ION_CHANNEL]+'.png')
    
