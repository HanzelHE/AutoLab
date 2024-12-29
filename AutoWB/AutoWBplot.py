import os
import cv2
import numpy as np
import pandas as pd

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
    global marker_end #定义全局变量用于下列操作
    marker_end = x_list_ref[1]
    return dic_ref


def discern_obj(array:np.array):
    
    array = 1 * (array < 128)
    row, col = array.shape

    x_list_obj = [] #创建蛋白 x坐标列表
    flag = marker_end #防止从头开始，从marker后开始遍历

    for i in range (flag, col):
        x_obj_mono = []#每组蛋白条带x坐标范围
        for j in range(2):#求蛋白条带x坐标范围
            for x in range(flag, col):
                if (sum(array[:,x]) > 3) != (sum(array[:,x-1])> 3): #当色块发生变化
                    x_obj_mono.append(x)
                    flag = x+1
                    if j == 1:
                        x_list_obj.append(x_obj_mono)
                    break #j+1
    #获得每组蛋白坐标


    protein_dict = {} #创建所有蛋白组，key为第num组，value为所有y值
    for num in range(0,len(x_list_obj)): #遍历所有蛋白
        y_list_obj = [] #蛋白条带所有蛋白y坐标范围列表
        y_obj_mono = [] #每组蛋白条带每个y坐标范围
        flag = 0 #ymin ymax循环
        for y in range(row):   
            if (sum(array[y,x_list_obj[num][0]:x_list_obj[num][1]+1]) > 5)!= (sum(array[y-1,x_list_obj[num][0]:x_list_obj[num][1]+1]) > 5): #在第num条蛋白带范围里检索突变
                y_obj_mono.append(y)#第num条蛋白带每组y坐标范围
                flag = flag + 1
                if flag == 2:
                    y_list_obj.append(y_obj_mono)
                    y_obj_mono = []
                    flag = 0
        protein_dict['第'+str(num+1)+'组'] = y_list_obj
    
    img = cv2.imread(os.path.join(file_path,pic_name))
    for num in range(0,len(x_list_obj)): #遍历所有蛋白组
        groupnumber = num + 1
        for obj in range(0,len(protein_dict['第'+str(groupnumber)+'组'])): #遍历某个蛋白组元素
            x1 = x_list_obj[num][0]
            y1 = protein_dict['第'+str(groupnumber)+'组'][obj][0]
            x2 = x_list_obj[num][1]
            y2 = protein_dict['第'+str(groupnumber)+'组'][obj][1]
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2) #绘制方框
            label = 'Group'+str(groupnumber)+'Protein'+chr(65+obj)
            cv2.putText(img, label, (x1,y1), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2) #添加文字，坐标, 字体，字体大小，颜色，粗细


    cv2.imwrite(os.path.join(file_path,"WBpic_discern.png"),img)
    
discern_ref(WB_pic)
discern_obj(WB_pic)

                    



    

    



