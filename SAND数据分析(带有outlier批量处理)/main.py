import tkinter as tk
import time
import os
from fpdf import FPDF
from task1 import task1
from task2 import task2
from task3 import task3
from task4 import task4
from task5 import task5
from task6 import task6
from task7 import task7
from task8 import task8
from task9 import task9
from task10 import task10
from task11 import task11
from tkinter.filedialog import *
now = time.localtime()
now = time.strftime("%Y_%m_%d_%H_%M%S", now)
task1_expri_time = '测试时间缺失'
# # GUI
# root = tk.Tk()
# root.wm_title("数据处理")
# root.geometry("850x250+370+270")
# path = tk.StringVar()
# path_dict = tk.StringVar()
# w0 = tk.Label(root, text='SAND认知行为测试报告', width=40, font='fangsong 15 bold')
# w0.place(x=200, y=10)
# w1 = tk.Label(root, text='姓名：').place(x=10, y=60)
# name = tk.Entry(root, width=60)
# name.place(x=300, y=60)
# w2 = tk.Label(root, text="测试次数（1:time1;2:time2;3:mother;4:father）").place(x=10, y=90)
# times = tk.Entry(root, width=60)
# times.place(x=300, y=90)
# w3 = tk.Label(root, text='文件路径：').place(x=10, y=120)
# path1 = tk.Entry(root, textvariable=path, width=60)
# path1.place(x=300, y=120)
# w4 = tk.Label(root, text='报告输出路径：').place(x=10, y=150)
# path2 = tk.Entry(root, textvariable=path_dict, width=60)
# path2.place(x=300, y=150)


