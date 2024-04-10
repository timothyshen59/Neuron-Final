import numpy as np
import json
from itertools import product
from functools import partial
from multiprocessing import Pool, Process
import pickle
import sys
import matplotlib.pyplot as plt

arr_overall = {}
ION_CHANNELS = 19
NUM_REGIONS = 20
ROUNDING = 1
global delta_region 
delta_region = float(2.0/NUM_REGIONS)

temp = 0
other_temp = 0
x_region = []
region_dictionary = {}
for i in range(NUM_REGIONS):
    if(i==0):
        temp = -1.0
        other_temp = float(temp)

    other_temp += delta_region
    other_temp = round(other_temp, ROUNDING)
    region_dictionary["Region "+str(i)] = [temp, other_temp]
    temp = round(other_temp,1)
    x_region.append(str(region_dictionary["Region "+str(i)]))

for i in range(ION_CHANNELS):
    arr_overall["Channel"+str(i)] = np.load(str(i)+"_absolute.npy")

the_numerator = 0
the_denom = 0
thresh = 0
violating = 0
non = 0
total = 0
found = False


while(found == False and thresh < 20):
    total = 0
    violating = 0
    non = 0
    for key, value in arr_overall.items():
        for iq in value:
            if(iq > thresh):
                violating += iq
            else:
                non += iq
            total += iq

    if((float(violating)/float(total))*100 >= 24.5 and (100*float(violating)/float(total) <= 25.5)):
        print(float(violating)/float(total)*100)
        found = True
        break
    thresh += 0.001

print(thresh)

the_lister = ["gNaTs2_tbar_NaTs2_t_apical", "gSKv3_1bar_SKv3_1_apical","gImbar_Im_apical","gIhbar_Ih_dend", "gNaTa_tbar_NaTa_t_axonal", "gK_Tstbar_K_Tst_axonal", "gNap_Et2bar_Nap_Et2_axonal", "gSK_E2bar_SK_E2_axonal", "gCa_HVAbar_Ca_HVA_axonal", "gK_Pstbar_K_Pst_axonal","gCa_LVAstbar_Ca_LVAst_axonal", "g_pas_axonal", "cm_axonal", "gSKv3_1bar_SKv3_1_somatic","gNaTs2_tbar_NaTs2_t_somatic", "gCa_LVAstbar_Ca_LVAst_somatic", "g_pas_somatic", "cm_somatic", "e_pas_all"]
counter = 0

bars = plt.subplots(ION_CHANNELS)

the_overall_dictionary = {}
for key, value in arr_overall.items():
    violating = []
    non_violating = []
    the_right = 0
    the_left = 0
    the_total = 0
    for iz in range(value.size):
        if(value[iz] > thresh):
            if(iz > (value.size/2)):
                the_right += 1
            else:
                the_left += 1
            violating.append(iz)
        else:
            non_violating.append(iz)
        the_total += 1

    plt.figure(figsize=(15,15))
    plt.ylim(0, 1)
    bars = plt.bar(x_region, value, tick_label = x_region, width=0.5, color=['blue'])

    the_overall_dictionary[the_lister[counter]] = []
    if(len(violating)/float(total) > 0.7):
        the_overall_dictionary[lister[counter]].append("fixed")
    elif(len(violating)/float(total) < 0.3):
        the_overall_dictionary[the_lister[counter]].append("expand")
    if(the_left < 3):
        the_overall_dictionary[the_lister[counter]].append("expand left")
    if(the_right < 3):
        the_overall_dictionary[the_lister[counter]].append("expand right")


    the_right = []
    the_left = []
    for qz in range(len(violating)):
        bars[violating[qz]].set_color('red')

    plt.xlabel('Region')
    plt.ylabel('Absolute Avg Error')
    plt.title('Absolute AVG Error vs Region with Threshold '+the_lister[counter])
    plt.savefig('Absolute_AVG_ION_CHANNEL_'+the_lister[counter]+'_25'+'.png')

    counter += 1

expanded = 0
fixed = 0
expanded_right = 0
expanded_left = 0
f = open("25_absolute.txt", "w")
for key, value in the_overall_dictionary.items():
    f.write(str(key)+"\n")
    f.write(str(value)+"\n")
    for i in value:
        if(i == "fixed"):
            fixed += 1
        elif(i == "expand"):
            expanded += 1
        elif(i == "expanded right"):
            expanded_right += 1
        else:
            expanded_left += 1

f.write("Summary"+"\n")
f.write("expanded: "+str(expanded)+"\n")
f.write("fixed: "+str(fixed)+"\n")
f.write("expanded right: "+str(expanded_right)+"\n")
f.write("expanded left: "+str(expanded_left)+"\n")
