import pandas as pd
import numpy as np
import os
import time
import re

num_dict = {'1': ['_time1_Delay_Discounting_Task', '_time1_'],
            '2': ['_time2_Delay_Discounting_Task', '_time2_'],
            '3': ['_mother_Delay_Discounting_Task', '_mother_'],
            '4': ['_father_Delay_Discounting_Task', '_father_']}
sub_dict = '/10_Delay_Discounting_Task'
now = time.localtime()
now = time.strftime("%Y_%m_%d_%H_%M%S", now)


def task10(info):
    print('测试十开始处理')
    contempt = info[2].split('/')
    filename = contempt[-1] + num_dict[info[1]][0]
    file_name_list = os.listdir(info[2]+sub_dict)
    for i in file_name_list:
        if  i.startswith(filename) & i.endswith('.csv'):
            filename = i
            break
        else:
            pass
    file_path = info[2] + sub_dict + '/' + filename
    data = pd.read_csv(file_path)
    expression = ['一周', '两周', '一个月', '六个月', '一年', '五年', '二十五年']
    contempt = ['key_resp_1week.keys', 'key_resp_2weeks.keys', 'key_resp_1month.keys', 'key_resp_6months.keys',
                'key_resp_1year.keys', 'key_resp5years.keys', 'key_resp25years.keys']
    def expected(data):
        x = 500
        y = 4
        for i in data:
            if i == 'left':
                x -= 1000 / y
            if i == 'right':
                x += 1000 / y
            y *= 2
        return x
    expect = []
    k = []
    A = 1000
    timesep = [0.25, 0.5, 1, 2, 6, 60, 300]
    for index, i in enumerate(contempt):
        df = data[data[i].notnull()][i]
        V = round(expected(df), 4)
        # print(index, i, A)
        D = timesep[index]
        k_temp = (A / V - 1) / D
        # print(k)
        k.append(k_temp)
        expect.append(V)
    # 输出数据csv文件
    result = pd.DataFrame(columns=['即时获得金币(对比1000金币)', '延迟折扣率'], index=expression)
    result.index.name = '延迟时间'
    for i in range(7):
        result.loc[expression[i], '即时获得金币(对比1000金币)'] = expect[i]
        result.loc[expression[i], '延迟折扣率'] = k[i]
    # 将表格直接生成图片并输出csv文件
    from pandas.plotting import table
    import matplotlib.pyplot as plt
    plt.clf()
    plt.rcParams['font.sans-serif'] = ['KaiTi']  # 指定默认字体
    plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题
    fig = plt.figure(figsize=(8, 2), dpi=100)  # dpi表示清晰度
    ax = fig.add_subplot(111, frame_on=False)
    ax.xaxis.set_visible(False)  # hide the x axis
    ax.yaxis.set_visible(False)  # hide the y axis
    task_table = table(ax, result, loc='center')  # 将df换成需要保存的dataframe即可
    cell_dict = task_table.get_celld()
    for i in range(8):
        cell_dict[(i, 0)].set_width(0.4)
    plt.savefig('task10_table.png')
    result['filename'] = filename
    output_name = info[0] + num_dict[info[1]][1] + '10_Delay_Discounting_Task_' + now + '.csv'
    path = info[3] + "/" + output_name
    result.to_csv(path, encoding='utf-8_sig')
    # 绘图
    import matplotlib.pyplot as plt
    plt.style.use('ggplot')
    # 解决中文显示问题
    plt.rcParams['font.sans-serif'] = ['KaiTi']  # 指定默认字体
    plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题
    # 平均反应时
    fig = plt.figure()
    ax1 = fig.add_subplot(1, 1, 1)
    ax1.bar(expression, expect, align='center', color='darkblue', width=0.3)
    ax1.xaxis.set_ticks_position("bottom")
    ax1.yaxis.set_ticks_position("left")
    plt.xlabel('延迟时间')
    plt.ylabel('金币数')
    plt.title('图1：预期期望')
    plt.savefig('task10_rt.png', dpi=100, bbox_inches='tight')
    # 延时折扣率
    fig = plt.figure()
    ax1 = fig.add_subplot(1, 1, 1)
    ax1.bar(expression, k, align='center', color='darkblue', width=0.3)
    ax1.xaxis.set_ticks_position("bottom")
    ax1.yaxis.set_ticks_position("left")
    plt.xlabel('延迟时间')
    plt.ylabel('延时折扣率')
    plt.title('图2：延时折扣率')
    plt.savefig('task10_corr.png', dpi=100, bbox_inches='tight')
    plt.cla()
    plt.close("all")
    print('测试十处理结束')
