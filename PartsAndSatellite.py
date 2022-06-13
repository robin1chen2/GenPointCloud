import os
import sys
import torch
import math
from CalTool import cal



class Hub:
    '''
    Hub's data structure
    label -> hub's label(0 or 1 or 2)
    points -> hub's points([x0,x1,x2,...],[y0,y1,y2,...],[z0,z1,z2,...])
    face_num ->points' orders of the faces([f1p1_order,f1p2_order,f1p3_order],...)
    sockets -> max number of board([1,2,3,4])
    xyz -> the cordinates of the socket of the hub and the board([x1,y1,z1])
    '''
    __slots__ =('label','points','face_num','sockets','xyz')
    def __init__(
        self, label:int, points:torch.Tensor, 
        face_num:torch.Tensor, sockets:list, xyz:torch.Tensor
    ):
        self.label = label
        self.points = points
        self.face_num = face_num
        self.sockets = sockets
        self.xyz = xyz
    
    def __repr__(self):  # sourcery skip: merge-list-append, merge-list-appends-into-extend, merge-list-extend, unwrap-iterable-construction
        return_list = []
        return_list.append('\n')
        return_list.append('-'*30)
        return_list.append('Let us introduce this hub:')
        return_list.append(f'The label of this hub is {self.label}')
        return_list.append(f'This hub contains {self.points.shape[1]} points')
        return_list.append(f'The first point is {self.points[:,0]}')
        return_list.append(f'This hub contains {self.face_num.shape[0]} faces')
        return_list.append(f'The first face is constructed by {self.face_num[0,:]} points')
        return_list.append(f'This hub has {self.sockets} sockets')
        return_list.append(f'The first socket is location is {self.xyz}')
        return_list.append('That is all!')
        return_list.append('-'*30)
        return_list.append('\n')
        return '\n'.join(return_list)

class Board:
    '''
    Board's data structure
    label -> hub's label(0 or 1 or 2)
    points -> hub's points([x0,x1,x2,...],[y0,y1,y2,...],[z0,z1,z2,...])
    face_num ->points' orders of the faces([f1p1_order,f1p2_order,f1p3_order],...)
    max -> this kind of board's max amout on a hub
    '''
    __slots__ =('label','points','face_num','max')
    def __init__(self, label:int, points:torch.Tensor, face_num:torch.Tensor, max:int):
        self.label = label
        self.points = points
        self.face_num = face_num
        self.max = max
    
    def __repr__(self):  # sourcery skip: merge-list-append, merge-list-appends-into-extend, merge-list-extend, unwrap-iterable-construction
        return_list = []
        return_list.append('\n')
        return_list.append('-'*30)
        return_list.append('Let us introduce this board:')
        return_list.append(f'The label of this board is {self.label}')
        return_list.append(f'This board contains {self.points.shape[1]} points')
        return_list.append(f'The first point is {self.points[:,0]}')
        return_list.append(f'This board contains {self.face_num.shape[0]} faces')
        return_list.append(f'The first face is constructed by {self.face_num[0,:]} points')
        return_list.append(f'The amount of this board is {self.max}')
        return_list.append('That is all!')
        return_list.append('-'*30)
        return_list.append('\n')
        return '\n'.join(return_list)

class Nozzle:
    '''
    Nozzle's data structure
    label -> hub's label(0 or 1 or 2)
    points -> hub's points([x0,x1,x2,...],[y0,y1,y2,...],[z0,z1,z2,...])
    face_num ->points' orders of the faces([f1p1_order,f1p2_order,f1p3_order],...)
    '''
    __slots__ =('label','points','face_num')
    def __init__(self, label:int, points:torch.Tensor, face_num:torch.Tensor):
        self.label = label
        self.points = points
        self.face_num = face_num

    def __repr__(self):  # sourcery skip: merge-list-append, merge-list-appends-into-extend, merge-list-extend, unwrap-iterable-construction
        return_list = []
        return_list.append('\n')
        return_list.append('-'*30)
        return_list.append('Let us introduce this nozzle:')
        return_list.append(f'The label of this nozzle is {self.label}')
        return_list.append(f'This nozzle contains {self.points.shape[1]} points')
        return_list.append(f'The first point is {self.points[:,0]}')
        return_list.append(f'This nozzle contains {self.face_num.shape[0]} faces')
        return_list.append(f'The first face is constructed by {self.face_num[0,:]} points')
        return_list.append('That is all!')
        return_list.append('-'*30)
        return_list.append('\n')
        return '\n'.join(return_list)

