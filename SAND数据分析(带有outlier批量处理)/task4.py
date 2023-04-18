import pandas as pd
import numpy as np
import os
import time
import re

num_dict = {'1': ['_time1_Nback', '_time1_'],
            '2': ['_time2_Nback', '_time2_'],
            '3': ['_mother_Nback', '_mother_'],
            '4': ['_father_Nback', '_father_']}
sub_dict = '/4_Nback'
now = time.localtime()
now = time.strftime("%Y_%m_%d_%H_%M%S", now)


def task4(info):
    print('测试四开始处理')
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
    expression = ['0back', '1back', '2back']
    aver = []
    corr = []
    std = []
    # print(data['key_resp_0back.rt'])
    q1 = data['key_resp_0back.rt'].quantile(q=0.25)
    q3 = data['key_resp_0back.rt'].quantile(q=0.75)
    iqr = q3 - q1
    #print(q1,q3)
    #print(q1-1.5*iqr, q3 + 1.5*iqr)
    data = data.loc[(q1 - 1.5 * iqr < data['key_resp_0back.rt']) & (data['key_resp_0back.rt'] < q3 + 1.5 * iqr)]
    # print(data['key_resp_0back.rt'])
    aver.append(round(np.mean(data['key_resp_0back.rt']), 4))
    std.append(round(np.std(data['key_resp_0back.rt']), 4))
    corr.append(100)
    contempt = [['key_resp_1back.corr', 'key_resp_1back.rt'],
                ['key_resp_2back.corr', 'key_resp_2back.rt']]
    for i in contempt:
        data = pd.read_csv(file_path)
        df = data.loc[(data[i[0]] == 1) | (data[i[0]] == 0)]
        q1 = df[i[1]].quantile(q=0.25)
        q3 = df[i[1]].quantile(q=0.75)
        iqr = q3 - q1
        # print(df)
        # print(q1-1.5*iqr, q3 + 1.5*iqr)
        df = df.loc[(q1 - 1.5 * iqr < df[i[1]]) & (df[i[1]] < q3 + 1.5 * iqr) | df[i[1]].isnull()]
        # print(df)
        df_corr = df[i[0]].value_counts()
        corr.append(round(df_corr[1.0]/len(df.loc[(df[i[0]] == 0) | (df[i[0]] == 1)])*100, 2))
        aver.append(round(np.mean(df[i[1]]), 4))
        std.append(round(np.std(df[i[1]]), 4))
        # print(corr)
    # 输出数据csv文件
    result = pd.DataFrame(columns=['反应时(秒)', '准确率', '标准差'], index=expression)
    result.index.name = 'Nback'
    for i in range(3):
        result.loc[expression[i], '标准差'] = std[i]
        result.loc[expression[i], '反应时(秒)'] = aver[i]
        result.loc[expression[i], '准确率'] = '{}%'.format(corr[i])
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
    task4_table = table(ax, result, loc='center')  # 将df换成需要保存的dataframe即可
    cell_dict = task4_table.get_celld()
    for i in range(4):
        cell_dict[(i, 0)].set_width(0.15)
        cell_dict[(i, 1)].set_width(0.15)
        cell_dict[(i, 2)].set_width(0.15)
    plt.savefig('task4_table.png')
    result['filename'] = filename
    output_name = info[0] + num_dict[info[1]][1] + '4_Nback_' + now + '.csv'
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
    ax1.bar(expression, aver, align='center', color='darkblue', width=0.3)
    ax1.errorbar(x=expression, y=aver, yerr=std, ecolor='grey', capsize=4, color='black', fmt='o')
    # ax1.bar(expression,corratio,align='center',color='red')
    ax1.xaxis.set_ticks_position("bottom")
    ax1.yaxis.set_ticks_position("left")
    plt.xlabel('Nback')
    plt.ylabel('时间(秒)')
    plt.title('图1：平均反应时间（秒）')
    plt.savefig('task4_rt.png', dpi=100, bbox_inches='tight')
    # 平均准确率
    fig1 = plt.figure()
    ax2 = fig1.add_subplot(1, 1, 1)
    ax2.bar(expression, corr, align='center', color='darkblue', width=0.3)
    ax2.xaxis.set_ticks_position("bottom")
    ax2.yaxis.set_ticks_position("left")
    plt.xlabel('Nback')
    plt.ylabel('准确率（%）')
    plt.title('图2：平均准确率')
    plt.savefig('task4_corr.png', dpi=100, bbox_inches='tight')
    plt.cla()
    plt.close("all")
    print('测试四处理结束')


