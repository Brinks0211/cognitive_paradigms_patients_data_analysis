import os
import re
import pandas as pd
import numpy as np

#输入待筛选的文件,文件必须用反斜线'/'，不能用'\'，程序要用

ori_files = [ 'D:/张以昊/课题组/张以昊/psychopy/SAND数据提取/2023_04_07_mdd_认知/task3数据结果.csv',
              'D:/张以昊/课题组/张以昊/psychopy/SAND数据提取/2023_04_07_mdd_认知/task5数据结果.csv',
              'D:/张以昊/课题组/张以昊/psychopy/SAND数据提取/2023_04_07_mdd_认知/task7数据结果.csv',
              'D:/张以昊/课题组/张以昊/psychopy/SAND数据提取/2023_04_07_mdd_认知/task8数据结果.csv',
            ]
def namelist(path):
    # 按文件类型选择
    df = pd.read_csv(path, encoding='GBK')
    # df = pd.read_excel(path)
    ls= []
    for i in df['filename']:
        temp = re.split('\.|_', i)

        # 自己定义筛选条件（需修改的）

        if (temp[4] == 'father') | (temp[4] == 'mother')|(temp[4] == 'time2'):
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
ls = sorted(ls)
index = '|'.join(ls)
#输出一个字符串用来给问卷匹配的
filenames = []
for i in ls:
    temp = re.split('\.|_', i)
    name = '{}_{}_{}_{}'.format(temp[0],temp[1],temp[2],temp[3],)
    filenames.append(name)
filenames = sorted(list(set(filenames)))
filenames = '|'.join(filenames)
print(filenames)
# 迭代逐个把筛选出的数据文件给导出来
for i in ori_files:
    temp = i.split('/')
    output_name = temp[-1]
    # 根据文件类型选择
    output_file = pd.read_csv(i, encoding='GBK')
    # output_file = pd.read_excel(i, encoding ='GBK')
    output_file = output_file[output_file['filename'].str.contains(index)]
    # 根据文件类型选择
    # output_file.to_excel(output_name, index=False)
    output_file.to_csv(output_name,encoding='GBK', index=False)
