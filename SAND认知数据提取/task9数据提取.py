import os
import pandas as pd
import numpy as np
output_file = pd.DataFrame(columns=['阶段1获利反应时', '阶段1获利标准差', 
                                    '阶段1损失反应时', '阶段1损失标准差', 
                                    '阶段2获利反应时', '阶段2获利标准差', 
                                    '阶段2损失反应时', '阶段2损失标准差', 
                                    '阶段3获利反应时', '阶段3获利标准差', 
                                    '阶段3损失反应时', '阶段3损失标准差',
                                    '阶段4获利反应时', '阶段4获利标准差',
                                    '阶段4损失反应时', '阶段4损失标准差',
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
        if '9_Simple_Guessing_Task' in j:
            SRT.append(j)
    for j in SRT:
        lst = []
        filepath = sub_path + '/' + j
        df = pd.read_csv(filepath, encoding='utf-8')
        output_file.append(df.append(pd.Series(), ignore_index=True))
        output_file.loc[ind, '阶段1获利反应时'] = df.iat[0, 1]
        output_file.loc[ind, '阶段1获利标准差'] = df.iat[0, 2]
        output_file.loc[ind, '阶段1损失反应时'] = df.iat[1, 1]
        output_file.loc[ind, '阶段1损失标准差'] = df.iat[1, 2]
        output_file.loc[ind, '阶段2获利反应时'] = df.iat[2, 1]
        output_file.loc[ind, '阶段2获利标准差'] = df.iat[2, 2]
        output_file.loc[ind, '阶段2损失反应时'] = df.iat[3, 1]
        output_file.loc[ind, '阶段2损失标准差'] = df.iat[3, 2]
        output_file.loc[ind, '阶段3获利反应时'] = df.iat[4, 1]
        output_file.loc[ind, '阶段3获利标准差'] = df.iat[4, 2]
        output_file.loc[ind, '阶段3损失反应时'] = df.iat[5, 1]
        output_file.loc[ind, '阶段3损失标准差'] = df.iat[5, 2]
        output_file.loc[ind, '阶段4获利反应时'] = df.iat[6, 1]
        output_file.loc[ind, '阶段4获利标准差'] = df.iat[6, 2]
        output_file.loc[ind, '阶段4损失反应时'] = df.iat[7, 1]
        output_file.loc[ind, '阶段4损失标准差'] = df.iat[7, 2]
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
output_file.to_csv('task9数据结果.csv', encoding='GBK', index=False)
