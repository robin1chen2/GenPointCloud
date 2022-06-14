import os
from re import L
import sys
import torch
import math
from tqdm import tqdm 

DEVICE=torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

class cal:
    '''
    class that cotains the calculation methods used in the progress
    '''

    @staticmethod
    def rot(x:torch.Tensor, rot_aix:torch.Tensor, rot_angle:torch.Tensor) -> torch.Tensor:
        '''
        rot matrix x([x0,x1,...],[y0,y1,...],[z0,z1,...]) 
        with rot_aix([x0],[y0],[z0]) 
        and rot_angle(theta)
        return x_done([x0',x1',...],[y0',y1',...],[z0',z1',...])
        '''
        if rot_aix.device != 'cpu':rot_aix = rot_aix.cpu()
        aix_norm = rot_aix*rot_aix
        aix_norm = aix_norm.sum().sqrt()
        if torch.abs(aix_norm-1) > 1e-3: 
            unit_aix = rot_aix/aix_norm
        else:unit_aix = rot_aix/1
        # print(f'unit_aix:{unit_aix}')
        p1,p2,p3 = unit_aix[0],unit_aix[1],unit_aix[2]
        # print(f'p1:{p1} p2:{p2} p3:{p3}')
        C = torch.cos(rot_angle)
        S = torch.sin(rot_angle)
        # print(f'Cos:{C},Sin:{S}')
        rot_dcm = torch.tensor(
            [[p1*p1*(1-C)+C,p1*p2*(1-C)-p3*S,p3*p1*(1-C)+p2*S],
            [p1*p2*(1-C)+p3*S,p2*p2*(1-C)+C,p3*p2*(1-C)-p1*S],
            [p3*p1*(1-C)-p2*S,p3*p2*(1-C)+p1*S,p3*p3*(1-C)+C]]
        ,device=DEVICE)
        # print(rot_dcm)
        if x.device != 'cuda:0':x = x.cuda()
        return torch.mm(rot_dcm,x).cpu()

    @staticmethod
    def moveto(x:torch.Tensor,cor_x,cor_y,cor_z):
        '''
        rot matrix x([x0,x1,...],[y0,y1,...],[z0,z1,...]) 
        with movement([cor_x],[cor_y],[cor_z])
        '''
        movement = torch.Tensor([[cor_x],[cor_y],[cor_z]])
        return x+movement

    @staticmethod
    def sym(x:torch.Tensor,aix):
        '''
        reflex the matrix x([x0,x1,...],[y0,y1,...],[z0,z1,...])
        with the coordinates aix
        '''
        y = x[:]
        match aix:
            case 'x':
                y[0,:] = -x[0,:]
            case 'y':
                y[1,:] = -x[1,:]
            case 'z':
                y[2,:] = -x[2,:]
        return y 




def test_rot():
    
    aix = torch.Tensor([[0],[0],[1]])
    point = torch.Tensor([[1,0],[0,1],[0,0]])
    theta = torch.Tensor([math.pi/4])
    print(cal.rot(point,aix,theta))
    print(point.device)
    return 0

def test_move():
    point = torch.Tensor([[1,0],[0,1],[0,0]])
    print(cal.moveto(point,2,2,2))
    return 0 

def test_sym():
    aix = 'x'
    point = torch.Tensor([[1,0],[0,1],[0,0]])
    print(cal.sym(point,aix))
    print(point.device)

def test_cat():
    a = torch.randn([3,7])
    b = torch.randn([3,3])
    c = torch.cat((a,b),dim=1)
    print(c)
    print(c.shape)
    return 0

def plustorch():
    a = torch.randn([3,7])
    print(a)
    print(a+1)
    return 0 

def test_torch2str():
    a = torch.randn([3,7])
    print(list(map(str,a[:,2].tolist())))
    return 0 


def path_try():
    path = os.path.join(os.path.abspath('..'),'satellitedata','hi.txt')
    # path = '.\\satellitedata\\hi.txt'
    with open(path,'w') as f:
        f.write('hi')
    print(path)

def test_torchpi():
    a = torch.randn([3,7])
    b = a.clone()
    c = torch.Tensor([[0],[0],[0]])
    b[:,0] = torch.Tensor([0,0,0])
    print(b)
    print(a)
    print(c)
    print(c.T)
    return 0

if __name__ == '__main__':
    test_torchpi()
    