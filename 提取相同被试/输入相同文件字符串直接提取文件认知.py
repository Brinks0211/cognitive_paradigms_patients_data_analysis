import os
import re
import pandas as pd
import numpy as np
#输入待筛选的文件,文件必须用反斜线'/'，不能用'\'，程序要用
ori_files = [
    'D:/张以昊/课题组/张以昊/psychopy/SAND数据提取/提取相同被试/task3数据结果.csv',
              'D:/张以昊/课题组/张以昊/psychopy/SAND数据提取/提取相同被试/task5数据结果.csv',
              'D:/张以昊/课题组/张以昊/psychopy/SAND数据提取/提取相同被试/task7数据结果.csv',
              'D:/张以昊/课题组/张以昊/psychopy/SAND数据提取/提取相同被试/task8数据结果.csv',
              ]
questionnair = 'D:/张以昊/课题组/张以昊/psychopy/SAND数据提取/提取相同被试/CDI_pat.csv'
df = pd.read_csv(questionnair, encoding='GBK')
filenames = []
for i in df['filename']:
    temp = i.split(".")
    filenames.append(temp[0])
filenames = "|".join(filenames)
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


