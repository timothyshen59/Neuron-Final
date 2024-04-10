import pickle
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from multiprocessing import Pool

NUM_CHANNELS = 19
RANGES = 10

def parallel(ION_CHANNEL):

    b = np.load("the_data.npz")
    a = []
    for num in range(70000):
        bval1 = b['actual_val'][num][ION_CHANNEL]
        bval2 = b['predicted_val'][num][ION_CHANNEL]
        a.append(bval1-bval2)
    return a

def parallel_2(arg):
    print(arg[1])
    count = 0
    for i in range(len(a)):
        if(a[i] >= arg[1][0] and a[i] <= arg[1][1]):
            count += 1

    return count
            

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
    the_min = np.min(a)
    the_max = np.max(a)
    the_range = float(the_max)-float(the_min)
    #the_stepping = float(the_range)/float(RANGES)
    the_stepping = std_dev

    counter = 0
    x_region = []
    intervals = []
    while(counter <= the_max+the_stepping):
        if(counter == 0):
            intervals.append([the_min, the_min+the_stepping])
            counter += the_min+the_stepping
            counter += 1
            continue

        intervals.append([counter, counter+the_stepping])
        counter += the_stepping
    

    the_args = []
    for i in range(len(intervals)):
        the_args.append([list(a), intervals[i]])

    with Pool() as pool:
        result = pool.map(parallel_2, [i for i in the_args])

    for i in intervals:
        x_region.append(str(i))

    y_val = result


    plt.figure(figsize=(140,20))
    plt.rcParams.update({'font.size':40})
    plt.yscale("log")
    plt.bar(x_region, y_val, tick_label = x_region, width=0.4, color=['blue'])
    plt.xlabel('Error Interval')
    plt.ylabel('Count')
    plt.title('Error Interval vs Count for all ION CHANNELS COMBINED ')
    plt.savefig("All_Error_Interval_vs_Count.png")
    y_value = []
    

    f = open("All_Errror_Interval_vs_Count.txt", "w")
    f.write(str(x_region)+"\n")
    f.write(str(y_val)+"\n")
    f.close()
    

