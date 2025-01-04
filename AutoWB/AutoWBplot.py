import os
import cv2
import pandas as pd
import json
import numpy
import matplotlib.pyplot as plt

file_path = os.path.dirname(os.path.abspath(__file__))#读取文件路径
pic_name = "WBpic_binary.png" #读取图片名称
WB_pic = cv2.imread(os.path.join(file_path,pic_name), -1) #直接读取二值图

array = 1 * (WB_pic < 128)

with open('./AutoWB/groups.json', 'r') as f:
    grouplist = json.load(f)
print(grouplist)

with open('./AutoWB/proteins.json', 'r') as f:
    proteinlist = json.load(f)
print(proteinlist)

plot_dict = {}
group_list = []
value_list= []
for i in range(len(grouplist)):

    if i not in [2,3]:
        x0, x1 = grouplist[i][0], grouplist[i][1]
        y0, y1 = proteinlist['第'+str(i+1)+'组'][0][0], proteinlist['第'+str(i+1)+'组'][0][1]
        value = sum(sum(array[y0:y1, x0:x1]))
        group_list.append('group'+str(i+1)) 
        value_list.append(value) #对黑点进行计数

    else:
        x0, x1 = grouplist[i][0], grouplist[i][1]
        y0, y1 = proteinlist['第'+str(i+1)+'组'][1][0], proteinlist['第'+str(i+1)+'组'][1][1]
        value = sum(sum(array[y0:y1, x0:x1]))
        group_list.append('group'+str(i+1)) 
        value_list.append(value)
    
    value_list_norm = list(map(lambda x: round(x/numpy.amax(value_list),2), value_list)) #归一化,round(,2)保留两位小数
    plot_dict['groups'] = group_list
    plot_dict['values'] = value_list_norm

plot_df = pd.DataFrame(plot_dict) #数据框封装
plot_df.plot(kind='bar', x='groups', y='values', title='Relative quantity of Protein ', xlabel='groups', ylabel='ratio', figsize=(8, 5)) #创建条形图
plt.savefig('./AutoWB/proteinratio.png')
plt.show()


    

    



