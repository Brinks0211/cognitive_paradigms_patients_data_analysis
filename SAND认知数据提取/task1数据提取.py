import os
import pandas as pd
import numpy as np
output_file = pd.DataFrame(columns=['悲伤反应时', '悲伤标准差', '悲伤正确率',
                                    '愤怒反应时', '愤怒标准差', '愤怒正确率',
                                    '恐惧反应时', '恐惧标准差', '恐惧正确率',
                                    '快乐反应时', '快乐标准差', '快乐正确率',
                                    '厌恶反应时', '厌恶标准差', '厌恶正确率',
                                    '中性反应时', '中性标准差', '中性正确率',
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
        if '1_Facial_Emotion_Recognition' in j:
            SRT.append(j)
    for j in SRT:
        lst = []
        filepath = sub_path + '/' + j
        df = pd.read_csv(filepath, encoding='utf-8')
        output_file.append(df.append(pd.Series(), ignore_index=True))
        output_file.loc[ind, '悲伤反应时'] = df.iat[0, 1]
        output_file.loc[ind, '悲伤正确率'] = df.iat[0, 2]
        output_file.loc[ind, '悲伤标准差'] = df.iat[0, 3]
        output_file.loc[ind, '愤怒反应时'] = df.iat[1, 1]
        output_file.loc[ind, '愤怒正确率'] = df.iat[1, 2]
        output_file.loc[ind, '愤怒标准差'] = df.iat[1, 3]
        output_file.loc[ind, '恐惧反应时'] = df.iat[2, 1]
        output_file.loc[ind, '恐惧正确率'] = df.iat[2, 2]
        output_file.loc[ind, '恐惧标准差'] = df.iat[2, 3]
        output_file.loc[ind, '快乐反应时'] = df.iat[3, 1]
        output_file.loc[ind, '快乐正确率'] = df.iat[3, 2]
        output_file.loc[ind, '快乐标准差'] = df.iat[3, 3]
        output_file.loc[ind, '厌恶反应时'] = df.iat[4, 1]
        output_file.loc[ind, '厌恶正确率'] = df.iat[4, 2]
        output_file.loc[ind, '厌恶标准差'] = df.iat[4, 3]
        output_file.loc[ind, '中性反应时'] = df.iat[5, 1]
        output_file.loc[ind, '中性正确率'] = df.iat[5, 2]
        output_file.loc[ind, '中性标准差'] = df.iat[5, 3]
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
output_file.to_csv('task1数据结果.csv', encoding='GBK', index=False)
