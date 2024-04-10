import pickle
import pandas as pd
import matplotlib.pyplot as plt

ION_CHANNEL = 19
NUM_REGIONS = 20
ROUNDING = 1
global delta_region 
delta_region = float(2.0/NUM_REGIONS)


global region_dictionary
region_dictionary = {}

temp = 0
other_temp = 0
x_region = []
x_other_region = []

for i in range(NUM_REGIONS):
    if(i==0):
        temp = -1.0
        other_temp = float(temp)

    other_temp += delta_region
    other_temp = round(other_temp, ROUNDING)
    region_dictionary["Region "+str(i)] = [temp, other_temp]
    x_region.append(temp)
    x_other_region.append(other_temp)
    temp = round(other_temp,1)

#print(region_dictionary)
the_lister = ["gNaTs2_tbar_NaTs2_t_apical", "gSKv3_1bar_SKv3_1_apical","gImbar_Im_apical","gIhbar_Ih_dend", "gNaTa_tbar_NaTa_t_axonal", "gK_Tstbar_K_Tst_axonal", "gNap_Et2bar_Nap_Et2_axonal", "gSK_E2bar_SK_E2_axonal", "gCa_HVAbar_Ca_HVA_axonal", "gK_Pstbar_K_Pst_axonal","gCa_LVAstbar_Ca_LVAst_axonal", "g_pas_axonal", "cm_axonal", "gSKv3_1bar_SKv3_1_somatic","gNaTs2_tbar_NaTs2_t_somatic", "gCa_LVAstbar_Ca_LVAst_somatic", "g_pas_somatic", "cm_somatic", "e_pas_all"]
for i in range(ION_CHANNEL):
    loaded_dict = {}
    with open('saved_bar_chart_1_cumulative_error'+str(i)+'.pkl', 'rb') as f:
        loaded_dict = pickle.load(f)

    zf = []
    y_value = []
    
    
    print(the_lister[i])
    #print(loaded_dict)
    temp = {}
    for key, value in loaded_dict.items():
        #temp = dict({"Region": [], "value": []})
        for k,v in value.items():
            #temp["Region"].append(k)
            #temp["value"].append(abs(v))
            y_value.append(abs(v))

    print(y_value)
    plt.figure(figsize=(25,25))
    plt.ylim(0, 4000)
    plt.bar(x_region, y_value, tick_label = x_region, width=0.05, color=['red'])
    plt.xlabel('Region')
    plt.ylabel('Cummulative Error')
    plt.title('Cummulative Error for ION Channel '+the_lister[i] + " v2")
    plt.savefig('ION_CHANNEL_'+the_lister[i]+'.png')
    y_value = []
    
