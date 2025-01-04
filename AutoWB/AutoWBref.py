import os
import cv2
import numpy as np
import json

file_path = os.path.dirname(os.path.abspath(__file__))#读取文件路径
pic_name = "WBpic_binary.png" #读取图片名称
WB_pic = cv2.imread(os.path.join(file_path,pic_name), -1) #直接读取二值图

def discern_ref(array:np.array):
    dic_ref = {}
    array = 1 * (array < 128) #白色转化为0,黑色转化为1
    row, col = array.shape

    x_list_ref = [] #创建marker x坐标列表
    flag = 0 #防止从头开始
    for i in range(2):#求marker条带x坐标范围
        for x in range(flag, col):
            if (sum(array[:,x]) == 0) != (sum(array[:,x-1])==0): #当色块发生变化
                x_list_ref.append(x)
                flag = x+1
                break#i+1
    
    y_list_ref = [] #求marker条带y坐标范围
    flag = 0 #防止从头开始

    for i in range(flag, row): #将循环器向下推进
        y_ref_mono = []#marker条带每组y坐标范围
        for j in range(2):
            for y in range(flag,row): #遍历指定范围y坐标
                if (sum(array[y,x_list_ref[0]:x_list_ref[1]+1]) > 3)!= (sum(array[y-1,x_list_ref[0]:x_list_ref[1]+1]) > 3): #在marker条带范围里检索突变
                    y_ref_mono.append(y)#marker条带每组y坐标范围
                    flag = y+1
                    if j == 1:
                        y_list_ref.append(y_ref_mono)
                    break#j+1
    
    marker_kda = list(map(lambda i:str(i)+'kda',range(1,11))) #创建系列marker分子量
    dic_ref = {'marker_kda':marker_kda, 'y_value':y_list_ref}

    f = open("./AutoWB/marker_end.txt", "w") #写入marker末端x值用于后续操作
    f.write( str(x_list_ref[1]) )
 
    return dic_ref

if __name__ == '__main__': #直接运行文件
    print(discern_ref(WB_pic))