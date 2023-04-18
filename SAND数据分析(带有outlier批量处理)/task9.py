import pandas as pd
import numpy as np
import csv
import os
import time
import re

num_dict = {'1': ['_time1_Simple_Guessing_Task', '_time1_'],
            '2': ['_time2_Simple_Guessing_Task', '_time2_'],
            '3': ['_mother_Simple_Guessing_Task', '_mother_'],
            '4': ['_father_Simple_Guessing_Task', '_father_']}
sub_dict = '/9_Simple_Guessing_Task'
now = time.localtime()
now = time.strftime("%Y_%m_%d_%H_%M%S", now)
def task9(info):
    print('测试九开始处理')
    contempt = info[2].split('/')
    filename = contempt[-1] + num_dict[info[1]][0]
    file_name_list = os.listdir(info[2]+sub_dict)
    for i in file_name_list:
        if  i.startswith(filename) & i.endswith('.csv'):
            filename = i
            break
        else:
            pass
    # print(filename)
    file_path = info[2] + sub_dict + '/' + filename
    # 文件数据读取
    f = open(file_path, 'r', encoding='utf-8')
    filereader = csv.reader(f)
    sentence = []
    rt = []
    for i, line in enumerate(filereader):
        if i == 0:
            for j in range(len(line)):
                if line[j] == 'fdb2':
                    sentence_num = j
                if line[j] == 'key_resp_formal1.rt':
                    rt_num = j
        if line[sentence_num] == '恭喜你，猜对了！' or line[sentence_num] == '很遗憾，你猜错了。':
            sentence.append(str(line[sentence_num]).strip())
        try:
            rt.append(eval(str(line[rt_num]).strip()))
        except:
            pass

    # 求反应时平均值及方差
    def aver(data):
        raw_rt = []
        for i in range(len(data)):
            raw_rt.append(float(data[i]))
        aver = np.mean(raw_rt)
        std1 = np.std(raw_rt)
        return aver, std1
    def chunks(arr, n):
        return [arr[i:i + n] for i in range(0, len(arr), n)]
    rt = chunks(rt, 16)
    sentence = chunks(sentence, 16)
    def select(sen_data, rt_data):
        rt_right = []
        rt_wrong = []
        for i in range(len(sen_data) - 1):
            if sen_data[i] == '恭喜你，猜对了！':
                rt_right.append(rt_data[i + 1])
            if sen_data[i] == '很遗憾，你猜错了。':
                rt_wrong.append(rt_data[i + 1])
        aver_right, std_right = aver(rt_right)
        aver_wrong, std_wrong = aver(rt_wrong)
        return aver_right, std_right, aver_wrong, std_wrong
    reacttime_right = []
    reacttime_wrong = []
    std_right = []
    std_wrong = []
    for i in range(len(sentence)):
        aver1, std1, aver2, std2 = select(sentence[i], rt[i])
        reacttime_right.append(aver1)
        reacttime_wrong.append(aver2)
        std_right.append(std1)
        std_wrong.append(std2)
    total = ['阶段1', '阶段2', '阶段3', '阶段4']
    total_right = ['阶段1获利', '阶段2获利', '阶段3获利', '阶段4获利']
    total_wrong = ['阶段1损失', '阶段2损失', '阶段3损失', "阶段4损失"]
    x = range(len(total))
    # 绘图
    import matplotlib.pyplot as plt
    plt.clf()
    total_index = len(total)
    plt.style.use('ggplot')
    # 解决中文显示问题
    plt.rcParams['font.sans-serif'] = ['KaiTi']  # 指定默认字体
    plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题
    # 平均反应时
    fig = plt.figure()
    bar_width = '   '
    aver_s = np.array(reacttime_right)
    aver_o = np.array(reacttime_wrong)
    ax1 = fig.add_subplot(1, 1, 1)
    ax1.bar(x, aver_s, width=0.4, color='darkblue', label='获利后下次反应时')
    ax1.errorbar(x, y=aver_s, yerr=std_right, ecolor='grey', capsize=4, color='black', fmt='o')
    ax1.bar([i + 0.4 for i in x], aver_o, width=0.4, color='red', label='损失后下次反应时')
    ax1.errorbar([i + 0.4 for i in x], y=aver_o, yerr=std_wrong, ecolor='grey', capsize=4, color='black', fmt='o')
    plt.xticks([i + 0.2 for i in x], total, fontsize=10)
    ax1.xaxis.set_ticks_position("bottom")
    ax1.yaxis.set_ticks_position("left")
    plt.xlabel('不同阶段')
    plt.ylabel('时间(秒)')
    plt.title('图1：平均反应时间（秒）')
    plt.legend()
    plt.savefig('task9_rt.png', dpi=100, bbox_inches='tight')
    # 输出数据csv文件
    expression = ['阶段1获利', '阶段1损失', '阶段2获利', '阶段2损失',
                  '阶段3获利', '阶段3损失', '阶段4获利', '阶段4损失']
    aver = []
    std = []
    for i in range(4):
        aver.append(round(reacttime_right[i], 4))
        aver.append(round(reacttime_wrong[i], 4))
        std.append(round(std_right[i], 4))
        std.append(round(std_wrong[i], 4))
    result = pd.DataFrame(columns=['反应时(秒)', '标准差'], index=expression)
    result.index.name = '不同阶段'
    for i in range(8):
        result.loc[expression[i], '标准差'] = std[i]
        result.loc[expression[i], '反应时(秒)'] = aver[i]
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
    for i in range(9):
        cell_dict[(i, 0)].set_width(0.15)
        cell_dict[(i, 1)].set_width(0.15)
    plt.savefig('task9_table.png')
    result['filename'] = filename
    output_name = info[0] + num_dict[info[1]][1] + '9_Simple_Guessing_Task_' + now + '.csv'
    path = info[3] + "/" + output_name
    result.to_csv(path, encoding='utf-8_sig')
    plt.cla()
    plt.close("all")
    print('测试九处理结束')

