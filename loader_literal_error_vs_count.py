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
for i in range(len(y_region)):
    if(int(y_region[i]) > 5):
        x_reg.append(str(x_region[i]))
        y_val.append(y_region[i])
        continue


print(len(x_reg))
print(len(y_val))
plt.figure(figsize=(140,20))
plt.rcParams.update({'font.size':40})
plt.yscale("log")
plt.bar(x_reg, y_val, tick_label = x_reg, width=0.4, color=['blue'])
plt.xlabel('Error Interval')
plt.ylabel('Count')
plt.title('Error Interval vs Count for all ION CHANNELS COMBINED ')
plt.savefig("All_Error_Interval_vs_Count.png")
y_value = []
    

