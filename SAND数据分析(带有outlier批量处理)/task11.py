import pandas as pd
import numpy as np
import os
import time
import re

num_dict = {'1': ['_time1_Time_Perception', '_time1_'],
            '2': ['_time2_Time_Perception', '_time2_'],
            '3': ['_mother_Time_Perception', '_mother_'],
            '4': ['_father_Time_Perception', '_father_']}
sub_dict = '/11_Time_Perception'
now = time.localtime()
now = time.strftime("%Y_%m_%d_%H_%M%S", now)


def task11(info):
    print('测试十一开始处理')
    contempt = info[2].split('/')
    filename = contempt[-1] + num_dict[info[1]][0]
    file_name_list = os.listdir(info[2]+sub_dict)
    for i in file_name_list:
        if i.startswith(filename) & i.endswith('.csv'):
            filename = i
            break
        else:
            pass
    file_path = info[2] + sub_dict + '/' + filename
    data = pd.read_csv(file_path)
    expression = ['听觉', '视觉']
    aver = []
    std = []
    contempt = [['p', 'key_resp_12.rt'], ['p', 'key_resp_10.rt']]
    for i in contempt:
        data = pd.read_csv(file_path)
        df = data[i[1]] - data['p']
        df = df.loc[df.isnull() == False]
        q1 = df.quantile(q=0.25)
        q3 = df.quantile(q=0.75)
        # print(q1-1.5*(q3-q1))
        # print(q3+1.5*(q3-q1))
        # print(df)
        # print(df.loc[(q1-1.5*(q3-q1) < df) & (df < q3 + 1.5*(q3-q1))])
        df = df.loc[((q1-1.5*(q3-q1) < df) & (df < q3 + 1.5*(q3-q1)))]
        aver.append(round(np.mean(df), 4))
        std.append(round(np.std(df), 4))
    # 输出数据csv文件
    result = pd.DataFrame(columns=['误差时间(秒)', '标准差'], index=expression)
    result.index.name = '知觉'
    for i in range(2):
        result.loc[expression[i], '标准差'] = std[i]
        result.loc[expression[i], '误差时间(秒)'] = aver[i]
    # 将表格直接生成图片并输出csv文件
    from pandas.plotting import table
    import matplotlib.pyplot as plt
    plt.rcParams['font.sans-serif'] = ['KaiTi']  # 指定默认字体
    plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题
    fig = plt.figure(figsize=(8, 2), dpi=100)  # dpi表示清晰度
    ax = fig.add_subplot(111, frame_on=False)
    ax.xaxis.set_visible(False)  # hide the x axis
    ax.yaxis.set_visible(False)  # hide the y axis
    task4_table = table(ax, result, loc='center')  # 将df换成需要保存的dataframe即可
    cell_dict = task4_table.get_celld()
    for i in range(3):
        cell_dict[(i, 0)].set_width(0.2)
        cell_dict[(i, 1)].set_width(0.2)
    plt.savefig('task11_table.png')
    result['filename'] = filename
    output_name = info[0] + num_dict[info[1]][1] + '11_Time_Perception_' + now + '.csv'
    path = info[3] + "/" + output_name
    result.to_csv(path, encoding='utf-8_sig')
    # 绘图
    import matplotlib.pyplot as plt
    plt.clf()
    plt.style.use('ggplot')
    # 解决中文显示问题
    plt.rcParams['font.sans-serif'] = ['KaiTi']  # 指定默认字体
    plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题
    # 平均反应时
    fig = plt.figure()
    ax1 = fig.add_subplot(1, 1, 1)
    ax1.bar(expression, aver, align='center', color='darkblue', width=0.3)
    ax1.errorbar(x=expression, y=aver, yerr=std, ecolor='grey', capsize=4, color='black', fmt='o')
    ax1.xaxis.set_ticks_position("bottom")
    ax1.yaxis.set_ticks_position("left")
    plt.xlabel('Time_Perception')
    plt.ylabel('时间(秒)')
    plt.title('图1：误差时间（秒）')
    plt.savefig('task11_rt.png', dpi=100, bbox_inches='tight')
    plt.cla()
    plt.close("all")
    print('测试十一处理完成')

# task11(['卢思彤','1','D:/张以昊/张以昊/SAND数据/原始/2020_002_pat_lusitong','C:/Users/zhang/Desktop/新建文件夹'])

