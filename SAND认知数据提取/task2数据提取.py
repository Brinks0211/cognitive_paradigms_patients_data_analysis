import os
import pandas as pd
import numpy as np
output_file = pd.DataFrame(columns=['平静-平静反应时', '平静-平静标准差', '平静-平静正确率',
                                    '悲伤(吸引)-高兴反应时', '悲伤(吸引)-高兴标准差', '悲伤(吸引)-高兴正确率',
                                    '悲伤-高兴(吸引)反应时', '悲伤-高兴(吸引)标准差', '悲伤-高兴(吸引)正确率',
                                    '悲伤(吸引)-平静反应时', '悲伤(吸引)-平静标准差', '悲伤(吸引)-平静正确率',
                                    '悲伤-平静(吸引)反应时', '悲伤-平静(吸引)标准差', '悲伤-平静(吸引)正确率',
                                    '高兴(吸引)-平静反应时', '高兴(吸引)-平静标准差', '高兴(吸引)-平静正确率',
                                    '高兴-平静(吸引)反应时', '高兴-平静(吸引)标准差', '高兴-平静(吸引)正确率',
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
        if '2_Dot_Probe' in j:
            SRT.append(j)
    for j in SRT:
        lst = []
        filepath = sub_path + '/' + j
        df = pd.read_csv(filepath, encoding='utf-8')
        output_file.append(df.append(pd.Series(), ignore_index=True))
        output_file.loc[ind, '平静-平静反应时'] = df.iat[0, 1]
        output_file.loc[ind, '平静-平静正确率'] = df.iat[0, 2]
        output_file.loc[ind, '平静-平静标准差'] = df.iat[0, 3]
        output_file.loc[ind, '悲伤(吸引)-高兴反应时'] = df.iat[1, 1]
        output_file.loc[ind, '悲伤(吸引)-高兴正确率'] = df.iat[1, 2]
        output_file.loc[ind, '悲伤(吸引)-高兴标准差'] = df.iat[1, 3]
        output_file.loc[ind, '悲伤-高兴(吸引)反应时'] = df.iat[2, 1]
        output_file.loc[ind, '悲伤-高兴(吸引)正确率'] = df.iat[2, 2]
        output_file.loc[ind, '悲伤-高兴(吸引)标准差'] = df.iat[2, 3]
        output_file.loc[ind, '悲伤(吸引)-平静反应时'] = df.iat[3, 1]
        output_file.loc[ind, '悲伤(吸引)-平静正确率'] = df.iat[3, 2]
        output_file.loc[ind, '悲伤(吸引)-平静标准差'] = df.iat[3, 3]
        output_file.loc[ind, '悲伤-平静(吸引)反应时'] = df.iat[4, 1]
        output_file.loc[ind, '悲伤-平静(吸引)正确率'] = df.iat[4, 2]
        output_file.loc[ind, '悲伤-平静(吸引)标准差'] = df.iat[4, 3]
        output_file.loc[ind, '高兴(吸引)-平静反应时'] = df.iat[5, 1]
        output_file.loc[ind, '高兴(吸引)-平静正确率'] = df.iat[5, 2]
        output_file.loc[ind, '高兴(吸引)-平静标准差'] = df.iat[5, 3]
        output_file.loc[ind, '高兴-平静(吸引)反应时'] = df.iat[6, 1]
        output_file.loc[ind, '高兴-平静(吸引)正确率'] = df.iat[6, 2]
        output_file.loc[ind, '高兴-平静(吸引)标准差'] = df.iat[6, 3]
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
output_file.to_csv('task2数据结果.csv', encoding='GBK', index=False)
