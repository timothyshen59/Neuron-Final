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
trail_name = sys.argv[1]
starter_csv = sys.argv[2]
#ender_csv = str(trail_name)+"_newer_suggestion"+".csv"
ender_csv = str(starter_csv)+str(super_counter)
while(FINISHED == False and super_counter < 3):
    FINISHED = True
    the_vals = []
    narrow_left = []
    narrow_right = []
    reduce_right = False
    reduce_left = False
    if(super_counter == 0):
        x = open(starter_csv).read().splitlines()
    else:
        x = open(ender_csv).read().splitlines()

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
            

    the_new_lb = []
    the_new_ub = []
    for iq in range(len(the_names)):
        if(super_counter == 0):
            the_new_lb.append(str(the_dictionary_lb[the_names[iq]]))
            the_new_ub.append(str(the_dictionary_ub[the_names[iq]]))
            continue
        """
        if(the_names[iq] != "gSKv3_1bar_SKv3_1_apical"):
            continue
        """
        a = open(the_names[iq]+".txt").read().splitlines()
        for i2 in a:
            if(int(i2) == 0):
                narrow_left.append(int(i2))
                continue
            if(int(i2) == 1 and len(narrow_left) >= 0):
                narrow_left.append(int(i2))
                continue
            if(int(i2) == 18):
                narrow_right.append(int(i2))
                continue
            if(int(i2) == 19 and len(narrow_right) >= 1):
                narrow_right.append(int(i2))
                continue
        if(len(narrow_right) >= 2):
            reduce_right = True
        if(len(narrow_left) >= 2):
            reduce_left = True

        if(reduce_right):
           FINISHED = False
           the_dictionary_ub[the_names[iq]] -= 0.1
           #contracting when last 2 regions violating
        else:
           the_dictionary_ub[the_names[iq]] += 0.1
           #expand when last 2 regions not violating
        if(reduce_left):
            FINISHED = False
            the_dictionary_lb[the_names[iq]] += 0.1
           #contracting when first 2 regions violating
        else:
            the_dictionary_lb[the_names[iq]] -= 0.1
            #expand when first 2 regions not violating

        the_new_lb.append(str(the_dictionary_lb[the_names[iq]]))
        the_new_ub.append(str(the_dictionary_ub[the_names[iq]]))

    f = open(ender_csv, "w")
    f.write('Parameters,LB,UB\n')
    print(the_new_lb)
    print(the_new_ub)
    for i_name in range(len(the_names)):
        f.write(str(the_names[i_name]) + ","+str(the_new_lb[i_name])+","+str(the_new_ub[i_name]))
        if(i_name == (len(the_names)-1)):
            break
        f.write('\n')

    f.close()
    subprocess.run("cat "+str(ender_csv), shell=True)
    #subprocess.run("cp "+str(starter_csv)+" /pscratch/sd/a/asharoff/NEW_DATA_OCT_25_2023/DL4neurons2/unit_params.csv", shell=True)
    subprocess.run("cp "+str(ender_csv)+" /pscratch/sd/a/asharoff/NEW_DATA_OCT_25_2023/DL4neurons2/"+str(ender_csv), shell=True)

    the_result1 = ""
    subprocess.run("rm -rf data_dir_M1", shell=True)
    print("deleted data_dir_M1 Prepping for datagen")
    currentDir = ""
    currentDir = str(os.getcwd())

    os.chdir("./DL4neurons2")
    the_result1 = ""
    the_result1 = subprocess.run('./M1_all_submit.sh '+str(ender_csv), stdout=subprocess.PIPE, universal_newlines=True, shell=True)
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

    subprocess.run("mkdir "+trail_name+str(super_counter), shell=True)
    subprocess.run("cp *.txt "+trail_name+str(super_counter)+"/", shell=True)
    subprocess.run("cp *.png "+trail_name+str(super_counter)+"/", shell=True)
    subprocess.run("cp *.npy "+trail_name+str(super_counter)+"/", shell=True)
    subprocess.run("cp *.csv "+trail_name+str(super_counter)+"/", shell=True)

    subprocess.run("cp /pscratch/sd/a/asharoff/tmp_neuInv/bbp3/L5_TTPC1cADpyr0/"+str(job_id1)+"/out/*.png "+trail_name+str(super_counter)+"/", shell=True)

    print("Finished Analysis prepping for DaCapo")
    if(super_counter == 0):
        FINISHED = False
    super_counter += 1
    break

