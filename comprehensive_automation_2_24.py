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
while(FINISHED == False and super_counter != 2):
    FINISHED = True
    the_vals = []
    the_lister = ["gNaTs2_tbar_NaTs2_t_apical", "gSKv3_1bar_SKv3_1_apical","gImbar_Im_apical","gIhbar_Ih_dend", "gNaTa_tbar_NaTa_t_axonal", "gK_Tstbar_K_Tst_axonal", "gNap_Et2bar_Nap_Et2_axonal", "gSK_E2bar_SK_E2_axonal", "gCa_HVAbar_Ca_HVA_axonal", "gK_Pstbar_K_Pst_axonal","gCa_LVAstbar_Ca_LVAst_axonal", "g_pas_axonal", "cm_axonal", "gSKv3_1bar_SKv3_1_somatic","gNaTs2_tbar_NaTs2_t_somatic", "gCa_LVAstbar_Ca_LVAst_somatic", "g_pas_somatic", "cm_somatic", "e_pas_all"]
    narrow_left = []
    narrow_right = []
    reduce_right = False
    reduce_left = False

    x = open("base_lb_ub.txt").read().splitlines()
    the_names1 = open("names.txt").read().splitlines()

    the_names = []
    for i1 in the_names1:
        tempy,_ = i1.split(",")
        the_names.append(tempy)

    the_dictionary_lb = {}
    the_dictionary_ub = {}
    the_order = []
    lb = []
    ub = []
    for i in range(len(x)):
        if(i == 0):
            lb = x[i].split(" ")
        else:
            ub = x[i].split(" ")

    for i in range(len(the_names)):
        the_dictionary_lb[the_names[i]] =float(lb[i])
        the_dictionary_ub[the_names[i]] = float(ub[i])

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
            if(int(i2) == 1 and len(narrow_left) >= 0):
                narrow_left.append(int(i2))
            if(int(i2) == 18):
                narrow_right.append(int(i2))
            if(int(i2) == 19 and len(narrow_right) >= 1):
                narrow_right.append(int(i))
            if(int(i2) == 19 and len(narrow_right) >= 2):
                reduce_right = True
            if(int(i2) == 3 and len(narrow_left) >= 2):
                reduce_left = True

        if(reduce_right):
           FINISHED = False
           the_dictionary_ub[the_names[iq]] -= 0.001
           #contracting when last 2 regions violating
        else:
           the_dictionary_ub[the_names[iq]] += 0.001
           #expand when last 2 regions not violating
        if(reduce_left):
            FINISHED = False
            the_dictionary_lb[the_names[iq]] -= 0.001
           #contracting when first 2 regions violating
        else:
            the_dictionary_lb[the_names[iq]] += 0.001
            #expand when first 2 regions not violating

        the_new_lb.append(str(the_dictionary_lb[the_names[iq]]))
        the_new_ub.append(str(the_dictionary_ub[the_names[iq]]))

    f = open("unit_params.csv", "w")
    f.write('Parameters,LB,UB\n')
    print(the_new_lb)
    print(the_new_ub)
    for i_name in range(len(the_names)):
        f.write(str(the_names[i_name]) + ","+str(the_new_lb[i_name])+","+str(the_new_ub[i_name]))
        if(i_name == (len(the_names)-1)):
            break
        f.write('\n')

    f.close()
    subprocess.run("cat unit_params.csv", shell=True)
    subprocess.run("cp unit_params.csv /pscratch/sd/a/asharoff/NEW_DATA_OCT_25_2023/DL4neurons2/unit_params.csv", shell=True)

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
    subprocess.run("cp /pscratch/sd/a/asharoff/tmp_neuInv/bbp3/L5_TTPC1cADpyr0/"+job_id+"/the_data.npz /pscratch/sd/a/asharoff/NEW_DATA_OCT_25_2023/the_data.npz",shell=True)
    subprocess.run("shifter --image=nersc/pytorch:ngc-21.08-v2 ./fixed_threshold_mse_version.sh", shell=True)
    print("Finished Analysis prepping for DaCapo")
    super_counter += 1

