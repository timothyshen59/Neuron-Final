import pickle
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from multiprocessing import Pool
import ast

f = open("All_Errror_Interval_vs_Count.txt", "r")
x_region = ast.literal_eval(f.readline())
y_region = ast.literal_eval(f.readline())
x_reg = []
y_val = []

the_total = 0
for i in y_region:
    the_total += i

counter = 0
for i in range(len(x_region)):
    counter = 0
    x_reg.append(str(x_region[i]))
    temp = ast.literal_eval(x_region[i])
    for q in range(len(x_region)):
        tmp = ast.literal_eval(x_region[q])
        if(tmp[0] > temp[0]):
            counter += y_region[q]
            continue

    print(counter)
    y_val.append((float(counter)/float(the_total))*100)


plt.figure(figsize=(20,20))
plt.rcParams.update({'font.size':40})
plt.ylim(0, 100)
plt.bar(x_reg, y_val, tick_label = x_reg, width=0.4, color=['blue'])
plt.xlabel('Error Interval')
plt.ylabel('Count')
plt.title('Error Interval vs Count for all ION CHANNELS COMBINED ')
plt.savefig("All_Error_Interval_vs_Count.png")
y_value = []
    

