import numpy as np
from itertools import product
from functools import partial
from multiprocessing import Pool, Process
import pickle
import sys

ION_CHANNEL = int(sys.argv[1])
NUM_REGIONS = 20
b = np.load("the_data.npz")

if __name__ == '__main__':
    arr = []
    for num in range(70000):
        #for i in range(NUM_CHANNELS):
        bval1 = b['actual_val'][num][ION_CHANNEL]
        bval2 = b['predicted_val'][num][ION_CHANNEL]
        arr.append(abs(bval1-bval2))

    arr = np.array(arr)
    np.savez("errors"+str(ION_CHANNEL)+".npz", x=arr)
