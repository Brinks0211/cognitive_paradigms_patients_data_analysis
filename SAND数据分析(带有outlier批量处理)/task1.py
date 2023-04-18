import pandas as pd
import numpy as np
import os
import time
import re

num_dict = {'1': ['_time1_Facial_Emotion_Recognition', '_time1_'],
            '2': ['_time2_Facial_Emotion_Recognition', '_time2_'],
            '3': ['_mother_Facial_Emotion_Recognition', '_mother_'],
            '4': ['_father_Facial_Emotion_Recognition', '_father_']}
sub_dict = '/1_Facial_Emotion_Recognition'
now = time.localtime()
now = time.strftime("%Y_%m_%d_%H_%M%S", now)


def task1(info):
    print('测试一开始处理')
    contempt = info[2].split('/')
    filename = contempt[-1] + num_dict[info[1]][0]
    file_name_list = os.listdir(info[2]+sub_dict)
    for i in file_name_list:
        if  i.startswith(filename) & i.endswith('.csv'):
            filename = i
            break
        else:
            pass
    expri_time = filename.split('_')
    expri_time = '_'.join(expri_time[-3:])[:-4]
    file_path = info[2] + sub_dict + '/' + filename
    data = pd.read_csv(file_path, encoding='utf-8')
    expression = ['悲伤', '愤怒', '恐惧', '快乐', '厌恶', '中性']
    aver = []
    corr = []
    std = []
    for i in expression:
        df = data.loc[((data['s1'] == i) & (data['key_resp_face_1.corr'] == 1) |
                                (data['s1'] == i) & (data['key_resp_face_2.corr'] == 1) |
                                (data['s1'] == i) & (data['key_resp_3.corr'] == 1) |
                                (data['s1'] == i) & (data['key_resp_8.corr'] == 1))]
        df.fillna(value=0, inplace=True)
        df['rt'] = df['key_resp_face_1.rt'] + df['key_resp_face_2.rt'] + df['key_resp_3.rt'] + df['key_resp_8.rt']
        df['corr'] = df['key_resp_face_1.corr'] + df['key_resp_face_2.corr'] +\
                     df['key_resp_3.corr'] + df['key_resp_8.corr']
        q1 = df['rt'].quantile(q=0.25)
        q3 = df['rt'].quantile(q=0.75)
        # print(q1-1.5*(q3-q1))
        # print(q3+1.5*(q3-q1))
        # print(df)
        # print(df.loc[(q1-1.5*(q3-q1) < df['rt']) & (df['rt'] < q3 + 1.5*(q3-q1))])
        df = df.loc[(q1-1.5*(q3-q1) < df['rt']) & (df['rt'] < q3 + 1.5*(q3-q1))]
        # print(df)
        aver.append(round(np.mean(df['rt']), 4))
        std.append(round(np.std(df['rt']), 4))
        corr.append(round(df['corr'].value_counts()[1.0]/len(data.loc[data['s1'] == i])*100, 2))
    result = pd.DataFrame(columns=['反应时(秒)', '准确率', '标准差'], index=expression)
    result.index.name = '表情'
    for i in range(6):
        result.loc[expression[i], '标准差'] = std[i]
        result.loc[expression[i], '反应时(秒)'] = aver[i]
        result.loc[expression[i], '准确率'] = '{}%'.format(corr[i])
    # 将表格直接生成图片并输出csv文件
    from pandas.plotting import table
    import matplotlib.pyplot as plt
    plt.clf()
    plt.rcParams['font.sans-serif'] = ['KaiTi']  # 指定默认字体
    plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题
    fig = plt.figure(figsize=(5, 3), dpi=100)  # dpi表示清晰度
    ax = fig.add_subplot(111, frame_on=False)
    ax.xaxis.set_visible(False)  # hide the x axis
    ax.yaxis.set_visible(False)  # hide the y axis
    table(ax, result, loc='center')  # 将df换成需要保存的dataframe即可
    plt.savefig('task1_table.png')
    result['filename'] = filename
    output_name = info[0] + num_dict[info[1]][1] + '1_Facial_Emotion_Recognition_' + now + '.csv'
    path = info[3] + "/" + output_name
    result.to_csv(path, encoding='utf-8_sig')
    # 输出图片
    import matplotlib.pyplot as plt
    plt.style.use('ggplot')
    #解决中文显示问题
    plt.rcParams['font.sans-serif'] = ['KaiTi']  # 指定默认字体
    plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题
    # 平均反应时
    fig = plt.figure()
    ax1 = fig.add_subplot(1, 1, 1)
    ax1.bar(expression, aver, align='center', color='darkblue')
    ax1.errorbar(x=expression, y=aver, yerr=std, ecolor='grey', capsize=4, color='black', fmt='o')
    ax1.xaxis.set_ticks_position("bottom")
    ax1.yaxis.set_ticks_position("left")
    plt.xlabel('人类不同种类的情绪')
    plt.ylabel('时间(秒)')
    plt.title('图1：平均反应时间（秒）')
    plt.savefig('task1_rt.png', dpi=100, bbox_inches='tight')
    # 平均准确率
    fig1 = plt.figure()
    ax2 = fig1.add_subplot(1, 1, 1)
    ax2.bar(expression, corr, align='center', color='darkblue')
    ax2.xaxis.set_ticks_position("bottom")
    ax2.yaxis.set_ticks_position("left")
    plt.xlabel('人类不同种类的情绪')
    plt.ylabel('准确率（%）')
    plt.title('图2：平均准确率')
    plt.savefig('task1_corr.png', dpi=100, bbox_inches='tight')
    plt.cla()
    plt.close("all")
    print('测试一处理结束')
    return expri_time

