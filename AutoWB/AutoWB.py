import os
import cv2
import numpy as np

file_path = os.path.dirname(os.path.abspath(__file__))#读取文件路径
pic_name = "WBresult.png" #读取图片名称
WB_pic = cv2.imread(os.path.join(file_path,pic_name)) #读取WB条带
WB_pic = cv2.blur(WB_pic,(3,3)) #均值模糊去噪

row, col, channel = WB_pic.shape #返回像素高度，像素宽度和通道数

WB_gray = np.zeros((row, col))#创建灰度图矩阵,#彩色转化为灰度图
for r in range(row): 
    for l in range(col):
        WB_gray[r, l] = 0.11 * WB_pic[r, l, 0] + 0.59 * WB_pic[r, l, 1] + 0.3 * WB_pic[r, l, 2]

WB_binary = np.zeros_like(WB_gray)
#创建二值图矩阵
threshold = 100
for r in range(row):
    for l in range(col):
        if WB_gray[r, l] >= threshold:
            WB_binary[r, l] = 255
        else:
            WB_binary[r, l] = 0

cv2.imwrite(os.path.join(file_path,"WBpic_binary.png"),WB_binary.astype("uint8"))