# def select_path():
#     path_ = askdirectory()
#     path.set(path_)
#
#
# def select_dict():
#     path2 = askdirectory()
#     path_dict.set(path2)
#
#
# def filepath_get():
#     global dict_name, times, name, output_dict
#     name = name.get()
#     times = times.get()
#     dict_name = path1.get()
#     output_dict = path2.get()
#     root.withdraw()
#     root.destroy()
#
#
# b1 = tk.Button(root, text='开始输出报告', font=('song', 12), width=20, command=filepath_get)
# b1.place(x=350, y=200)
# b2 = tk.Button(root, text="选择数据文件夹", font=('song', 10), width=15, height=1, command=select_path)
# b2.place(x=730, y=120)
# b3 = tk.Button(root, text="选择输出文件夹", font=('song', 10), width=15, height=1, command=select_dict)
# b3.place(x=730, y=150)
# root.mainloop()
import os
names = os.listdir(r'D:\张以昊\课题组\数据\认知_MDD\CON控制组认知数据结果') #放原始数据路径
for i in names:
    name = i
    times = '4' #根据自己要跑的类型（time1, time2, mother, father ）选择
    dict_name =r'D:\张以昊\课题组\数据\认知_MDD\CON控制组认知数据结果' #放原始数据路径
    output_dict = r'C:/Users/zhang/Desktop/father'  #自己建一个新的结果文件夹并把路径放入
    # num_dict = {'1': [name, '_time1_'], '2': [name+'(复查)', '_time2_'],
    #             '3': [name+'(母亲)', '_mother_'], '4': [name+'(父亲)', '_father_']}
    num_dict = {'1': [name, '_time1_'], '2': [name, '_time2_'],
                '3': [name, '_mother_'], '4': [name, '_father_']}
    if os.path.exists(output_dict + '/' + num_dict[times][0]):
        pass
    else:
        os.mkdir(output_dict + '/' + num_dict[times][0])
    output_dict = output_dict + '/' + num_dict[times][0]
    dict_name = dict_name + '/' + i
    info = [num_dict[times][0], times, dict_name, output_dict]
    output_path = output_dict + '/' + info[0] + num_dict[times][1] + now + '.pdf'

    # 只跑数据不输出pdf
    # try:task1_expri_time = task1(info)
    # except:pass
    # try:task2(info)
    # except:task3(info)
    # try:task4(info)
    # except:pass
    # try:task5(info)
    # except:pass
    # try:task6(info)
    # except:pass
    # try:task7(info)
    # except:pass
    # try:task8(info)
    # except:pass
    # try:task9(info)
    # except:pass
    # try:task10(info)
    # except:pass
    # try:task11(info)
    # except:pass


    # 执行子文件函数，输出csv，返回结果Dataframe和实验日期
    class PDF(FPDF):
        # Page footer
        def footer(self):
            pdf.image('sdnu_logo.png', 150, 8, 50)
            # Position at 1.5 cm from bottom
            self.set_y(-10)
            # Arial italic 8
            self.set_font('Arial', 'I', 8)
            # Page number
            self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')
    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.add_font('song', fname='STSONG.TTF', uni=True)
    pdf.set_font('song', size=15)
    pdf.cell(60)
    pdf.cell(60, 10, '电脑认知测试报告', 0, 1, 'C')
    pdf.ln(2)
    pdf.set_font('song', size=10)
    pdf.cell(115, 5, txt='姓名：'+info[0], border=0, ln=0, align='C')
    try:
        task1_expri_time = task1(info)
    except:
        pdf.cell(115, 5, txt='测试时间：' + task1_expri_time, border=0, ln=1, )
        pdf.ln(2)
        pdf.cell(60, 5, txt='电脑认知测试一：面孔情绪识别能力', border=1, ln=1)
        pdf.ln(15)
        pdf.cell(60, 5, txt='测试数据确缺失', border=0, ln=1)
        pdf.ln(15)
    else:
        pdf.cell(115, 5, txt='测试时间：' + task1_expri_time, border=0, ln=1, )
        pdf.ln(2)
        pdf.cell(60, 5, txt='电脑认知测试一：面孔情绪识别能力', border=1, ln=1)
        pdf.image('task1_table.png', x=10, y=35, w=70, h=42)
        pdf.image('task1_rt.png', x=90, y=35, w=45, h=36)
        pdf.image('task1_corr.png', x=150, y=35, w=45, h=36)
        pdf.ln(35)
        os.remove('task1_corr.png')
        os.remove('task1_rt.png')
        os.remove('task1_table.png')
    pdf.cell(52, 5, txt='电脑认知测试二：注意探测能力', border=1, ln=1)
    try:
        task2(info)
    except:
        pdf.ln(15)
        pdf.cell(60, 5, txt='测试数据确缺失', border=0, ln=1)
        pdf.ln(15)
    else:
        pdf.image('task2_table.png', x=-15, y=75, w=140, h=42)
        pdf.image('task2_rt.png', x=90, y=75, w=45, h=36)
        pdf.image('task2_corr.png', x=150, y=75, w=45, h=36)
        pdf.ln(35)
        os.remove('task2_corr.png')
        os.remove('task2_rt.png')
        os.remove('task2_table.png')
    pdf.cell(52, 5, txt='电脑认知测试三：注意探测能力', border=1, ln=1)
    try:
        task3(info)
    except:
        pdf.ln(15)
        pdf.cell(60, 5, txt='测试数据确缺失', border=0, ln=1)
        pdf.ln(15)
    else:
        pdf.image('task3_table.png', x=-15, y=115, w=112, h=42)
        pdf.image('task3_rt.png', x=90, y=115, w=45, h=36)
        pdf.image('task3_corr.png', x=150, y=115, w=45, h=36)
        pdf.ln(35)
        os.remove('task3_corr.png')
        os.remove('task3_rt.png')
        os.remove('task3_table.png')
    pdf.cell(52, 5, txt='电脑认知测试四：短时记忆能力', border=1, ln=1)
    try:
        task4(info)
    except:
        pdf.ln(13)
        pdf.cell(60, 5, txt='测试数据确缺失', border=0, ln=1)
        pdf.ln(14)
    else:
        pdf.image('task4_table.png', x=-15, y=155, w=112, h=28)
        pdf.image('task4_rt.png', x=90, y=155, w=45, h=36)
        pdf.image('task4_corr.png', x=150, y=155, w=45, h=36)
        pdf.ln(32)
        os.remove('task4_corr.png')
        os.remove('task4_rt.png')
        os.remove('task4_table.png')
    pdf.cell(52, 5, txt='电脑认知测试五：冲突解决能力', border=1, ln=1)
    try:
        task5(info)
    except:
        pdf.ln(15)
        pdf.cell(60, 5, txt='测试数据确缺失', border=0, ln=1)
        pdf.ln(15)
    else:
        pdf.image('task5_table.png', x=-15, y=195, w=112, h=28)
        pdf.image('task5_rt.png', x=90, y=195, w=45, h=36)
        pdf.image('task5_corr.png', x=150, y=195, w=45, h=36)
        pdf.ln(35)
        os.remove('task5_corr.png')
        os.remove('task5_rt.png')
        os.remove('task5_table.png')
    pdf.cell(52, 5, txt='电脑认知测试六：空间识别能力', border=1, ln=1)
    try:
        task6(info)
    except:
        pdf.ln(15)
        pdf.cell(60, 5, txt='测试数据确缺失', border=0, ln=1)
        pdf.ln(15)
    else:
        pdf.image('task6_table.png', x=-15, y=235, w=112, h=28)
        pdf.image('task6_rt.png', x=90, y=235, w=45, h=36)
        pdf.image('task6_corr.png', x=150, y=235, w=45, h=36)
        os.remove('task6_corr.png')
        os.remove('task6_rt.png')
        os.remove('task6_table.png')
    pdf.add_page()
    pdf.ln(10)
    pdf.cell(59, 5, txt='电脑认知测试七：空间冲突解决能力', border=1, ln=1)
    try:
        task7(info)
    except:
        pdf.ln(13)
        pdf.cell(60, 5, txt='测试数据确缺失', border=0, ln=1)
        pdf.ln(14)
    else:
        pdf.image('task7_table.png', x=-15, y=28, w=112, h=28)
        pdf.image('task7_rt.png', x=90, y=20, w=45, h=36)
        pdf.image('task7_corr.png', x=150, y=20, w=45, h=36)
        pdf.ln(32)
        os.remove('task7_corr.png')
        os.remove('task7_rt.png')
        os.remove('task7_table.png')
    pdf.cell(52, 5, txt='电脑认知测试八：任务切换能力', border=1, ln=1)
    try:
        task8(info)
    except:
        pdf.ln(13)
        pdf.cell(60, 5, txt='测试数据确缺失', border=0, ln=1)
        pdf.ln(14)
    else:
        pdf.image('task8_table.png', x=-15, y=65, w=112, h=28)
        pdf.image('task8_rt.png', x=90, y=60, w=45, h=36)
        pdf.image('task8_corr.png', x=150, y=60, w=45, h=36)
        pdf.ln(32)
        os.remove('task8_corr.png')
        os.remove('task8_rt.png')
        os.remove('task8_table.png')
    pdf.cell(52, 5, txt='电脑认知测试九：奖赏反应情况', border=1, ln=1)
    try:
        task9(info)
    except:
        pdf.ln(15)
        pdf.cell(60, 5, txt='测试数据确缺失', border=0, ln=1)
        pdf.ln(15)
    else:
        pdf.image('task9_table.png', x=-15, y=105, w=112, h=28)
        pdf.image('task9_rt.png', x=150, y=60, w=45, h=36)
        pdf.ln(35)
        os.remove('task9_rt.png')
        os.remove('task9_table.png')
    pdf.cell(52, 5, txt='电脑认知测试十：延迟满足能力', border=1, ln=1)
    try:
        task10(info)
    except:
        pdf.ln(15)
        pdf.cell(60, 5, txt='测试数据确缺失', border=0, ln=1)
        pdf.ln(15)
    else:
        pdf.image('task10_table.png', x=-5, y=145, w=112, h=28)
        pdf.image('task10_rt.png', x=90, y=140, w=45, h=36)
        pdf.image('task10_corr.png', x=150, y=140, w=45, h=36)
        pdf.ln(35)
        os.remove('task10_rt.png')
        os.remove('task10_corr.png')
        os.remove('task10_table.png')
    pdf.cell(78, 5, txt='电脑认知测试十一：视觉和听觉的时间知觉能力', border=1, ln=1)
    try:
        task11(info)
    except:
        pdf.ln(15)
        pdf.cell(60, 5, txt='测试数据确缺失', border=0, ln=1)
        pdf.ln(15)
    else:
        pdf.image('task11_table.png', x=-15, y=185, w=112, h=28)
        pdf.image('task11_rt.png', x=90, y=180, w=45, h=36)
        os.remove('task11_rt.png')
        os.remove('task11_table.png')
    print('正在打印pdf')
    pdf.output(output_path)

# import tkinter as tk
# def quit(root):
#     root.destroy()
# root=tk.Tk()
# root.title('提示')
# root.geometry('300x170+600+300')
# w1 = tk.Label(root, text='测试数据已处理完成', font='黑体 15 ')
# w1.pack(pady=30)
# b1 = tk.Button(root, text='确定', font='song 11', width=15, command=lambda root=root: quit(root))
# b1.pack(anchor='center', pady=10)
# root.mainloop()
