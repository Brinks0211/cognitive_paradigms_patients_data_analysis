import os
import pandas as pd
import numpy as np
output_file = pd.DataFrame(columns=['一周获利',
                                    '两周获利',
                                    '一个月获利',
                                    '六个月获利',
                                    '一年获利',
                                    '五年获利',
                                    '二十五年获利',
                                    'k_一周',
                                    'k_两周',
                                    'k_一个月',
                                    'k_六个月',
                                    'k_一年',
                                    'k_五年',
                                    'k_二十五年',
                                    'time', 'pat/con','name', 'filename'],
                           )
ind = 0
path = r'D:\张以昊\课题组\数据\认知_MDD\MDD抑郁组认知数据结果_初步'
sub_dirs = os.listdir(path)
for i in sub_dirs:
    sub_path = path + '/' + i
    files = os.listdir(sub_path)
    SRT = []
    for j in files:
        if '10_Delay_Discounting_Task' in j:
            SRT.append(j)
    for j in SRT:
        lst = []
        filepath = sub_path + '/' + j
        df = pd.read_csv(filepath, encoding='utf-8')
        output_file.append(df.append(pd.Series(), ignore_index=True))
        output_file.loc[ind, '一周获利'] = df.iat[0, 1]
        output_file.loc[ind, '两周获利'] = df.iat[1, 1]
        output_file.loc[ind, '一个月获利'] = df.iat[2, 1]
        output_file.loc[ind, '六个月获利'] = df.iat[3, 1]
        output_file.loc[ind, '一年获利'] = df.iat[4, 1]
        output_file.loc[ind, '五年获利'] = df.iat[5, 1]
        output_file.loc[ind, '二十五年获利'] = df.iat[6, 1]
        output_file.loc[ind, 'k_一周'] = df.iat[0,2]
        output_file.loc[ind, 'k_两周'] = df.iat[1,2]
        output_file.loc[ind, 'k_一个月'] = df.iat[2,2]
        output_file.loc[ind, 'k_六个月'] = df.iat[3,2]
        output_file.loc[ind, 'k_一年'] = df.iat[4,2]
        output_file.loc[ind, 'k_五年'] = df.iat[5,2]
        output_file.loc[ind, 'k_二十五年'] = df.iat[6,2]
        output_file.loc[ind, 'filename'] = j
        temp = i.split('_')
        output_file.loc[ind, 'name'] = temp[3]
        if temp[2] == 'con':
            output_file.loc[ind, 'pat/con'] = 'con'
        elif temp[2] == 'pat':
            output_file.loc[ind, 'pat/con'] = 'pat'
        if 'time1' in j:
            output_file.loc[ind, 'time'] = 'time1'
        elif 'time2' in j:
            output_file.loc[ind, 'time'] = 'time2'
        elif 'mother' in j:
            output_file.loc[ind, 'time'] = 'mother'
        elif 'father' in j:
            output_file.loc[ind, 'time'] = 'father'
        ind += 1
output_file.to_csv('task10数据结果.csv', encoding='GBK', index=False)
