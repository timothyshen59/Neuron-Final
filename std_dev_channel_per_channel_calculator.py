import pickle
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from multiprocessing import Pool

NUM_CHANNELS = 19


def parallel(ION_CHANNEL):

    b = np.load("the_data.npz")
    a = []
    for num in range(70000):
        bval1 = b['actual_val'][num][ION_CHANNEL]
        bval2 = b['predicted_val'][num][ION_CHANNEL]
        a.append(bval1-bval2)
    return a
if __name__ == '__main__':

    b = np.load("the_data.npz")
    
    with Pool() as pool:
        result = pool.map(parallel, range(0, NUM_CHANNELS))

    a = np.array([])
    for i in result:
        for az in i:
            a = np.append(a, az)

    std_dev = np.std(a)
    avg = np.average(a)
   
    buckets = []
    the_dictionary = {}
    for i in range(1000):
        the_dictionary[str(i)+"-"+str(i+1)+" away"] = 0
        buckets.append([avg+i*std_dev, avg+(i+1)*std_dev])

    for i in a:
        diff = abs(float(avg-i)/float(-1*std_dev))
        for q in range(len(buckets)):
            if(diff >= buckets[q][0] and diff <= buckets[q][1]):
                the_dictionary[str(q)+"-"+str(q+1)+" away"] += 1
                break

    
    final_dictionary = {}
    x_region = []
    y_val = []
    for key, value in the_dictionary.items():
        if(value > 5):
            x_region.append(key)
            y_val.append(value)
            final_dictionary[key] = value

    print(final_dictionary)
    with open("histogram_data.txt", 'w') as f:
        f.write(str(final_dictionary))

    plt.figure(figsize=(40,20))
    plt.bar(x_region, y_val, tick_label = x_region, width=0.4, color=['blue'])
    plt.ylim(0, 4000)
    plt.xlabel('Standard Deviation')
    plt.ylabel('Number of data points at this Standard Deviation')
    plt.title('Standard Deviation vs Count for all ION CHANNELS COMBINED ')
    plt.savefig("STD_DEV_VS_COUNT.png")
    y_value = []
    