class Satellite:
    '''
    Satellite's data structure
    points -> satellite's points([x0,x1,x2,...],[y0,y1,y2,...],[z0,z1,z2,...])
    face_num ->points' orders of the faces([f1p1_order,f1p2_order,f1p3_order],...)
    total_hub_face_num -> the faces of the hub
    total_board_face_num -> the faces of the board
    total_nozzle_face_num -> the faces of the nozzle
    assemble() -> gen the points and face_num
    '''
    # __slots__ = ('points','face_num','total_hub_face_num','total_board_face_num','total_nozzle_face_num','assemble')
    def __init__(self,hub,board,nozzle,board_num):
        self.total_hub_face_num = int(hub.face_num.shape[0])
        self.total_board_face_num = int(board.face_num.shape[0])*board_num
        self.total_nozzle_face_num = int(nozzle.face_num.shape[0])
        self.assemble(hub,board,nozzle,board_num)
        
    def __repr__(self):  # sourcery skip: merge-list-append, merge-list-appends-into-extend, merge-list-extend,
        return_list=[]
        return_list.append('\n')
        return_list.append('-'*30)
        return_list.append(f'This satellite contains {self.points.shape[1]} points')
        return_list.append(f'This satellite contains {self.face_num.shape[0]} faces')
        return_list.append(f'The faces of hub {self.total_hub_face_num}, board {self.total_board_face_num}and nozzle{self.total_nozzle_face_num}.')
        return_list.append('-'*30)
        return_list.append('\n')
        return '\n'.join(return_list)
    
    def assemble(self,hub,board,nozzle,board_num):
        original_board_points= cal.moveto(board.points, hub.xyz[0], hub.xyz[1], hub.xyz[2])
        unit_hub_points_len = hub.points.shape[1]
        unit_board_points_len = board.points.shape[1]
        match board_num:
            case 1:
                self.points = torch.cat((hub.points,original_board_points,nozzle.points),dim=1)
                board_num1 = board.face_num + unit_hub_points_len
                nozzle_num1 = nozzle.face_num + unit_hub_points_len + unit_board_points_len
                self.face_num = torch.cat((hub.face_num,board_num1,nozzle_num1),dim = 0)
            case 2:
                # other_board_points= cal.sym(original_board_points,'x')
                aix = torch.Tensor([[0],[1],[0]])
                theta1 = torch.Tensor([math.pi])
                other_board_points1 = cal.rot(original_board_points,aix,theta1)
                self.points = torch.cat((hub.points,original_board_points,other_board_points1,nozzle.points),dim=1)
                board_num1 = board.face_num + unit_hub_points_len
                board_num2 = board.face_num + unit_hub_points_len + unit_board_points_len
                nozzle_num1 = nozzle.face_num + unit_hub_points_len + 2*unit_board_points_len
                self.face_num = torch.cat((hub.face_num,board_num1,board_num2,nozzle_num1),dim = 0)
            case 3:
                aix = torch.Tensor([[0],[1],[0]])
                theta1 = torch.Tensor([math.pi*2/3])
                theta2 = torch.Tensor([math.pi*4/3])
                other_board_points1 = cal.rot(original_board_points,aix,theta1)
                other_board_points2 = cal.rot(original_board_points,aix,theta2)
                self.points = torch.cat((hub.points,original_board_points,other_board_points1,other_board_points2,nozzle.points),dim=1)
                board_num1 = board.face_num + unit_hub_points_len
                board_num2 = board.face_num + unit_hub_points_len + unit_board_points_len
                board_num3 = board.face_num + unit_hub_points_len + 2*unit_board_points_len
                nozzle_num1 = nozzle.face_num + unit_hub_points_len + 3*unit_board_points_len
                self.face_num = torch.cat((hub.face_num,board_num1,board_num2,board_num3,nozzle_num1),dim = 0)
            case 4:
                aix = torch.Tensor([[0],[1],[0]])
                theta1 = torch.Tensor([math.pi / 2])
                theta2 = torch.Tensor([math.pi])
                theta3 = torch.Tensor([math.pi*3/2])
                other_board_points1 = cal.rot(original_board_points,aix,theta1)
                other_board_points2 = cal.rot(original_board_points,aix,theta2)
                other_board_points3 = cal.rot(original_board_points,aix,theta3)
                self.points = torch.cat((hub.points,original_board_points,other_board_points1,other_board_points2,other_board_points3,nozzle.points),dim=1)
                board_num1 = board.face_num + unit_hub_points_len
                board_num2 = board.face_num + unit_hub_points_len + unit_board_points_len
                board_num3 = board.face_num + unit_hub_points_len + 2*unit_board_points_len
                board_num4 = board.face_num + unit_hub_points_len + 3*unit_board_points_len
                nozzle_num1 = nozzle.face_num + unit_hub_points_len + 4*unit_board_points_len
                self.face_num = torch.cat((hub.face_num,board_num1,board_num2,board_num3,board_num4,nozzle_num1),dim = 0)

    def output(self,path):
        with open(path,'w') as f:
            f.write(f'#hub_face_num {self.total_hub_face_num}')
            f.write('\n')
            f.write(f'#board_face_num {self.total_board_face_num}')
            f.write('\n')
            f.write(f'#nozzle_face_num {self.total_nozzle_face_num}')
            f.write('\n')
            for i in range(self.points.shape[1]):
                str_point = ' '.join(list(map(str,self.points[:,i].tolist())))
                f.write(f'v {str_point}')
                f.write('\n')
            for i in range(self.face_num.shape[0]):
                str_point = ' '.join(list(map(str,self.face_num[i,:].tolist())))
                f.write(f'f {str_point}')
                f.write('\n')







if __name__ == 'main':
    print('hi')