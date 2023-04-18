import pandas as pd
import numpy as np
import os
import time
import re

num_dict = {'1': ['_time1_Dot_Probe', '_time1_'],
            '2': ['_time2_Dot_Probe', '_time2_'],
            '3': ['_mother_Dot_Probe', '_mother_'],
            '4': ['_father_Dot_Probe', '_father_']}
sub_dict = '/2_Dot_Probe'
now = time.localtime()
now = time.strftime("%Y_%m_%d_%H_%M%S", now)


def task2(info):
    print('测试二开始处理')
    contempt = info[2].split('/')
    filename = contempt[-1] + num_dict[info[1]][0]
    file_name_list = os.listdir(info[2]+sub_dict)
    for i in file_name_list:
        if  i.startswith(filename) & i.endswith('.csv'):
            filename = i
            break
        else:
            pass
    expri_time = filename[-20: -4]
    file_path = info[2] + sub_dict + '/' + filename
    data = pd.read_csv(file_path)
    # data = data.astype({'type1': 'str', 'type2': 'str', 'j': 'str'})
    expression = ['平静-平静', '悲伤(吸引)-高兴', '悲伤-高兴(吸引)', '悲伤(吸引)-平静',
                  '悲伤-平静(吸引)', '高兴(吸引)-平静', '高兴-平静(吸引)']
    contempt = [['s', 'h', 'left', 'h', 's', 'right'], ['s', 'h', 'right', 'h', 's', 'left'],
                ['s', 'n', 'left', 'n', 's', 'right'], ['s', 'n', 'right', 'n', 's', 'left'],
                ['h', 'n', 'left', 'n', 'h', 'right'], ['h', 'n', 'right', 'n', 'h', 'left']]
    aver = []
    corr = []
    std = []
    # n n
    df = data[data['type1'].str.startswith('n', na=False) & data['type2'].str.startswith('n', na=False) &
              (data['key_resp_trial_1.corr'] == 1) | data['type1'].str.startswith('n', na=False) &
              data['type2'].str.startswith('n', na=False) & (data['key_resp_trial_2.corr'] == 1)]
    df_con = data[data['type1'].str.startswith('n', na=False) & data['type2'].str.startswith('n', na=False)]
    df.fillna(value=0, inplace=True)
    df_con.fillna(value=0, inplace=True)
    df['rt'] = df['key_resp_trial_1.rt'] + df['key_resp_trial_2.rt']
    df['corr'] = df['key_resp_trial_1.corr'] + df['key_resp_trial_2.corr']
    df_con['corr'] = df_con['key_resp_trial_1.corr'] + df_con['key_resp_trial_2.corr']
    aver.append(round(np.mean(df['rt']), 4))
    std.append(round(np.std(df['rt']), 4))
    corr.append(round(df['corr'].value_counts()[1.0] / len(df_con['corr'])*100, 2))
    data['key_resp_trial_1.corr'].fillna(value=0, inplace=True)
    data['key_resp_trial_2.corr'].fillna(value=0, inplace=True)
    data['corr'] = data['key_resp_trial_1.corr'] + data['key_resp_trial_2.corr']
    for i in contempt:

        df = data[(data['type1'].str.startswith(i[0], na=False)) & (data['type2'].str.startswith(i[1], na=False)) &
                  (data['j'] == i[2]) & (data['corr'] == 1) | (data['type1'].str.startswith(i[3], na=False)) &
                  (data['type2'].str.startswith(i[4], na=False)) & (data['j'] == i[5]) & (data['corr'] == 1)]
        df_con = data[data['type1'].str.startswith(i[0], na=False) & data['type2'].str.startswith(i[1], na=False) &
                      (data['j'] == i[2]) | data['type1'].str.startswith(i[3], na=False) &
                      data['type2'].str.startswith(i[4], na=False) & (data['j'] == i[5])]
        df.fillna(value=0, inplace=True)
        df['rt'] = df['key_resp_trial_1.rt'] + df['key_resp_trial_2.rt']
        df['corr'] = df['key_resp_trial_1.corr'] + df['key_resp_trial_2.corr']
        df_con['corr'] = df_con['key_resp_trial_1.corr'] + df_con['key_resp_trial_2.corr']
        aver.append(round(np.mean(df['rt']), 4))
        std.append(round(np.std(df['rt']), 4))
        corr.append(round(df['corr'].value_counts()[1.0] / len(df_con['corr'])*100, 2))
    # 输出数据csv文件
    result = pd.DataFrame(columns=['反应时(秒)', '准确率', '标准差'], index=expression)
    result.index.name = '表情'
    for i in range(7):
        result.loc[expression[i], '标准差'] = std[i]
        result.loc[expression[i], '反应时(秒)'] = aver[i]
        result.loc[expression[i], '准确率'] = '{}%'.format(corr[i])
    # 将表格直接生成图片并输出csv文件
    from pandas.plotting import table
    import matplotlib.pyplot as plt
    plt.clf()
    plt.rcParams['font.sans-serif'] = ['KaiTi']  # 指定默认字体
    plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题
    fig = plt.figure(figsize=(10, 3), dpi=100)  # dpi表示清晰度
    ax = fig.add_subplot(111, frame_on=False)
    ax.xaxis.set_visible(False)  # hide the x axis
    ax.yaxis.set_visible(False)  # hide the y axis
    task2_table = table(ax, result, loc='center')  # 将df换成需要保存的dataframe即可
    cell_dict = task2_table.get_celld()
    for i in range(8):
        cell_dict[(i, 0)].set_width(0.15)
        cell_dict[(i, 1)].set_width(0.15)
        cell_dict[(i, 2)].set_width(0.15)
    plt.savefig('task2_table.png')
    result['filename'] = filename
    output_name = info[0] + num_dict[info[1]][1] + '2_Dot_Probe_' + now + '.csv'
    path = info[3] + "/" + output_name
    result.to_csv(path, encoding='utf-8_sig')
    # 绘图
    expression = ['平静——平静', '悲伤——高兴', '悲伤——平静', '高兴——平静']
    x = range(len(expression))
    aver_s = aver[::2]
    aver_o = aver[1::2]
    std_s = std[:: 2]
    std_o = std[1:: 2]
    corr_s = corr[:: 2]
    corr_o = corr[1:: 2]
    aver_o.insert(0, 0)
    std_o.insert(0, 0)
    corr_o.insert(0, 0)
    import matplotlib.pyplot as plt
    expression_index = len(expression)
    plt.style.use('ggplot')
    # 解决中文显示问题
    plt.rcParams['font.sans-serif'] = ['KaiTi']  # 指定默认字体
    plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题
    # 平均反应时
    fig = plt.figure()
    bar_width = '   '
    aver_s = np.array(aver_s)
    aver_o = np.array(aver_o)
    ax1 = fig.add_subplot(1, 1, 1)
    ax1.bar(x, aver_s, width=0.4, color='darkblue', label='前者吸引')
    ax1.errorbar(x, y=aver_s, yerr=std_s, ecolor='grey', capsize=4, color='black', fmt='o')
    ax1.bar([i + 0.4 for i in x], aver_o, width=0.4, color='red', label='后者吸引')
    ax1.errorbar([i + 0.4 for i in x], y=aver_o, yerr=std_o, ecolor='grey', capsize=4, color='black', fmt='o')
    # ax1.bar(expression,corratio,align='center',color='red')
    plt.xticks([i + 0.2 for i in x], expression, fontsize=10)
    ax1.xaxis.set_ticks_position("bottom")
    ax1.yaxis.set_ticks_position("left")
    plt.xlabel('人类不同种类的情绪')
    plt.ylabel('时间(秒)')
    plt.title('图1：平均反应时间（秒）')
    plt.legend()
    plt.savefig('task2_rt.png', dpi=100, bbox_inches='tight')
    # 平均准确率
    fig1 = plt.figure()
    ax2 = fig1.add_subplot(1, 1, 1)
    ax2.bar(x, corr_s, color='darkblue', label='前者吸引', width=0.4)
    ax2.bar([i + 0.4 for i in x], corr_o, color='red', label='后者吸引', width=0.4)
    plt.xticks([i + 0.2 for i in x], expression, fontsize=10)
    ax2.xaxis.set_ticks_position("bottom")
    ax2.yaxis.set_ticks_position("left")
    plt.xlabel('人类不同种类的情绪')
    plt.ylabel('准确率（%）')
    plt.title('图2：平均准确率')
    plt.legend()
    plt.savefig('task2_corr.png', dpi=100, bbox_inches='tight')
    plt.cla()
    plt.close("all")
    print('测试二处理结束')
