import numpy as np
import json
from itertools import product
from functools import partial
from multiprocessing import Pool, Process
import os
import pickle
import sys
#import matplotlib.pyplot as plt
import subprocess
import time
 
starter_csv = sys.argv[1]
ender_csv = sys.argv[2]

x = open(starter_csv).read().splitlines()
  
the_names = []
name = ""
lb = ""
ub = ""
the_dictionary_lb = {}
the_dictionary_ub = {}
the_dictionary_lb_mod = {}
the_dictionary_ub_mod = {}  
for i_csv_reader in range(len(x)):
    if(i_csv_reader == 0):
        continue
    else:
        name, lb, ub = x[i_csv_reader].split(',')
        the_names.append(name)
        the_dictionary_lb[name] = float(lb)
        the_dictionary_ub[name] = float(ub)

the_numbers = []
lb_reduce = []
ub_reduce = []
done_lower = False
done_upper = False
for i in the_names:
    lb_reduce = []
    ub_reduce = []
    with open(i+".txt") as file:
        print(i)
        the_numbers = file.readlines()
        the_numbers = [eval(il) for il in the_numbers]
        the_numbers.sort()
        for ix in range(len(the_numbers)):
            if(the_numbers[ix] == 0):
                lb_reduce.append(the_numbers[ix])
                continue
            elif(done_lower == False and the_numbers[ix] == (lb_reduce[ix-1])+1):
                lb_reduce.append(the_numbers[ix])
                continue
            elif(done_lower == False and the_numbers[ix] != (lb_reduce[ix-1]+1)):
                break

        the_numbers.sort(reverse = True)
        for ix2 in range(len(the_numbers)):
            if(the_numbers[ix2] == 19):
                ub_reduce.append(the_numbers[ix2])
                continue
            elif(ix2 == 0 and len(ub_reduce) == 0):
                break
            elif(done_upper == False and the_numbers[ix2] == (ub_reduce[ix2-1])-1):
                ub_reduce.append(the_numbers[ix2])
                continue
            elif(done_lower == False and the_numbers[ix2] != (ub_reduce[ix2-1]-1)):
                break

        the_dictionary_ub_mod[i] = the_dictionary_ub[i] - (float(len(ub_reduce)*0.1)/float(2))*(float(the_dictionary_ub[i])-float(the_dictionary_lb[i]))
        the_dictionary_lb_mod[i] = the_dictionary_lb[i] + (float(len(lb_reduce)*0.1)/float(2))*(float(the_dictionary_ub[i])-float(the_dictionary_lb[i]))

print(the_dictionary_ub_mod)
f = open(ender_csv, "w")
f.write('Parameters,LB,UB\n')
for i_name in range(len(the_names)):
    f.write(str(the_names[i_name]) + ","+str(the_dictionary_lb_mod[the_names[i_name]])+","+str(the_dictionary_ub_mod[the_names[i_name]]))
    if(i_name == (len(the_names)-1)):
        break
    f.write('\n')



           



