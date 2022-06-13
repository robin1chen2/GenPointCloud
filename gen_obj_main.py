import os
import sys
import torch
import math
from tqdm import tqdm 
from CalTool import cal
from PartsAndSatellite import *


DEVICE=torch.device("cuda:0" if torch.cuda.is_available() else "cpu")



def fetch_data(
        hub_path='obj_parts/hub/', 
        board_path='obj_parts/board/',
        nozzle_path='obj_parts/nozzle/'
    ):
    '''
    fetch the parts data in the given paths
    '''
    hub_parts_paths = [os.path.join(hub_path,name) for name in os.listdir(hub_path)]
    board_parts_paths = [os.path.join(board_path,name) for name in os.listdir(board_path)]
    nozzle_parts_paths = [os.path.join(nozzle_path,name) for name in os.listdir(nozzle_path)]
    hub_list = []
    board_list = []
    nozzle_list = []
    for hub_path in hub_parts_paths:
        label = 0
        points = []
        face_num = []
        socket = []
        xyz = []
        with open(hub_path,'r') as f:
            for line in f.readlines():
                curLine = line.strip().split(' ')
                match curLine[0]:
                    case '#ass':
                        socket.extend(list(map(int,curLine[1:])))
                    case '#xyz':
                        xyz.extend(list(map(float,curLine[1:4])))
                    case 'v':
                        points.append(list(map(float,curLine[1:4])))
                    case 'f':
                        p1 = curLine[1].strip().split('/')
                        p2 = curLine[2].strip().split('/')
                        p3 = curLine[3].strip().split('/')
                        face_num.append([int(p1[0]), int(p2[0]), int(p3[0])] )
        points = torch.Tensor(points)
        points = points.T
        face_num = torch.tensor(face_num)
        hub_list.append(Hub(label,points,face_num,socket,xyz))
    for borad_path in board_parts_paths:
        label = 1
        points = []
        face_num = []
        max = 0
        with open(borad_path,'r') as f:
            for line in f.readlines():
                curLine = line.strip().split(' ')
                match curLine[0]:
                    case '#max':
                        max = int(curLine[1])
                    case 'v':
                        points.append(list(map(float,curLine[1:4])))
                    case 'f':
                        p1 = curLine[1].strip().split('/')
                        p2 = curLine[2].strip().split('/')
                        p3 = curLine[3].strip().split('/')
                        face_num.append([int(p1[0]), int(p2[0]), int(p3[0])] )
        points = torch.Tensor(points)
        points = points.T
        face_num = torch.tensor(face_num)
        board_list.append(Board(label,points,face_num,max))
    for nozzle_path in nozzle_parts_paths:
        label = 2
        points = []
        face_num = []
        with open(nozzle_path,'r') as f:
            for line in f.readlines():
                curLine = line.strip().split(' ')
                match curLine[0]:
                    case 'v':
                        points.append(list(map(float,curLine[1:4])))
                    case 'f':
                        p1 = curLine[1].strip().split('/')
                        p2 = curLine[2].strip().split('/')
                        p3 = curLine[3].strip().split('/')
                        face_num.append([int(p1[0]), int(p2[0]), int(p3[0])] )
        points = torch.Tensor(points)
        points = points.T
        face_num = torch.tensor(face_num)
        nozzle_list.append(Nozzle(label,points,face_num))
    return (hub_list,board_list,nozzle_list)
            
def total_progress():
    '''
    The main function
    '''
    hub_list,board_list,nozzle_list = fetch_data()
    # print(hub_list[1],board_list[1],nozzle_list[1])
    for i in tqdm(range(len(hub_list)), file=sys.stdout):
        for j in tqdm(range(len(board_list)), leave=False, file=sys.stdout):
            for k in tqdm(range(len(nozzle_list)), leave=False, file=sys.stdout):
                hub = hub_list[i]
                board = board_list[j]
                nozzle = nozzle_list[k]
                for l in tqdm(hub.sockets, leave=False, file=sys.stdout):
                    if l <= board.max:
                        for legth in ['normal','short','long']:
                            if legth == 'short':
                                nozzle.points[1,:] *= 0.7 
                            elif legth == 'long':
                                nozzle.points[1,:] *= 2
                            new_sat = Satellite(hub, board, nozzle, l)
                            path = os.path.join(os.path.abspath('..'),'obj_models',f'hub{i}board{j}nozzle{k}_{l}s{legth}.obj')
                            new_sat.output(path)
    
    # print(satellite_list)

    return 0


if __name__ == '__main__':
    total_progress()
    # test_sym()

    
    
   
