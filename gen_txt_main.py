import os 
import sys
import torch
import math
import numpy as np
from tqdm import tqdm
import multiprocessing as mp
from multiprocessing import Pool
from PartsAndSatellite import *


def fetch_data(input_path,output_path):
    obj_list = os.listdir(input_path)
    for obj in obj_list:
        with open(os.path.join(input_path,obj),'r') as f:
            for line in f.readlines():
                curLine = line.strip().split(' ')
                




def total_process():
    input_path = os.path.join(obj)

    return 0

if __name__ == '__main__':
    total_process()