import os
import pandas as pd
import numpy as np
output_file = pd.DataFrame(columns=['0back反应时', '0back标准差', '0back正确率',
                                    '1back反应时', '1back标准差', '1back正确率',
                                    '2back反应时', '2back标准差', '2back正确率',
                                    'time', 'pat/con','name', 'filename'],
                           )
ind = 0
path =r'D:\张以昊\课题组\数据\认知_MDD\MDD抑郁组认知数据结果_初步'
sub_dirs = os.listdir(path)
for i in sub_dirs:
    sub_path = path + '/' + i
    files = os.listdir(sub_path)
    SRT = []
    for j in files:
        if '4_Nback' in j:
            SRT.append(j)
    for j in SRT:
        lst = []
        filepath = sub_path + '/' + j
        df = pd.read_csv(filepath, encoding='utf-8')
        output_file.append(df.append(pd.Series(), ignore_index=True))
        output_file.loc[ind, '0back反应时'] = df.iat[0, 1]
        output_file.loc[ind, '0back正确率'] = df.iat[0, 2]
        output_file.loc[ind, '0back标准差'] = df.iat[0, 3]
        output_file.loc[ind, '1back反应时'] = df.iat[1, 1]
        output_file.loc[ind, '1back正确率'] = df.iat[1, 2]
        output_file.loc[ind, '1back标准差'] = df.iat[1, 3]
        output_file.loc[ind, '2back反应时'] = df.iat[2, 1]
        output_file.loc[ind, '2back正确率'] = df.iat[2, 2]
        output_file.loc[ind, '2back标准差'] = df.iat[2, 3]
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
output_file.to_csv('task4数据结果.csv', encoding='GBK', index=False)
