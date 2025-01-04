import os
import cv2
import numpy as np
import json

file_path = os.path.dirname(os.path.abspath(__file__))#读取文件路径
pic_name = "WBpic_binary.png" #读取图片名称
WB_pic = cv2.imread(os.path.join(file_path,pic_name), -1) #直接读取二值图

def discern_obj(pic:np.array):
    
    array = 1 * (pic < 128)  #白色转化为0,黑色转化为1

    row, col = array.shape

    x_list_obj = [] #创建蛋白 x坐标列表
    f = open("./AutoWB/marker_end.txt", "r")
    flag = int(f.read())+1 #防止从头开始，从marker后1位开始遍历

    for i in range (flag, col): #当x满足条件后根据flag同时跳跃
        x_obj_mono = []#每组蛋白条带x坐标范围
        for j in range(2):#求蛋白条带x坐标范围
            for x in range(flag, col):
                if (sum(array[:,x]) > 3) != (sum(array[:,x-1])> 3): #当色块发生变化
                    x_obj_mono.append(x)
                    flag = x+1
                    if j == 1:
                        x_list_obj.append(x_obj_mono)
                    break #j+1
    with open('./AutoWB/groups.json', 'w') as f:
        json.dump(x_list_obj, f)

    protein_dict = {} #创建所有蛋白组，key为第num组，value为所有y值
    for num in range(0,len(x_list_obj)): #遍历所有蛋白
        y_list_obj = [] #蛋白条带所有蛋白y坐标范围列表
        y_obj_mono = [] #每组蛋白条带每个y坐标范围
        cycle = 0 #ymin ymax循环
        for y in range(row):   
            if (sum(array[y,x_list_obj[num][0]:x_list_obj[num][1]+1]) > 10)!= (sum(array[y-1,x_list_obj[num][0]:x_list_obj[num][1]+1]) > 10): #在第num条蛋白带范围里检索突变
                y_obj_mono.append(y)#第num条蛋白带每组y坐标范围
                cycle = cycle + 1
                if cycle == 2:
                    y_list_obj.append(y_obj_mono)
                    y_obj_mono = []
                    cycle = 0
        protein_dict['第'+str(num+1)+'组'] = y_list_obj

    
    img = cv2.imread(os.path.join(file_path,pic_name))#添加图片注释
    for num in range(0,len(x_list_obj)): #遍历所有蛋白组
        groupnumber = num + 1
        for obj in range(0,len(protein_dict['第'+str(groupnumber)+'组'])): #遍历某个蛋白组元素
            x1 = x_list_obj[num][0]
            y1 = protein_dict['第'+str(groupnumber)+'组'][obj][0]
            x2 = x_list_obj[num][1]
            y2 = protein_dict['第'+str(groupnumber)+'组'][obj][1]
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2) #绘制方框
            label = 'Group'+str(groupnumber)+'\n'+'Protein'+chr(65+obj) #添加换行标签
            for i, txt in enumerate(label.split('\n')): #逐行添加换行文字
                y = y1-20+i*15
                cv2.putText(img, txt, (x1,y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2) #添加文字，坐标, 字体，字体大小，颜色，粗细

    cv2.imwrite(os.path.join(file_path,"WBpic_discern.png"),img)#添加至图片上

    with open('./AutoWB/proteins.json', 'w') as f:
        json.dump(protein_dict, f)

    return protein_dict
    



if __name__ == '__main__': #直接运行文件
    print(discern_obj(WB_pic))