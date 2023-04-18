import os
import re
import pandas as pd
import numpy as np
#输入待筛选的文件,文件必须用反斜线'/'，不能用'\'，程序要用
ori_files = [
              'D:/张以昊/课题组/张以昊/psychopy/SAND数据提取/2023_04_07_mdd_认知/task2数据结果.csv',
              'D:/张以昊/课题组/张以昊/psychopy/SAND数据提取/2023_04_07_mdd_认知/task3数据结果.csv',
              'D:/张以昊/课题组/张以昊/psychopy/SAND数据提取/2023_04_07_mdd_认知/task4数据结果.csv',
              'D:/张以昊/课题组/张以昊/psychopy/SAND数据提取/2023_04_07_mdd_认知/task5数据结果.csv',
              'D:/张以昊/课题组/张以昊/psychopy/SAND数据提取/2023_04_07_mdd_认知/task6数据结果.csv',
              'D:/张以昊/课题组/张以昊/psychopy/SAND数据提取/2023_04_07_mdd_认知/task7数据结果.csv',
              'D:/张以昊/课题组/张以昊/psychopy/SAND数据提取/2023_04_07_mdd_认知/task8数据结果.csv',
              'D:/张以昊/课题组/张以昊/psychopy/SAND数据提取/2023_04_07_mdd_认知/task11数据结果.csv'
              ]
def namelist(path):
    # 按文件类型选择
    df = pd.read_csv(path, encoding='GBK')
    # df = pd.read_excel(path)
    ls= []
    for i in df['filename']:
        temp = re.split('\.|_', i)

        # 自己定义筛选条件（需修改的）

        if (temp[4] == 'father') | (temp[4] == 'mother'):
            continue
        else:
            name = '{}_{}_{}_{}_{}'.format(temp[0],temp[1],temp[2],temp[3],temp[4])
            ls.append(name)
    return ls
# 通过迭代，选出选中文件的交集文件夹
ls1 = namelist(ori_files[0])
ls2 = namelist(ori_files[1])
ls = sorted(list(set(ls1)&set(ls2)))
for i in range(2,len(ori_files),1):
    ls1 = namelist(ori_files[i])
    ls = list(set(ls)&set(ls1))
# 在交集文件夹中筛选有time1,time2的文件夹，即被试编号出现两次
sub = []
for i in ls:
    temp = re.split('\.|_', i)
    sub.append(temp[1])
sub = pd.value_counts(sub)
sub = sub[sub.values==2]
sub = sorted(list(sub.index))
filenames = []
for i in ls:
    temp = re.split('\.|_', i)
    if temp[1] in sub:
        filenames.append(i)
filenames = sorted(filenames)
filenames_print = []
for i in filenames:
    temp = i.split('_')
    name = '{}_{}_{}_{}'.format(temp[0],temp[1],temp[2],temp[3])
    filenames_print.append(name)
filenames_print = '|'.join(filenames_print)
filenames = '|'.join(filenames)
print(filenames_print)
# 迭代逐个把筛选出的认知数据文件给导出来
for i in ori_files:
    temp = i.split('/')
    output_name = temp[-1]
    # 根据文件类型选择
    output_file = pd.read_csv(i, encoding='GBK')
    # output_file = pd.read_excel(i, encoding ='GBK')
    output_file = output_file[output_file['filename'].str.contains(filenames)]
    # 根据文件类型选择
    # output_file.to_excel(output_name, index=False)
    output_file.to_csv(output_name,encoding='GBK', index=False)