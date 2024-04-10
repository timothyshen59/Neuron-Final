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


for i in range(ION_CHANNEL):
    with open('saved_bar_chart_1_cumulative_error'+str(i)+'.pkl', 'rb') as f:
        loaded_dict = pickle.load(f)

    zf = []
    y_value = []

    for key, value in loaded_dict.items():
        temp = dict({"Region": [], "value": []})
        for k,v in value.items():
            temp["Region"].append(k)
            temp["value"].append(abs(v))
            y_value.append(abs(v))

    plt.bar(x_region, y_value, tick_label = x_region, width=0.07, color=['red'])
    plt.ylim(0, 4000)
    plt.xlabel('Region')
    plt.ylabel('Cummulative Error')
    plt.title('Cummulative Error for ION Channel '+str(i))
    print('ION_CHANNEL_'+str(i)+'.png')
    plt.savefig('ION_CHANNEL_'+str(i)+'.png')
    
