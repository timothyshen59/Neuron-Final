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

THE_PATH = "/pscratch/sd/a/asharoff/data_dir_M1_Dom_"

FINISHED = False
super_counter = 0
trail_name = sys.argv[2]
iteration = sys.argv[3]
if(iteration == 0):
    subprocess.run("cp before_automation_unit_params.csv "+trail_name+".csv", shell=True)
while(FINISHED == False and super_counter < 3):
    FINISHED = True
    the_vals = []
    narrow_left = []
    narrow_right = []
    reduce_right = False
    reduce_left = False

    if(iteration == 0):
        x = open(trail_name+".csv").read().splitlines()
    else:
        x = open(trail_name+str(iteration)+".csv").read().splitlines()
    the_names = []
    name = ""
    lb = ""
    ub = ""
    the_dictionary_lb = {}
    the_dictionary_ub = {}

    for i_csv_reader in range(len(x)):
        if(i_csv_reader == 0):
            continue
        else:
            name, lb, ub = x[i_csv_reader].split(',')
            the_names.append(name)
            the_dictionary_lb[name] = float(lb)
            the_dictionary_ub[name] = float(ub)
            

    for iq in range(2):
        if(iteration == 0):
            continue
            break
        """
        if(the_names[iq] != "gSKv3_1bar_SKv3_1_apical"):
            continue
        """
        a = open(sys.argv[1]+".txt").read().splitlines()
        for i2 in a:
            if(int(i2) == 0):
                narrow_left.append(int(i2))
            if(int(i2) == 1 and len(narrow_left) >= 0):
                narrow_left.append(int(i2))
            if(int(i2) == 18):
                narrow_right.append(int(i2))
            if(int(i2) == 19 and len(narrow_right) >= 1):
                narrow_right.append(int(i2))
            if(int(i2) == 19 and len(narrow_right) >= 2):
                reduce_right = True
            if(int(i2) == 3 and len(narrow_left) >= 2):
                reduce_left = True

        if(reduce_right):
           FINISHED = False
           the_dictionary_ub[sys.argv[1]] -= 0.1
           #contracting when last 2 regions violating
        else:
           the_dictionary_ub[sys.argv[1]] += 0.1
           #expand when last 2 regions not violating
        if(reduce_left):
            FINISHED = False
            the_dictionary_lb[sys.argv[1]] += 0.1
           #contracting when first 2 regions violating
        else:
            the_dictionary_lb[sys.argv[1]] -= 0.1
            #expand when first 2 regions not violating

        break

    f = open(trail_name+".csv", "w")
    f.write('Parameters,LB,UB\n')
    print(the_dictionary_ub)
    print(the_dictionary_lb)

    for i_name in range(len(the_names)):
        f.write(str(the_names[i_name]) + ","+str(the_dictionary_lb[sys.argv[1]])+","+str(the_dictionary_ub[sys.argv[1]]))
        if(i_name == (len(the_names)-1)):
            break
        f.write('\n')

    f.close()
    subprocess.run("cat "+trail_name+".csv", shell=True)
    subprocess.run("cp "+trail_name+".csv"+ " /pscratch/sd/a/asharoff/NEW_DATA_OCT_25_2023/DL4neurons2/"+trail_name+".csv", shell=True)

    subproces.run("cp "+trail_name+".csv "+trail_name+str(iteration)+".csv", shell=True)

    the_result1 = ""
    subprocess.run("rm -rf data_dir_M1", shell=True)
    print("deleted data_dir_M1 Prepping for datagen")
    currentDir = ""
    currentDir = str(os.getcwd())

    os.chdir("./DL4neurons2")
    the_result1 = ""
    the_result1 = subprocess.run('./M1_all_submit.sh', stdout=subprocess.PIPE, universal_newlines=True, shell=True)
    the_result1 = str(the_result1.stdout)
    the_array = the_result1.splitlines()
    job_id = str((the_array[len(the_array)-2]))

    while True:
        # Use subprocess to run the squeue command and capture its output
        result = subprocess.run(['squeue', '--format', '%T', '--noheader', '-j', job_id], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result1 = result.stdout.decode().strip()
        print(result1)

        if result.returncode != 0:
            print("Error occurred while checking job status.")
            print(result.stderr)
            break

        # Check if the job is still in the queue
        if result1 == "":
            print("Job", job_id, "has finished.")
            break
    os.chdir(currentDir)
    print("Finished data gen prepping for preprocessing")

    os.chdir("./MLNeuronInverter/packBBP3")
    the_result1 = subprocess.run("shifter --image=nersc/pytorch:ngc-21.08-v2 ./bigPacker.sh "+job_id, shell=True)

    os.chdir(currentDir)
    print("Finished data preprocessing packer prepping for dom")

    os.chdir("./MLNeuronInverter/packBBP3")
    the_result1 = subprocess.run("shifter --image=nersc/pytorch:ngc-21.08-v2 ./bigDom.sh "+job_id, shell=True)
    the_result1 = str(the_result1.stdout)
    the_array = the_result1.splitlines()

    print("Finished data preprocessing dom prepping for ML")
    os.chdir(currentDir)

    currentDir = str(os.getcwd())
    os.chdir("./MLNeuronInverter")

    print("yeh")
    print(str(os.getcwd()))
    the_result1 = subprocess.run('sbatch batchShifter.slr '+ THE_PATH+job_id, stdout=subprocess.PIPE, universal_newlines=True, shell=True)
    print(the_result1.stdout)
    the_result1 = str(the_result1.stdout).split()
    print(the_result1)
    job_id1 = str(the_result1[len(the_result1)-1])
    while True:
        # Use subprocess to run the squeue command and capture its output
        result = subprocess.run(['squeue', '--format', '%T', '--noheader', '-j', job_id1], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result1 = result.stdout.decode().strip()
        print(result1)

        if result.returncode != 0:
            print("Error occurred while checking job status.")
            print(result.stderr)
            break

        # Check if the job is still in the queue
        if result1 == "":
            print("Job", job_id1, "has finished.")
            break


    print("Finished ML prepping for Analysis")

    os.chdir(currentDir)
    subprocess.run("cp /pscratch/sd/a/asharoff/tmp_neuInv/bbp3/L5_TTPC1cADpyr0/"+job_id1+"/the_data.npz /pscratch/sd/a/asharoff/NEW_DATA_OCT_25_2023/the_data.npz",shell=True)
    subprocess.run("shifter --image=nersc/pytorch:ngc-21.08-v2 ./fixed_threshold_mse_version.sh", shell=True)

    subprocess.run("mkdir "+trail_name+str(iteration), shell=True)
    subprocess.run("cp *.txt "+trail_name+str(iteration)+"/", shell=True)
    subprocess.run("cp *.png "+trail_name+str(iteration)+"/", shell=True)
    subprocess.run("cp *.npy "+trail_name+str(iteration)+"/", shell=True)
    subprocess.run("cp *.csv "+trail_name+str(iteration)+"/", shell=True)

    subprocess.run("cp /pscratch/sd/a/asharoff/tmp_neuInv/bbp3/L5_TTPC1cADpyr0/"+str(job_id1)+"/out/*.png "+trail_name+str(iteration)+"/", shell=True)

    print("Finished Analysis prepping for DaCapo")
    if(super_counter == 0):
        FINISHED = False
    super_counter += 1
    break

