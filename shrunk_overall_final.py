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

THE_PATH = "/pscratch/sd/t/timshen/data_dir_M1_Dom_"

FINISHED = False
super_counter = 0
trail_name = sys.argv[1]
starter_csv = sys.argv[2]
that_param = sys.argv[3]
#ender_csv = str(trail_name)+"_newer_suggestion"+".csv"
#ender_csv = str(starter_csv)+str(super_counter)
while(FINISHED == False and super_counter < 3):
    """
    the_result1 = ""
    subprocess.run("rm -rf data_dir_M1", shell=True)
    print("deleted data_dir_M1 Prepping for datagen")
    """
    currentDir = ""
    currentDir = str(os.getcwd())
    subprocess.run("cp "+starter_csv+" DL4neurons2/", shell=True)

    os.chdir("./DL4neurons2")
    the_result1 = ""
    if(super_counter == 0):
        the_result1 = subprocess.run('./M1_all_submit.sh '+str(starter_csv), stdout=subprocess.PIPE, universal_newlines=True, shell=True)
    else:
        the_result1 = subprocess.run('./M1_all_submit.sh '+"../"+trail_name+str(super_counter-1)+"/"+str(trail_name)+str(super_counter-1)+".csv", stdout=subprocess.PIPE, universal_newlines=True, shell=True)

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
    subprocess.run("cp /pscratch/sd/t/timshen/tmp_neuInv/bbp3/L5_TTPC1cADpyr0/"+job_id1+"/the_data.npz /pscratch/sd/t/timshen/NEW_DATA_OCT_25_2023/the_data.npz",shell=True)
    subprocess.run("shifter --image=nersc/pytorch:ngc-21.08-v2 ./fixed_threshold_mse_version.sh", shell=True)

    subprocess.run("mkdir "+trail_name+str(super_counter), shell=True)
    subprocess.run("cp *.txt "+trail_name+str(super_counter)+"/", shell=True)
    subprocess.run("cp *.png "+trail_name+str(super_counter)+"/", shell=True)
    subprocess.run("cp *.npy "+trail_name+str(super_counter)+"/", shell=True)
    subprocess.run("cp *.csv "+trail_name+str(super_counter)+"/", shell=True)

    subprocess.run("cp /pscratch/sd/t/timshen/tmp_neuInv/bbp3/L5_TTPC1cADpyr0/"+str(job_id1)+"/out/*.png "+trail_name+str(super_counter)+"/", shell=True)
    subprocess.run("python3 shrunk_final.py "+starter_csv+" "+trail_name+str(super_counter)+".csv"+" "+trail_name+str(super_counter)+" "+that_param, shell=True)
    subprocess.run("cp *.csv "+trail_name+str(super_counter)+"/", shell=True)
    starter_csv = starter_csv+str(super_counter)

    print("Finished Analysis prepping for DaCapo")
    if(super_counter == 0):
        FINISHED = False
    super_counter += 1

