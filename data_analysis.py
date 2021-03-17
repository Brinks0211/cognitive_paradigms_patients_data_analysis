import csv
import numpy
import tkinter as tk
import time
import fpdf
import os
import re
from tkinter.filedialog import *
reacttime=[]
corratio=[]
Standard_Deviation=[]
datalist=[]
# GUI
root=tk.Tk()
root.wm_title("数据处理")
root.geometry("850x250+370+270")
path=tk.StringVar()
path_dict=tk.StringVar()
w0=tk.Label(root,text='数据处理',width=40,font='fangsong 15 bold')
w0.place(x=200,y=10)
w1=tk.Label(root,text='姓名：').place(x=10,y=60)
name=tk.Entry(root,width=60)
name.place(x=300,y=60)
w2=tk.Label(root,text="测试次数（1:time1;2:time2;3:mother;4:father）").place(x=10,y=90)
times=tk.Entry(root,width=60)
times.place(x=300,y=90)
w3=tk.Label(root,text='文件路径：').place(x=10,y=120)
path1=tk.Entry(root,textvariable=path,width=60)
path1.place(x=300,y=120)
w4=tk.Label(root,text='报告输出路径：').place(x=10,y=150)
path2=tk.Entry(root,textvariable=path_dict,width=60)
path2.place(x=300,y=150)
def selectpath():
    path_ = askdirectory()
    path.set(path_)
def selectdict():
    path2 = askdirectory()
    path_dict.set(path2)
def filepathget():
    global filename,times,name,dictname
    name=name.get()
    times=times.get()
    filename=path1.get()
    dictname=path2.get()
    root.withdraw()
    root.destroy()
b1 = tk.Button(root, text='开始输出报告', font=('song', 12), width=20,command=filepathget)
b1.place(x=350,y=200)
b2 = tk.Button(root,text="选择数据文件夹",font=('song',10),width=15,height=1,command=selectpath)
b2.place(x=730,y=120)
b3 = tk.Button(root,text="选择输出文件夹",font=('song',10),width=15,height=1,command=selectdict)
b3.place(x=730,y=150)
root.mainloop()
filename1=filename.split('/')
print("测试一文件开始处理。")
# 文件数据读取
if times == '1':
    filename=filename1[-1]+'_time1_Facial_Emotion_Recognition'
elif times == '2':
    filename = filename1[-1]+'_time2_Facial_Emotion_Recognition'
elif times == '3':
    filename = filename1[-1]+'_mother_Facial_Emotion_Recognition'
elif times == '4':
    filename = filename1[-1] + '_father_Facial_Emotion_Recognition'
else:
    filename = filename1[-1] + '_time1_Facial_Emotion_Recognition'

for files in os.listdir('/'.join(filename1) + '/1_Facial_Emotion_Recognition/'):
    if filename in files and '.csv' in files:
        expri_time=files[-20:-4]
        filename='/'.join(filename1) + '/1_Facial_Emotion_Recognition/'+files

f = open(filename, 'r', encoding='utf-8')
filereader = csv.reader(f)
expression=[]
rt_total=[]
corr_total=[]
global rt_light_num
for i,line in enumerate(filereader):
    if i==0:
        for j in range(len(line)):
            if line[j] == 's1':
                expression_num=j
            if line[j] == 'key_resp_face_1.corr':
                corr1_num=j
            if line[j] == 'key_resp_face_1.rt':
                rt1_num =j
            if line[j] == 'key_resp_face_2.corr':
                corr2_num = j
            if line[j] == 'key_resp_face_2.rt':
                rt2_num = j
            if line[j] == 'key_resp_3.corr':
                corr3_num = j
            if line[j] == 'key_resp_3.rt':
                rt3_num = j
            if line[j] == 'key_resp_8.corr':
                corr4_num =j
            if line[j] == 'key_resp_8.rt':
                rt4_num = j
    corr = str(line[corr1_num]).strip()+str(line[corr2_num]).strip()+str(line[corr3_num]).strip()+str(line[corr4_num]).strip()
    rt = str(line[rt1_num]).strip()+str(line[rt2_num]).strip()+str(line[rt3_num]).strip()+str(line[rt4_num]).strip()
    expression.append(line[expression_num])
    corr_total.append(corr)
    rt_total.append(rt)
sad_rt=[]
sad_corr=[]
neutral_rt=[]
neutral_corr = []
furry_rt =[]
furry_corr=[]
fear_rt=[]
fear_corr=[]
hated_rt=[]
hated_corr=[]
happy_rt=[]
happy_corr=[]
for i in range(len(expression)):
    if expression[i] == '愤怒':
        furry_corr.append(corr_total[i])
        if corr_total[i]== '1':
            furry_rt.append(rt_total[i])
    if expression[i] == '悲伤':
        sad_corr.append(corr_total[i])
        if corr_total[i]== '1':
            sad_rt.append(rt_total[i])
    if expression[i] == '中性':
        neutral_corr.append(corr_total[i])
        if corr_total[i]== '1':
            neutral_rt.append(rt_total[i])
    if expression[i] == '恐惧':
        fear_corr.append(corr_total[i])
        if corr_total[i]== '1':
            fear_rt.append(rt_total[i])
    if expression[i] == '厌恶':
        hated_corr.append(corr_total[i])
        if corr_total[i]== '1':
            hated_rt.append(rt_total[i])
    if expression[i] == '快乐':
        happy_corr.append(corr_total[i])
        if corr_total[i]== '1':
            happy_rt.append(rt_total[i])
# 求反应时平均值及方差
def aver(data):
    raw_rt=[]
    for i in range(len(data)):
        raw_rt.append(float(data[i]))
    aver=numpy.mean(raw_rt)
    std1=numpy.std(raw_rt)
    return aver,std1
# 求正确率
def correct(data):
    right=0
    total=0
    for i in range(len(data)):
        if  data[i] =='1':
            total += 1
            right += 1
        else :
            total += 1
    ratio=right/total
    ratio=ratio*100
    return  ratio
# 计算平均值方差正确率
total_rt=[furry_rt,sad_rt,neutral_rt,fear_rt,hated_rt,happy_rt]
total_corr=[furry_corr,sad_corr,neutral_corr,fear_corr,hated_corr,happy_corr]
for i in total_rt:
    aver1,std1=aver(i)
    reacttime.append(aver1)
    Standard_Deviation.append(std1)
for i in total_corr:
    corr1=correct(i)
    corratio.append(corr1)
# print(reacttime,corratio)
expression=["愤怒","悲伤","平静","恐惧","厌恶","快乐"]
# 绘图
import matplotlib.pyplot as plt
expression_index=len(expression)
plt.style.use('ggplot')
#解决中文显示问题
plt.rcParams['font.sans-serif'] = ['KaiTi'] # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题
# 平均反应时
fig=plt.figure()
ax1=fig.add_subplot(1,1,1)
ax1.bar(expression, reacttime, align='center', color='darkblue')
ax1.errorbar(x=expression,y=reacttime,yerr=Standard_Deviation,ecolor='grey',capsize=4,color='black',fmt='o')
# ax1.bar(expression,corratio,align='center',color='red')
ax1.xaxis.set_ticks_position("bottom")
ax1.yaxis.set_ticks_position("left")
plt.xlabel('人类不同种类的情绪')
plt.ylabel('时间(秒)')
plt.title('图1：平均反应时间（秒）')
plt.savefig('reaction_time.png',dpi=400,bbox_inches='tight')
# 平均准确率
fig1=plt.figure()
ax2=fig1.add_subplot(1,1,1)
ax2.bar(expression,corratio,align='center',color='darkblue')
ax2.xaxis.set_ticks_position("bottom")
ax2.yaxis.set_ticks_position("left")
plt.xlabel('人类不同种类的情绪')
plt.ylabel('准确率（%）')
plt.title('图2：平均准确率')
plt.savefig('correction_ratio.png',dpi=400,bbox_inches='tight')
# plt.show()
# 绘制pdf
from fpdf import FPDF
# class PDF(FPDF):
#     def footer(self):
#         # Position at 1.5 cm from bottom
#         self.set_y(0)
#         # Arial italic 8
#         self.set_font('Arial', 'I', 8)
#         # Page number
#         self.cell(0, 0, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')

pdf = FPDF('p','mm','A4')
pdf.alias_nb_pages()
pdf.add_page()
pdf.add_font('hei','',fname=r'C:\Windows\Fonts\simhei.ttf',uni=True)
pdf.set_font("hei", size=18)
pdf.cell(180, 20, txt="电脑认知测试一：面孔情绪识别能力", ln=1, align="C")
pdf.set_font('hei',size=12)
pdf.cell(180,13,txt='姓名：'+name,ln=1)
pdf.cell(180,13,txt='时间：'+expri_time,ln=1)
pdf.cell(180,7,txt='—————————————————————————',ln=1,align="C")
pdf.cell(180,7,txt='表情       准确率        反应时(秒)        标准差',ln=1,align='C')
pdf.cell(180,7,txt='—————————————————————————',ln=1,align='C')
for i in range(0,6):
    text="{}        {:.2f}%        {:.5f}       {:.5f}".format(expression[i],corratio[i],reacttime[i],Standard_Deviation[i])
    pdf.cell(180,7,txt=text,ln=1,align="C")
pdf.cell(180,7,txt='—————————————————————————',ln=1,align='C')
pdf.image('reaction_time.png',x=0,y=160,w=100,h=86)
pdf.image('correction_ratio.png',x=110,y=160,w=100,h=86)
if times == '1':
    pdfname = dictname+'/'+name+"_time1_"+time.strftime('%Y_%m_%d_%H%m',time.localtime())+'.pdf'
elif times == '2':
    pdfname = dictname+'/'+name+"_time2_"+time.strftime('%Y_%m_%d_%H%m',time.localtime())+'.pdf'
elif times== '3':
    pdfname = dictname+'/'+name+"_mother_"+time.strftime('%Y_%m_%d_%H%m',time.localtime())+'.pdf'
elif times== '4':
    pdfname = dictname+"/"+name+"_father_"+time.strftime('%Y_%m_%d_%H%m',time.localtime())+'.pdf'
# pdf.output(pdfname)
print("测试一文件处理完成。")

# 文件数据读取
reacttime = []
reacttime1=[]
corratio = []
Standard_Deviation = []
datalist = []

if times == '1':
    filename=filename1[-1]+'_time1_Dot_Probe'
elif times == '2':
    filename = filename1[-1]+'_time2_Dot_Probe'
elif times == '3':
    filename = filename1[-1]+'_mother_Dot_Probe'
elif times == '4':
    filename = filename1[-1] + '_father_Dot_Probe'
else:
    filename = filename1[-1] + '_time1_Dot_Probe'
for files in os.listdir('/'.join(filename1) + '/2_Dot_Probe/'):
    if filename in files and '.csv'in files:
        expri_time=files[-20:-4]
        filename='/'.join(filename1) + '/2_Dot_Probe/'+files

print("测试二文件开始处理。")
# 文件数据读取
f = open(filename, 'r', encoding='utf-8')
filereader = csv.reader(f)
database1 = []
direction=[]
type1 = []
type2 = []
for i,line in enumerate(filereader):
    if i == 0:
        for j in range(len(line)):
            if line[j] == 'key_resp_trial_1.rt':
                rt1_num = j
            if line[j] == 'key_resp_trial_2.rt':
                rt2_num = j
            if line[j] == 'key_resp_trial_1.corr':
                corr1_num = j
            if line[j] == 'key_resp_trial_2.corr':
                corr2_num = j
    direction_con=str(line[3].strip())
    type1_com = str(line[5]).strip()
    type2_com = str(line[6]).strip()
    rt1=str(line[rt1_num]).strip()
    rt2=str(line[rt2_num]).strip()
    corr1=str(line[corr1_num]).strip()
    corr2=str(line[corr2_num]).strip()
    rt_con=rt1+rt2
    corr_con=corr1+corr2
    # print(line)
    if rt_con != '' and rt_con != 'key_resp_trial_1.rtkey_resp_trial_2.rt':
        reacttime1.append(rt_con)
    if corr_con != '' and corr_con !='key_resp_trial_1.corrkey_resp_trial_2.corr':
        corratio.append(corr_con)
    if type1_com != '' and type1_com != 'type1':
        type1.append(type1_com)
    if type2_com != '' and type2_com != 'type2':
        type2.append(type2_com)
    if direction_con != '' and direction_con != 'j':
        direction.append(direction_con)
    for i in reacttime1:
        reacttime.append(float(i))
# print(reacttime)
# print(corratio)
# print(direction)
# print(type1)
# print(type2)
# print(len(direction))
# print(len(type1))
# print(len(type2))
# 各数据类型匹配
nn_rt=[]
nn_corr=[]
for i in range(len(direction)):
    if type1[i][0]=='n' and type2[i][0]=='n':
        nn_rt.append(reacttime[i])
        nn_corr.append(corratio[i])
# print(nn_rt)
# print(nn_corr)
# sad、happy同侧
sh_s_rt=[]
sh_s_corr=[]
for i in range(len(direction)):
    if type1[i][0]=='h' and type2[i][0]=='s' and direction[i]=='right':
        if corratio[i] == '1':
            sh_s_rt.append(reacttime[i])
        sh_s_corr.append(corratio[i])
    if type1[i][0] =='s' and type2[i][0]=='h' and direction[i]=='left':
        if corratio[i] == '1':
            sh_s_rt.append(reacttime[i])
        sh_s_corr.append(corratio[i])
# print(sh_s_corr)
# print(sh_s_rt)
# sad、happy异侧
sh_o_rt=[]
sh_o_corr=[]
for i in range(len(direction)):
    if type1[i][0]=='h' and type2[i][0]=='s' and direction[i]=='left':
        if corratio[i] == '1':
            sh_o_rt.append(reacttime[i])
        sh_o_corr.append(corratio[i])
    if type1[i][0]=='s' and type2[i][0]=='h' and direction[i]=='right':
        if corratio[i] == '1':
            sh_o_rt.append(reacttime[i])
        sh_o_corr.append(corratio[i])
# print(sh_o_corr)
# print(sh_o_rt)
# sad、neutral同侧
sn_s_rt=[]
sn_s_corr=[]
for i in range(len(direction)):
    if type1[i][0]=='n' and type2[i][0]=='s' and direction[i]=='right':
        if corratio[i] == '1':
            sn_s_rt.append(reacttime[i])
        sn_s_corr.append(corratio[i])
    if type1[i][0]=='s' and type2[i][0]=='n' and direction[i]=='left':
        if corratio[i] == '1':
            sn_s_rt.append(reacttime[i])
        sn_s_corr.append(corratio[i])
# print(sn_s_corr)
# print(sn_s_rt)
# sad、neutral异侧
sn_o_rt=[]
sn_o_corr=[]
for i in range(len(direction)):
    if type1[i][0]=='n' and type2[i][0]=='s' and direction[i]=='left':
        if corratio[i] == '1':
            sn_o_rt.append(reacttime[i])
        sn_o_corr.append(corratio[i])
    if type1[i][0]=='s' and type2[i][0]=='n' and direction[i]=='right':
        sn_o_corr.append(corratio[i])
        if corratio[i] == '1':
            sn_o_rt.append(reacttime[i])
# print(sn_o_corr)
# print(sn_o_rt)
# happy、neutral同侧
hn_s_rt=[]
hn_s_corr=[]
for i in range(len(direction)):
    if type1[i][0]=='n' and type2[i][0]=='h' and direction[i]=='right':
        hn_s_corr.append(corratio[i])
        if corratio[i] == '1':
            hn_s_rt.append(reacttime[i])
    if type1[i][0]=='h' and type2[i][0]=='n' and direction[i]=='left':
        hn_s_corr.append(corratio[i])
        if corratio[i] == '1':
            hn_s_rt.append(reacttime[i])
# print(hn_s_corr)
# print(hn_s_rt)
# happy、neutral异侧
hn_o_rt=[]
hn_o_corr=[]
for i in range(len(direction)):
    if type1[i][0]=='n' and type2[i][0]=='h' and direction[i]=='left':
        hn_o_corr.append(corratio[i])
        if corratio[i] == '1':
            hn_o_rt.append(reacttime[i])
    if type1[i][0]=='h' and type2[i][0]=='n' and direction[i]=='right':
        hn_o_corr.append(corratio[i])
        if corratio[i]=='1':
            hn_o_rt.append(reacttime[i])
# print(hn_o_corr)
# print(hn_o_rt)
# print(len(sh_o_rt)+len(sh_s_rt)+len(sn_o_rt)+len(sn_s_rt)+len(nn_rt)+len(hn_o_rt)+len(hn_s_rt))
# 求反应时平均值及方差
total_rt=[nn_rt,sh_s_rt,sh_o_rt,sn_s_rt,sn_o_rt,hn_s_rt,hn_o_rt]
def aver_and_std(data):
    average=[]
    std=[]
    for i in data:
        average1 = numpy.mean(i)
        average1 = round(average1, 5)
        std1 = numpy.std(i)
        std1 = round(std1,5)
        average.append(average1)
        std.append(std1)
    return average,std
aver1,std1=aver_and_std(total_rt)
# print(aver1)
# print(std1)
# 各类型正确率
total_corr=[nn_corr,sh_s_corr,sh_o_corr,sn_s_corr,sn_o_corr,hn_s_corr,hn_o_corr]
def correct_ratio(data2):
    result=[]
    right=0
    wrong=0
    total=0
    for j in data2:
        for i in j:
            if i == '1':
                right += 1
            elif i == '0':
                wrong += 1
            else:
                pass
            total += 1
        ratio=right/total
        ratio=ratio*100
        result.append(ratio)
        # ratio="{:.2%}".format(ratio)
    return  result
corr=correct_ratio(total_corr)
expression1=['平静——平静','悲伤(吸引)——高兴','悲伤——高兴(吸引)','悲伤(吸引)——平静','悲伤——平静(吸引)','高兴(吸引)——平静','高兴——平静(吸引)']
# #输出表格
# print("—————————————————————————————")
# print("表情        准确率        反应时         标准差")
# print("—————————————————————————————")
# for i in range(0,7):
#     print("{}       {:.2f}%       {:.5f}        {:.5f}".format(expression1[i],corr[i],aver1[i],std1[i]))
# print("—————————————————————————————")
expression=['平静——平静','悲伤——高兴','悲伤——平静','高兴——平静']
corr_s=[]
corr_o=[0]
aver_s=[]
aver_o=[0]
std_s=[]
std_o=[0]
x=range(len(expression))
for i in range(len(corr)):
    if i==0 or i==1 or i==3 or i== 5 :
        corr_s.append(corr[i])
        aver_s.append(aver1[i])
        std_s.append(std1[i])
    else:
        corr_o.append(corr[i])
        aver_o.append(aver1[i])
        std_o.append(std1[i])
# 绘图
import matplotlib.pyplot as plt
expression_index=len(expression)
plt.style.use('ggplot')
#解决中文显示问题
plt.rcParams['font.sans-serif'] = ['KaiTi'] # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题
# 平均反应时
fig=plt.figure()
bar_width='   '
aver_s=numpy.array(aver_s)
aver_o=numpy.array(aver_o)
ax1=fig.add_subplot(1,1,1)
ax1.bar(x,aver_s,width=0.4, color='darkblue',label='前者吸引')
ax1.errorbar(x,y=aver_s,yerr=std_s,ecolor='grey',capsize=4,color='black',fmt='o')
ax1.bar([i+0.4 for i in x],aver_o,width=0.4,color='red',label='后者吸引')
ax1.errorbar([i+0.4 for i in x],y=aver_o,yerr=std_o,ecolor='grey',capsize=4,color='black',fmt='o')
# ax1.bar(expression,corratio,align='center',color='red')
plt.xticks([i+0.2 for i in x], expression ,fontsize=10)
ax1.xaxis.set_ticks_position("bottom")
ax1.yaxis.set_ticks_position("left")
plt.xlabel('人类不同种类的情绪')
plt.ylabel('时间(秒)')
plt.title('图1：平均反应时间（秒）')
plt.legend()
plt.savefig('reaction_time.png',dpi=400,bbox_inches='tight')
# 平均准确率
fig1=plt.figure()
ax2=fig1.add_subplot(1,1,1)
ax2.bar(x,corr_s,color='darkblue',label='前者吸引',width=0.4)
ax2.bar([i+0.4 for i in x],corr_o,color='red',label='后者吸引',width=0.4)
plt.xticks([i+0.2 for i in x],expression,fontsize=10)
ax2.xaxis.set_ticks_position("bottom")
ax2.yaxis.set_ticks_position("left")
plt.xlabel('人类不同种类的情绪')
plt.ylabel('准确率（%）')
plt.title('图2：平均准确率')
plt.legend()
plt.savefig('correction_ratio.png',dpi=400,bbox_inches='tight')
# plt.show()
# 绘制pdf文档
from fpdf import FPDF
pdf.add_page()
pdf.add_font('hei','',fname=r'C:\Windows\Fonts\simhei.ttf',uni=True)
pdf.set_font("hei", size=18)
pdf.cell(180, 20, txt="电脑认知测试二：注意探测能力", ln=1, align="C")
pdf.set_font('hei',size=12)
pdf.cell(180,13,txt='姓名：'+name,ln=1)
pdf.cell(180,13,txt='时间：'+expri_time,ln=1)
pdf.cell(180,7,txt='———————————————————————————————————',ln=1,align="C")
pdf.cell(180,7,txt='表情       准确率        反应时（秒）        标准差',ln=1,align='C')
pdf.cell(180,7,txt='———————————————————————————————————',ln=1,align='C')
for i in range(0,7):
    text="{}        {:.2f}%        {:.5f}            {:.5f}".format(expression1[i],corr[i],aver1[i],std1[i])
    pdf.cell(180,7,txt=text,ln=1,align="C")
pdf.cell(180,7,txt='———————————————————————————————————',ln=1,align='C')
pdf.image('reaction_time.png',x=0,y=160,w=100,h=86)
pdf.image('correction_ratio.png',x=110,y=160,w=100,h=86)
print("测试二文件处理完成。")

# 测试三
reacttime = []
corratio = []
Standard_Deviation = []
if times == '1':
    filename=filename1[-1]+'_time1_Go_Nogo'
elif times == '2':
    filename = filename1[-1]+'_time2_Go_Nogo'
elif times == '3':
    filename = filename1[-1]+'_mother_Go_Nogo'
elif times == '4':
    filename = filename1[-1] + '_father_Go_Nogo'
else:
    filename = filename1[-1] + '_time1_Go_Nogo'
for files in os.listdir('/'.join(filename1) + '/3_Go_Nogo/'):
    if filename in files and '.csv' in files:
        expri_time=files[-20:-4]
        filename='/'.join(filename1) + '/3_Go_Nogo/'+files
print("测试三文件开始处理。")
# 文件数据读取
f = open(filename, 'r', encoding='utf-8')
filereader = csv.reader(f)
light=[]
expression=[]
rt_light=[]
rt_expreesion=[]
corr_expression=[]
corr_light=[]
global rt_light_num
for i,line in enumerate(filereader):
    if i==0:
        for word in range(len(line)):
            if line[word] == 'key_resp_light.rt':
                rt_light_num=word
            if line[word] == 'key_resp_face.rt':
                rt_face__num=word
    light1=str(line[1].strip())
    expression2 = str(line[3]).strip()
    rt_l=str(line[rt_light_num]).strip()
    rt_e=str(line[rt_face__num]).strip()
    corr_l=str(line[31]).strip()
    corr_e=str(line[42]).strip()
    light.append(light1)
    expression.append(expression2)
    rt_light.append(rt_l)
    rt_expreesion.append(rt_e)
    if corr_l == '1' or corr_l == '0':
        corr_light.append(corr_l)
    if corr_e == '1' or corr_e == '0':
        corr_expression.append(corr_e)
# print(light)
# print(expression)
# print(rt_expreesion)
# print(rt_light)
# print(corr_light)
# print(corr_expression)
# 求反应时平均值及方差
def aver(data,rt):
    raw_rt=[]
    for i in range(len(data)):
        if data[i] == 'space' and rt[i] != '':
            raw_rt.append(eval(rt[i]))
    aver=numpy.mean(raw_rt)
    std1=numpy.std(raw_rt)
    return aver,std1
# 求正确率
def correct(data):
    right=0
    total=0
    for i in range(len(data)):
        if  data[i] =='1':
            total += 1
            right += 1
        else :
            total += 1
    ratio=right/total
    ratio=ratio*100
    return  ratio
# 计算平均值方差正确率
rt_li,std_li = aver(light,rt_light)
corr_li = correct(corr_light)
rt_ex,std_ex = aver(expression,rt_expreesion)
corr_ex = correct(corr_expression)
reacttime.append(rt_li)
reacttime.append(rt_ex)
corratio.append(corr_li)
corratio.append(corr_ex)
Standard_Deviation.append(std_li)
Standard_Deviation.append(std_ex)
# print(reacttime)
# print(corratio)
# print(Standard_Deviation)
expression1=['灯光','表情']
# # 数据输出
# print("—————————————————————————————")
# print(" 灯光/表情        准确率        反应时         标准差")
# print("—————————————————————————————")
# for i in range(0,2):
#     print("   {}           {:.2f}%       {:.5f}        {:.5f}".format(expression1[i],corratio[i],reacttime[i],Standard_Deviation[i]))
# print("—————————————————————————————")
# 绘图
import matplotlib.pyplot as plt
expression_index=len(expression)
plt.style.use('ggplot')
#解决中文显示问题
plt.rcParams['font.sans-serif'] = ['KaiTi'] # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题
# 平均反应时
fig=plt.figure()
ax1=fig.add_subplot(1,1,1)
ax1.bar(expression1, reacttime, align='center', color='darkblue',width=0.3)
ax1.errorbar(x=expression1,y=reacttime,yerr=Standard_Deviation,ecolor='grey',capsize=4,color='black',fmt='o')
# ax1.bar(expression,corratio,align='center',color='red')
ax1.xaxis.set_ticks_position("bottom")
ax1.yaxis.set_ticks_position("left")
plt.xlabel('灯光/表情')
plt.ylabel('时间(秒)')
plt.title('图1：平均反应时间（秒）')
plt.savefig('reaction_time.png',dpi=400,bbox_inches='tight')

# 平均准确率
fig1=plt.figure()
ax2=fig1.add_subplot(1,1,1)
ax2.bar(expression1,corratio,align='center',color='darkblue',width=0.3)
ax2.xaxis.set_ticks_position("bottom")
ax2.yaxis.set_ticks_position("left")
plt.ylim(40,100)
plt.xlabel('灯光/表情')
plt.ylabel('准确率（%）')
plt.title('图2：平均准确率')
plt.savefig('correction_ratio.png',dpi=400,bbox_inches='tight')
# plt.show()

pdf.add_page()
pdf.add_font('hei','',fname=r'C:\Windows\Fonts\simhei.ttf',uni=True)
pdf.set_font("hei", size=18)
pdf.cell(180, 20, txt="电脑认知测试三：注意探测能力", ln=1, align="C")
pdf.set_font('hei',size=12)
pdf.cell(180,13,txt='姓名：'+name,ln=1)
pdf.cell(180,13,txt='时间：'+expri_time,ln=1)
pdf.cell(180,7,txt='———————————————————————————',ln=1,align="C")
pdf.cell(180,7,txt='灯光/表情       准确率        反应时(秒)        标准差',ln=1,align='C')
pdf.cell(180,7,txt='———————————————————————————',ln=1,align='C')
for i in range(0,2):
    text="{}        {:.2f}%        {:.5f}       {:.5f}".format(expression1[i],corratio[i],reacttime[i],Standard_Deviation[i])
    pdf.cell(180,7,txt=text,ln=1,align="C")
pdf.cell(180,7,txt='———————————————————————————',ln=1,align='C')
pdf.image('reaction_time.png',x=0,y=160,w=100,h=86)
pdf.image('correction_ratio.png',x=110,y=160,w=100,h=86)
print("测试三文件处理完成。")

# 测试四
reacttime = []
corratio = []
Standard_Deviation = []
if times == '1':
    filename=filename1[-1]+'_time1_Nback'
elif times == '2':
    filename = filename1[-1]+'_time2_Nback'
elif times == '3':
    filename = filename1[-1]+'_mother_Nback'
elif times == '4':
    filename = filename1[-1] + '_father_Nback'
else:
    filename = filename1[-1] + '_time1_Nback'
for files in os.listdir('/'.join(filename1) + '/4_Nback/'):
    if filename in files and '.csv' in files:
        expri_time=files[-20:-4]
        filename='/'.join(filename1) + '/4_Nback/'+files
print("测试四文件开始处理。")
# 文件数据读取
f = open(filename, 'r', encoding='utf-8')
filereader = csv.reader(f)
back0_rt_list=[]
back0_rt_list1=[]
back1_corr_list=[]
back2_corr_list=[]
back1_rt_list=[]
back2_rt_list=[]
for i,line in enumerate(filereader):
    if i==0:
        for j in range(len(line)):
            if line[j] == 'key_resp_0back.rt' :
                back0_num=j
            if line[j] == 'key_resp_1back.rt':
                back1_rt_num=j
            if line[j] == 'key_resp_1back.corr':
                back1_corr_num=j
            if line[j] == 'key_resp_2back.rt':
                back2_rt_num=j
            if line[j] == 'key_resp_2back.corr':
                back2_corr_num=j
    back0_rt=str(line[back0_num]).strip()
    back1_rt=str(line[back1_rt_num]).strip()
    back1_corr=str(line[back1_corr_num]).strip()
    back2_rt=str(line[back2_rt_num]).strip()
    back2_corr = str(line[back2_corr_num]).strip()
    back0_rt_list1.append(back0_rt)
    if back1_corr == '1' or back1_corr == '0':
        back1_corr_list.append(back1_corr)
    if back2_corr =='1' or back2_corr == '0':
        back2_corr_list.append(back2_corr)
    if back1_corr == '1' :
        back1_rt_list.append(back1_rt)
    if back2_corr== '1' :
        back2_rt_list.append(back2_rt)
for i in back0_rt_list1:
    try  :
        j = eval(i)
        back0_rt_list.append(j)
    except:
        pass
# print(back0_rt_list)
# print(back1_rt_list)
# print(back2_rt_list)
# print(back1_corr_list)
# print(back2_corr_list)

# 求反应时平均值及方差
def aver(data):
    raw_rt=[]
    for i in range(len(data)):
        raw_rt.append(float(data[i]))
    aver=numpy.mean(raw_rt)
    std1=numpy.std(raw_rt)
    return aver,std1

# 求正确率
def correct(data):
    right=0
    total=0
    for i in range(len(data)):
        if  data[i] =='1':
            total += 1
            right += 1
        else :
            total += 1
    ratio=right/total
    ratio=ratio*100
    return  ratio

# 计算结果
total_rt=[back0_rt_list,back1_rt_list,back2_rt_list]
total_corr=[back1_corr_list,back2_corr_list]
for i in range(len(total_rt)):
    aver_con,std=aver(total_rt[i])
    reacttime.append(aver_con)
    Standard_Deviation.append(std)
for i in total_corr:
    corratio_con=correct(i)
    corratio.append(corratio_con)
# print(reacttime)
# print(Standard_Deviation)
# print(corratio)
corratio_print=[100]+corratio
back_rt_list=['0back','1back','2back']
# 数据输出
# print("—————————————————————————————")
# print("    Nback       准确率        反应时         标准差")
# print("—————————————————————————————")
# for i in range(0,3):
#     print("   {}        {:.2f}%       {:.5f}        {:.5f}".format(back_rt_list[i],corratio_print[i],reacttime[i],Standard_Deviation[i]))
# print("—————————————————————————————")
# 绘图
import matplotlib.pyplot as plt
plt.style.use('ggplot')
#解决中文显示问题
plt.rcParams['font.sans-serif'] = ['KaiTi'] # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题
# 平均反应时
fig=plt.figure()
ax1=fig.add_subplot(1,1,1)
ax1.bar(back_rt_list, reacttime, align='center', color='darkblue',width=0.3)
ax1.errorbar(x=back_rt_list,y=reacttime,yerr=Standard_Deviation,ecolor='grey',capsize=4,color='black',fmt='o')
# ax1.bar(expression,corratio,align='center',color='red')
ax1.xaxis.set_ticks_position("bottom")
ax1.yaxis.set_ticks_position("left")
plt.xlabel('Nback')
plt.ylabel('时间(秒)')
plt.title('图1：平均反应时间（秒）')
plt.savefig('reaction_time.png',dpi=400,bbox_inches='tight')
# plt.show()
# 平均准确率
fig1=plt.figure()
ax2=fig1.add_subplot(1,1,1)
ax2.bar(back_rt_list,corratio_print,align='center',color='darkblue',width=0.3)
ax2.xaxis.set_ticks_position("bottom")
ax2.yaxis.set_ticks_position("left")
plt.xlabel('Nback')
plt.ylabel('准确率（%）')
plt.title('图2：平均准确率')
plt.savefig('correction_ratio.png',dpi=400,bbox_inches='tight')
# plt.show()
# 绘制pdf文档
pdf.add_page()
pdf.add_font('hei','',fname=r'C:\Windows\Fonts\simhei.ttf',uni=True)
pdf.set_font("hei", size=18)
pdf.cell(180, 20, txt="电脑认知测试四：短时记忆能力", ln=1, align="C")
pdf.set_font('hei',size=12)
pdf.cell(180,13,txt='姓名：'+name,ln=1)
pdf.cell(180,13,txt='时间：'+expri_time,ln=1)
pdf.cell(180,7,txt='—————————————————————————',ln=1,align="C")
pdf.cell(180,7,txt='Nback       准确率        反应时(秒)        标准差',ln=1,align='C')
pdf.cell(180,7,txt='—————————————————————————',ln=1,align='C')
for i in range(0,3):
    text="{}        {:.2f}%        {:.5f}       {:.5f}".format(back_rt_list[i],corratio_print[i],reacttime[i],Standard_Deviation[i])
    pdf.cell(180,7,txt=text,ln=1,align="C")
pdf.cell(180,7,txt='—————————————————————————',ln=1,align='C')
pdf.image('reaction_time.png',x=0,y=160,w=100,h=86)
pdf.image('correction_ratio.png',x=110,y=160,w=100,h=86)
print("测试四文件处理完成。")

# 测试五
reacttime = []
corratio = []
Standard_Deviation = []
if times == '1':
    filename=filename1[-1]+'_time1_Stroop'
elif times == '2':
    filename = filename1[-1]+'_time2_Stroop'
elif times == '3':
    filename = filename1[-1]+'_mother_Stroop'
elif times == '4':
    filename = filename1[-1] + '_father_Stroop'
else:
    filename = filename1[-1] + '_time1_Stroop'
for files in os.listdir('/'.join(filename1) + '/5_Stroop/'):
    if filename in files and '.csv' in files:
        expri_time=files[-20:-4]
        filename='/'.join(filename1) + '/5_Stroop/'+files
print("测试五文件开始处理。")
# 文件数据读取
f = open(filename, 'r', encoding='utf-8')
filereader = csv.reader(f)
character_rt=[]
character_corr=[]
color_s_corr=[]
color_s_rt=[]
color_o_corr=[]
color_o_rt=[]
last_name=['王','李','张','孙','行','钱','赵','武','周']
color_name=['红','黄','蓝']
color_En=['red','blue','yellow']
dictory_color={'红':'red','黄':'yellow','蓝':'blue'}
global character_num
for i,line in enumerate(filereader):
    if i==0:
        for j in range(len(line)):
            if line[j] == 'color':
                color_num=j
            if line[j] == 'key_resp_5.corr':
                corr1_num=j
            if line[j] == 'key_resp_5.rt':
                rt1_num=j
            if line[j] == 'key_resp.corr':
                corr2_num=j
            if line[j] == 'key_resp.rt':
                rt2_num=j
            if line[j] == 'key_resp_2.corr':
                corr3_num=j
            if line[j] == 'key_resp_2.rt':
                rt3_num=j
    rt=line[rt1_num]+line[rt2_num]+line[rt3_num]
    corr=line[corr1_num]+line[corr2_num]+line[corr3_num]
    if line[0] in last_name:
        if corr == '1':
            character_rt.append(float(str(rt).strip()))
        character_corr.append(str(corr).strip())
    if line[0] =='蓝' and line[color_num] == 'blue':
        if corr == '1':
            color_s_rt.append(float(str(rt).strip()))
        color_s_corr.append(str(corr).strip())
    if line[0] =='红' and line[color_num] == 'red':
        if corr == '1':
            color_s_rt.append(float(str(rt).strip()))
        color_s_corr.append(str(corr).strip())
    if line[0] =='黄' and line[color_num] == 'yellow':
        if corr == '1':
            color_s_rt.append(float(str(rt).strip()))
        color_s_corr.append(str(corr).strip())
    if line[0] =='蓝' and line[color_num] != 'blue':
        if corr == '1':
            color_o_rt.append(float(str(rt).strip()))
        color_o_corr.append(str(corr).strip())
    if line[0] =='黄' and line[color_num] != 'yellow':
        if corr == '1':
            color_o_rt.append(float(str(rt).strip()))
        color_o_corr.append(str(corr).strip())
    if line[0] =='红' and line[color_num] != 'red':
        if corr == '1':
            color_o_rt.append(float(str(rt).strip()))
        color_o_corr.append(str(corr).strip())


# 求反应时平均值及方差
def aver(data):
    raw_rt=[]
    for i in range(len(data)):
        raw_rt.append(float(data[i]))
    aver=numpy.mean(raw_rt)
    std1=numpy.std(raw_rt)
    return aver,std1

# 求正确率
def correct(data):
    right=0
    total=0
    for i in range(len(data)):
        if  data[i] =='1':
            total += 1
            right += 1
        else :
            total += 1
    ratio=right/total
    ratio=ratio*100
    return  ratio

total_rt=[character_rt,color_s_rt,color_o_rt]
total_corr=[character_corr,color_s_corr,color_o_corr]
for i in total_rt:
    aver1,std=aver(i)
    reacttime.append(aver1)
    Standard_Deviation.append(std)
for i in total_corr:
    corr1=correct(i)
    corratio.append(corr1)

tag=['中性条件','一致性条件','冲突条件']
# # 数据输出
# print("—————————————————————————————")
# print("    分类      准确率        反应时         标准差")
# print("—————————————————————————————")
# for i in range(0,3):
#     print("   {}        {:.2f}%       {:.5f}        {:.5f}".format(tag[i],corratio[i],reacttime[i],Standard_Deviation[i]))
# print("—————————————————————————————")

# 绘图
import matplotlib.pyplot as plt
plt.style.use('ggplot')
#解决中文显示问题
plt.rcParams['font.sans-serif'] = ['KaiTi'] # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题
# 平均反应时
fig=plt.figure()
ax1=fig.add_subplot(1,1,1)
ax1.bar(tag, reacttime, align='center', color='darkblue',width=0.3)
ax1.errorbar(x=tag,y=reacttime,yerr=Standard_Deviation,ecolor='grey',capsize=4,color='black',fmt='o')
# ax1.bar(expression,corratio,align='center',color='red')
ax1.xaxis.set_ticks_position("bottom")
ax1.yaxis.set_ticks_position("left")
plt.xlabel('Stroop')
plt.ylabel('时间(秒)')
plt.title('图1：平均反应时间（秒）')
plt.savefig('reaction_time.png',dpi=400,bbox_inches='tight')
# plt.show()
# 平均准确率
fig1=plt.figure()
ax2=fig1.add_subplot(1,1,1)
ax2.bar(tag,corratio,align='center',color='darkblue',width=0.3)
ax2.xaxis.set_ticks_position("bottom")
ax2.yaxis.set_ticks_position("left")
plt.xlabel('Stroop')
plt.ylabel('准确率（%）')
plt.title('图2：平均准确率')
plt.savefig('correction_ratio.png',dpi=400,bbox_inches='tight')
# plt.show()

# 绘制pdf文档
pdf.add_page()
pdf.add_font('hei','',fname=r'C:\Windows\Fonts\simhei.ttf',uni=True)
pdf.set_font("hei", size=18)
pdf.cell(180, 20, txt="电脑认知测试五：冲突解决能力", ln=1, align="C")
pdf.set_font('hei',size=12)
pdf.cell(180,13,txt='姓名：'+name,ln=1)
pdf.cell(180,13,txt='时间：'+expri_time,ln=1)
pdf.cell(180,7,txt='—————————————————————————',ln=1,align="C")
pdf.cell(180,7,txt='分类       准确率        反应时(秒)        标准差',ln=1,align='C')
pdf.cell(180,7,txt='—————————————————————————',ln=1,align='C')
for i in range(0,3):
    text="{}        {:.2f}%        {:.5f}       {:.5f}".format(tag[i],corratio[i],reacttime[i],Standard_Deviation[i])
    pdf.cell(180,7,txt=text,ln=1,align="C")
pdf.cell(180,7,txt='—————————————————————————',ln=1,align='C')
pdf.image('reaction_time.png',x=0,y=160,w=100,h=86)
pdf.image('correction_ratio.png',x=110,y=160,w=100,h=86)
print("测试五文件处理完成。")

# 测试六
reacttime = []
corratio = []
Standard_Deviation = []
if times == '1':
    filename=filename1[-1]+'_time1_Scene_Recognition_Task'
elif times == '2':
    filename = filename1[-1]+'_time2_Scene_Recognition_Task'
elif times == '3':
    filename = filename1[-1]+'_mother_Scene_Recognition_Task'
elif times == '4':
    filename = filename1[-1] + '_father_Scene_Recognition_Task'
else:
    filename = filename1[-1] + '_time1_Scene_Recognition_Task'
for files in os.listdir('/'.join(filename1) + '/6_Scene_Recognition_Task/'):
    if filename in files and '.csv' in files:
        expri_time=files[-20:-4]
        filename='/'.join(filename1) + '/6_Scene_Recognition_Task/'+files
print('测试六文件开始处理')
# 文件数据读取
f = open(filename, 'r', encoding='utf-8')
filereader = csv.reader(f)
direction_rt=[]
direction_corr=[]
location_rt=[]
location_corr=[]
arrange_rt=[]
arrange_corr=[]
for i,line in enumerate(filereader):
    if i==0:
        for j in range(len(line)):
            if line[j] == 'key_resp_formal1.corr':
                direction_corr_num=j
            if line[j] == 'key_resp_formal1.rt':
                direction_rt_num=j
            if line[j] == 'key_resp_formal2.corr':
                location_corr_num=j
            if line[j] == 'key_resp_formal2.rt':
                location_rt_num=j
            if line[j] == 'key_resp_formal3.corr':
                arrange_corr_num=j
            if line[j] == 'key_resp_formal3.rt':
                arrange_rt_num=j
    if line[direction_corr_num] == '1' or line[direction_corr_num] =='0':
        direction_corr.append(str(line[direction_corr_num]).strip())
    if line[direction_corr_num] == '1':
        direction_rt.append(float(str(line[direction_rt_num]).strip()))
    if line[location_corr_num] == '1' or line[location_corr_num] =='0':
        location_corr.append(str(line[location_corr_num]).strip())
    if line[location_corr_num] == '1':
        location_rt.append(float(str(line[location_rt_num]).strip()))
    if line[arrange_corr_num] =='1' or line[arrange_corr_num] == '0':
        arrange_corr.append(str(line[arrange_corr_num]).strip())
    if line[arrange_corr_num] == '1':
        arrange_rt.append(float(str(line[arrange_rt_num]).strip()))
# print(direction_rt)
# print(direction_corr)
# print(location_corr)
# print(location_rt)
# print(arrange_corr)
# print(arrange_rt)
# print(len(direction_corr)+len(location_corr)+len(arrange_corr))

# 求正确率
def correct(data):
    right=0
    total=0
    for i in range(len(data)):
        if  data[i] =='1':
            total += 1
            right += 1
        else :
            total += 1
    ratio=right/total
    ratio=ratio*100
    return  ratio

# 求反应时平均值及方差
def aver(data):
    raw_rt=[]
    for i in range(len(data)):
        raw_rt.append(float(data[i]))
    aver=numpy.mean(raw_rt)
    std1=numpy.std(raw_rt)
    return aver,std1

# 计算结果
total_rt=[direction_rt,location_rt,arrange_rt]
total_corr=[direction_corr,location_corr,arrange_corr]
for i in range(len(total_rt)):
    aver_con,std=aver(total_rt[i])
    reacttime.append(aver_con)
    Standard_Deviation.append(std)
for i in total_corr:
    corratio_con=correct(i)
    corratio.append(corratio_con)
#print(reacttime)
# print(Standard_Deviation)
# print(corratio)
total=['空间方向','空间位置','空间排列']

# 数据输出
# print("—————————————————————————————")
# print("    分类          准确率        反应时         标准差")
# print("—————————————————————————————")
# for i in range(0,3):
#     print("   {}        {:.2f}%       {:.5f}        {:.5f}".format(total[i],corratio[i],reacttime[i],Standard_Deviation[i]))
# print("—————————————————————————————")

# 绘图
import matplotlib.pyplot as plt
plt.style.use('ggplot')
#解决中文显示问题
plt.rcParams['font.sans-serif'] = ['KaiTi'] # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题
# 平均反应时
fig=plt.figure()
ax1=fig.add_subplot(1,1,1)
ax1.bar(total, reacttime, align='center', color='darkblue',width=0.3)
ax1.errorbar(x=total,y=reacttime,yerr=Standard_Deviation,ecolor='grey',capsize=4,color='black',fmt='o')
# ax1.bar(expression,corratio,align='center',color='red')
ax1.xaxis.set_ticks_position("bottom")
ax1.yaxis.set_ticks_position("left")
plt.xlabel('Scene_Recognition_Task')
plt.ylabel('时间(秒)')
plt.title('图1：平均反应时间（秒）')
plt.savefig('reaction_time.png',dpi=400,bbox_inches='tight')
# plt.show()
# 平均准确率
fig1=plt.figure()
ax2=fig1.add_subplot(1,1,1)
ax2.bar(total,corratio,align='center',color='darkblue',width=0.3)
ax2.xaxis.set_ticks_position("bottom")
ax2.yaxis.set_ticks_position("left")
plt.xlabel('Scene_Recognition_Task')
plt.ylabel('准确率（%）')
plt.title('图2：平均准确率')
plt.savefig('correction_ratio.png',dpi=400,bbox_inches='tight')
# plt.show()

# 绘制pdf文档
pdf.add_page()
pdf.add_font('hei','',fname=r'C:\Windows\Fonts\simhei.ttf',uni=True)
pdf.set_font("hei", size=18)
pdf.cell(180, 20, txt="电脑认知测试六：空间识别能力", ln=1, align="C")
pdf.set_font('hei',size=12)
pdf.cell(180,13,txt='姓名：'+name,ln=1)
pdf.cell(180,13,txt='时间：'+expri_time,ln=1)
pdf.cell(180,7,txt='—————————————————————————',ln=1,align="C")
pdf.cell(180,7,txt='分类        准确率        反应时(秒)        标准差',ln=1,align='C')
pdf.cell(180,7,txt='—————————————————————————',ln=1,align='C')
for i in range(0,3):
    text="{}        {:.2f}%        {:.5f}       {:.5f}".format(total[i],corratio[i],reacttime[i],Standard_Deviation[i])
    pdf.cell(180,7,txt=text,ln=1,align="C")
pdf.cell(180,7,txt='—————————————————————————',ln=1,align='C')
pdf.image('reaction_time.png',x=0,y=160,w=100,h=86)
pdf.image('correction_ratio.png',x=110,y=160,w=100,h=86)
print("测试六文件处理完成。")

# 测试七
reacttime = []
corratio = []
Standard_Deviation = []
if times == '1':
    filename=filename1[-1]+'_time1_Flanker'
elif times == '2':
    filename = filename1[-1]+'_time2_Flanker'
elif times == '3':
    filename = filename1[-1]+'_mother_Flanker'
elif times == '4':
    filename = filename1[-1] + '_father_Flanker'
else:
    filename = filename1[-1] + '_time1_Flanker'
for files in os.listdir('/'.join(filename1) + '/7_Flanker/'):
    if filename in files and '.csv' in files:
        expri_time=files[-20:-4]
        filename='/'.join(filename1) + '/7_Flanker/'+files
print("测试七文件开始处理。")
# 文件数据读取
f = open(filename, 'r', encoding='utf-8')
filereader = csv.reader(f)
same_list_rt=[]
same_list_corr=[]
opposed_list_rt=[]
opposed_list_corr=[]
for i,line in enumerate(filereader):
    if i==0:
        for j in range(len(line)):
            if line[j] == 'key_resp.corr':
                corr_num=j
            if line[j] == 'key_resp.rt':
                rt_num=j

    if line[0] == '>><>>' or line[0] =='<<><<':
        opposed_list_corr.append(str(line[corr_num]).strip())
        if line[corr_num] =='1':
            opposed_list_rt.append(float(str(line[rt_num]).strip()))
    if line[0] == '<<<<<' or line[0] == '>>>>>':
        same_list_corr.append(str(line[corr_num]).strip())
        if line[corr_num] == '1':
            same_list_rt.append(float(str(line[rt_num]).strip()))
# print(same_list_corr,same_list_rt)
# print(opposed_list_corr,opposed_list_rt)
# print(len(opposed_list_corr)+len(same_list_corr))

# 求反应时平均值及方差
def aver(data):
    raw_rt=[]
    for i in range(len(data)):
        raw_rt.append(float(data[i]))
    aver=numpy.mean(raw_rt)
    std1=numpy.std(raw_rt)
    return aver,std1

# 求正确率
def correct(data):
    right=0
    total=0
    for i in range(len(data)):
        if  data[i] =='1':
            total += 1
            right += 1
        else :
            total += 1
    ratio=right/total
    ratio=ratio*100
    return  ratio

# 计算结果
total_rt=[same_list_rt,opposed_list_rt]
total_corr=[same_list_corr,opposed_list_corr]
for i in range(len(total_rt)):
    aver_con,std=aver(total_rt[i])
    reacttime.append(aver_con)
    Standard_Deviation.append(std)
for i in total_corr:
    corratio_con=correct(i)
    corratio.append(corratio_con)
# print(reacttime)
# print(Standard_Deviation)
# print(corratio)

total=['不冲突','冲突']
# # 数据输出
# print("—————————————————————————————")
# print("不冲突/冲突       准确率        反应时         标准差")
# print("—————————————————————————————")
# for i in range(0,2):
#     print("   {}        {:.2f}%       {:.5f}        {:.5f}".format(total[i],corratio[i],reacttime[i],Standard_Deviation[i]))
# print("—————————————————————————————")

# 绘图
import matplotlib.pyplot as plt
plt.style.use('ggplot')
#解决中文显示问题
plt.rcParams['font.sans-serif'] = ['KaiTi'] # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题
# 平均反应时
fig=plt.figure()
ax1=fig.add_subplot(1,1,1)
ax1.bar(total, reacttime, align='center', color='darkblue',width=0.3)
ax1.errorbar(x=total,y=reacttime,yerr=Standard_Deviation,ecolor='grey',capsize=4,color='black',fmt='o')
# ax1.bar(expression,corratio,align='center',color='red')
ax1.xaxis.set_ticks_position("bottom")
ax1.yaxis.set_ticks_position("left")
plt.xlabel('Flanker')
plt.ylabel('时间(秒)')
plt.title('图1：平均反应时间（秒）')
plt.savefig('reaction_time.png',dpi=400,bbox_inches='tight')
# plt.show()
# 平均准确率
fig1=plt.figure()
ax2=fig1.add_subplot(1,1,1)
ax2.bar(total,corratio,align='center',color='darkblue',width=0.3)
ax2.xaxis.set_ticks_position("bottom")
ax2.yaxis.set_ticks_position("left")
plt.xlabel('Flanker')
plt.ylabel('准确率（%）')
plt.title('图2：平均准确率')
plt.savefig('correction_ratio.png',dpi=400,bbox_inches='tight')
# plt.show()

# 绘制pdf文档
pdf.add_page()
pdf.add_font('hei','',fname=r'C:\Windows\Fonts\simhei.ttf',uni=True)
pdf.set_font("hei", size=18)
pdf.cell(180, 20, txt="电脑认知测试七：空间冲突解决能力", ln=1, align="C")
pdf.set_font('hei',size=12)
pdf.cell(180,13,txt='姓名：'+name,ln=1)
pdf.cell(180,13,txt='时间：'+expri_time,ln=1)
pdf.cell(180,7,txt='———————————————————————————————',ln=1,align="C")
pdf.cell(180,7,txt='不冲突/冲突       准确率        反应时(秒)        标准差',ln=1,align='C')
pdf.cell(180,7,txt='———————————————————————————————',ln=1,align='C')
for i in range(0,2):
    text="{}        {:.2f}%        {:.5f}       {:.5f}".format(total[i],corratio[i],reacttime[i],Standard_Deviation[i])
    pdf.cell(180,7,txt=text,ln=1,align="C")
pdf.cell(180,7,txt='———————————————————————————————',ln=1,align='C')
pdf.image('reaction_time.png',x=0,y=160,w=100,h=86)
pdf.image('correction_ratio.png',x=110,y=160,w=100,h=86)
print("测试七文件处理完成。")

# 测试八
reacttime = []
corratio = []
Standard_Deviation = []
if times == '1':
    filename=filename1[-1]+'_time1_Task_Switching'
elif times == '2':
    filename = filename1[-1]+'_time2_Task_Switching'
elif times == '3':
    filename = filename1[-1]+'_mother_Task_Switching'
elif times == '4':
    filename = filename1[-1] + '_father_Task_Switching'
else:
    filename = filename1[-1] + '_time1_Task_Switching'
for files in os.listdir('/'.join(filename1) + '/8_Task_Switching/'):
    if filename in files and '.csv'in files:
        expri_time=files[-20:-4]
        filename='/'.join(filename1) + '/8_Task_Switching/'+files

print("测试八文件开始处理。")
# 文件数据读取
f = open(filename, 'r', encoding='utf-8')
filereader = csv.reader(f)
convertion_rt=[]
unconvertion_rt=[]
convertion_corr=[]
unconvertion_corr=[]
for i,line in enumerate(filereader):
    if i==0:
        for j in range(len(line)):
            if line[j] == 'condition':
                condition_num = j
            if line[j] == 'key_resp_formal.corr':
                corr_num = j
            if line[j] == 'key_resp_formal.rt':
                rt_num=j
    if line[condition_num] == 'no_c':
        unconvertion_corr.append(str(line[corr_num]).strip())
        if str(line[corr_num]).strip() == '1':
            unconvertion_rt.append(float(str(line[rt_num]).strip()))
    if line[condition_num] == 'c':
        convertion_corr.append(str(line[corr_num]).strip())
        if str(line[corr_num]) == '1':
            convertion_rt.append(float(str(line[rt_num]).strip()))
# print(convertion_rt,unconvertion_rt)
# print(convertion_corr,unconvertion_corr)
# print(len(convertion_corr)+len(unconvertion_corr))

# 求正确率
def correct(data):
    right=0
    total=0
    for i in range(len(data)):
        if  data[i] =='1':
            total += 1
            right += 1
        else :
            total += 1
    ratio=right/total
    ratio=ratio*100
    return  ratio

# 求反应时平均值及方差
def aver(data):
    raw_rt=[]
    for i in range(len(data)):
        raw_rt.append(float(data[i]))
    aver=numpy.mean(raw_rt)
    std1=numpy.std(raw_rt)
    return aver,std1

# 求反应时平均值及方差
def aver(data):
    raw_rt=[]
    for i in range(len(data)):
        raw_rt.append(float(data[i]))
    aver=numpy.mean(raw_rt)
    std1=numpy.std(raw_rt)
    return aver,std1

# 计算结果
total_rt=[convertion_rt,unconvertion_rt]
total_corr=[convertion_corr,unconvertion_corr]
for i in range(len(total_rt)):
    aver_con,std=aver(total_rt[i])
    reacttime.append(aver_con)
    Standard_Deviation.append(std)
for i in total_corr:
    corratio_con=correct(i)
    corratio.append(corratio_con)
# print(reacttime)
# print(Standard_Deviation)
total=['转化','不转化']

# 数据输出
# print("—————————————————————————————")
# print("转化/不转化       准确率        反应时         标准差")
# print("—————————————————————————————")
# for i in range(0,2):
#     print("   {}        {:.2f}%       {:.5f}        {:.5f}".format(total[i],corratio[i],reacttime[i],Standard_Deviation[i]))
# print("—————————————————————————————")

# 绘图
import matplotlib.pyplot as plt
plt.style.use('ggplot')
#解决中文显示问题
plt.rcParams['font.sans-serif'] = ['KaiTi'] # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题
# 平均反应时
fig=plt.figure()
ax1=fig.add_subplot(1,1,1)
ax1.bar(total, reacttime, align='center', color='darkblue',width=0.3)
ax1.errorbar(x=total,y=reacttime,yerr=Standard_Deviation,ecolor='grey',capsize=4,color='black',fmt='o')
# ax1.bar(expression,corratio,align='center',color='red')
ax1.xaxis.set_ticks_position("bottom")
ax1.yaxis.set_ticks_position("left")
plt.xlabel('Task_Switching')
plt.ylabel('时间(秒)')
plt.title('图1：平均反应时间（秒）')
plt.savefig('reaction_time.png',dpi=400,bbox_inches='tight')
# plt.show()
# 平均准确率
fig1=plt.figure()
ax2=fig1.add_subplot(1,1,1)
ax2.bar(total,corratio,align='center',color='darkblue',width=0.3)
ax2.xaxis.set_ticks_position("bottom")
ax2.yaxis.set_ticks_position("left")
plt.xlabel('Task_Switching')
plt.ylabel('准确率（%）')
plt.title('图2：平均准确率')
plt.savefig('correction_ratio.png',dpi=400,bbox_inches='tight')
# plt.show()

# 绘制pdf文档
pdf.add_page()
pdf.add_font('hei','',fname=r'C:\Windows\Fonts\simhei.ttf',uni=True)
pdf.set_font("hei", size=18)
pdf.cell(180, 20, txt="电脑认知测试八：任务切换能力", ln=1, align="C")
pdf.set_font('hei',size=12)
pdf.cell(180,13,txt='姓名：'+name,ln=1)
pdf.cell(180,13,txt='时间：'+expri_time,ln=1)
pdf.cell(180,7,txt='———————————————————————————',ln=1,align="C")
pdf.cell(180,7,txt='转化/不转化      准确率       反应时(秒)       标准差',ln=1,align='C')
pdf.cell(180,7,txt='———————————————————————————',ln=1,align='C')
for i in range(0,2):
    text="{}       {:.2f}%       {:.5f}      {:.5f}".format(total[i],corratio[i],reacttime[i],Standard_Deviation[i])
    pdf.cell(180,7,txt=text,ln=1,align="C")
pdf.cell(180,7,txt='———————————————————————————',ln=1,align='C')
pdf.image('reaction_time.png',x=0,y=160,w=100,h=86)
pdf.image('correction_ratio.png',x=110,y=160,w=100,h=86)
print("测试八文件处理完成。")

# 测试九
reacttime = []
corratio = []
Standard_Deviation = []
if times == '1':
    filename=filename1[-1]+'_time1_Simple_Guessing_Task'
elif times == '2':
    filename = filename1[-1]+'_time2_Simple_Guessing_Task'
elif times == '3':
    filename = filename1[-1]+'_mother_Simple_Guessing_Task'
elif times == '4':
    filename = filename1[-1] + '_father_Simple_Guessing_Task'
else:
    filename = filename1[-1] + '_time1_Simple_Guessing_Task'
for files in os.listdir('/'.join(filename1) + '/9_Simple_Guessing_Task/'):
    if filename in files and '.csv' in files:
        expri_time=files[-20:-4]
        filename='/'.join(filename1) + '/9_Simple_Guessing_Task/'+files

print("测试九文件开始处理。")
# 文件数据读取
f = open(filename, 'r', encoding='utf-8')
filereader = csv.reader(f)
sentence=[]
rt=[]
for i,line in enumerate(filereader):
    if i==0:
        for j in range(len(line)):
            if line[j] == 'fdb2':
                sentence_num=j
            if line[j] == 'key_resp_formal1.rt':
                rt_num=j
    if line[sentence_num] =='恭喜你，猜对了！' or line[sentence_num] == '很遗憾，你猜错了。':
         sentence.append(str(line[sentence_num]).strip())
    try :
        rt.append(eval(str(line[rt_num]).strip()))
    except:
        pass
# print(sentence)
# print(rt)
# print(len(sentence)+len(rt))

# 求反应时平均值及方差
def aver(data):
    raw_rt=[]
    for i in range(len(data)):
        raw_rt.append(float(data[i]))
    aver=numpy.mean(raw_rt)
    std1=numpy.std(raw_rt)
    return aver,std1


def chunks(arr, n):
    return [arr[i:i+n] for i in range(0, len(arr), n)]
rt=chunks(rt,16)
sentence=chunks(sentence,16)
def select(sen_data,rt_data):
    rt_right=[]
    rt_wrong=[]
    for i in range(len(sen_data)-1):
        if sen_data[i] == '恭喜你，猜对了！':
            rt_right.append(rt_data[i+1])
        if sen_data[i] == '很遗憾，你猜错了。':
            rt_wrong.append(rt_data[i+1])
    aver_right,std_right=aver(rt_right)
    aver_wrong,std_wrong=aver(rt_wrong)
    return aver_right,std_right,aver_wrong,std_wrong

reacttime_right=[]
reacttime_wrong=[]
std_right=[]
std_wrong=[]

for i in range(len(sentence)):
    aver1,std1,aver2,std2=select(sentence[i],rt[i])
    reacttime_right.append(aver1)
    reacttime_wrong.append(aver2)
    std_right.append(std1)
    std_wrong.append(std2)

total=['阶段1','阶段2','阶段3','阶段4']
total_right=['阶段1获利','阶段2获利','阶段3获利','阶段4获利']
total_wrong=['阶段1损失','阶段2损失','阶段3损失',"阶段4损失"]
x=range(len(total))

# 绘图
import matplotlib.pyplot as plt
total_index=len(total)
plt.style.use('ggplot')

#解决中文显示问题
plt.rcParams['font.sans-serif'] = ['KaiTi'] # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题

# 平均反应时
fig=plt.figure()
bar_width='   '
aver_s=numpy.array(reacttime_right)
aver_o=numpy.array(reacttime_wrong)
ax1=fig.add_subplot(1,1,1)
ax1.bar(x,aver_s,width=0.4, color='darkblue',label='获利后下次反应时')
ax1.errorbar(x,y=aver_s,yerr=std_right,ecolor='grey',capsize=4,color='black',fmt='o')
ax1.bar([i+0.4 for i in x],aver_o,width=0.4,color='red',label='损失后下次反应时')
ax1.errorbar([i+0.4 for i in x],y=aver_o,yerr=std_wrong,ecolor='grey',capsize=4,color='black',fmt='o')
# ax1.bar(expression,corratio,align='center',color='red')
plt.xticks([i+0.2 for i in x],total,fontsize=10)
ax1.xaxis.set_ticks_position("bottom")
ax1.yaxis.set_ticks_position("left")
plt.xlabel('不同阶段')
plt.ylabel('时间(秒)')
plt.title('图1：平均反应时间（秒）')
plt.legend()
plt.savefig('reaction_time.png',dpi=400,bbox_inches='tight')
# plt.show()

# 绘制pdf文档
pdf.add_page()
pdf.add_font('hei','',fname=r'C:\Windows\Fonts\simhei.ttf',uni=True)
pdf.set_font("hei", size=18)
pdf.cell(180, 20, txt="电脑认知测试九：奖赏反应情况", ln=1, align="C")
pdf.set_font('hei',size=12)
pdf.cell(180,13,txt='姓名：'+name,ln=1)
pdf.cell(180,13,txt='时间：'+expri_time,ln=1)
pdf.cell(180,7,txt='—————————————————————————',ln=1,align="C")
pdf.cell(180,7,txt='  不同阶段         反应时(秒)        标准差',ln=1,align='C')
pdf.cell(180,7,txt='—————————————————————————',ln=1,align='C')
for i in range(0,4):
    text1="{}         {:.5f}       {:.5f}".format(total_right[i],reacttime_right[i],std_right[i])
    text2="{}         {:.5f}       {:.5f}".format(total_wrong[i],reacttime_wrong[i],std_wrong[i])
    pdf.cell(180,7,txt=text1,ln=2,align="C")
    pdf.cell(180,7,txt=text2,ln=2,align="C")
pdf.cell(180,7,txt='—————————————————————————',ln=1,align='C')
pdf.image('reaction_time.png',x=50,y=160,w=100,h=86)
print("测试九文件处理完成。")

# 测试十
reacttime = []
corratio = []
Standard_Deviation = []
if times == '1':
    filename=filename1[-1]+'_time1_Delay_Discounting_Task'
elif times == '2':
    filename = filename1[-1]+'_time2_Delay_Discounting_Task'
elif times == '3':
    filename = filename1[-1]+'_mother_Delay_Discounting_Task'
elif times == '4':
    filename = filename1[-1] + '_father_Delay_Discounting_Task'
else:
    filename = filename1[-1] + '_time1_Delay_Discounting_Task'
for files in os.listdir('/'.join(filename1) + '/10_Delay_Discounting_Task/'):
    if filename in files and '.csv' in files:
        expri_time=files[-20:-4]
        filename='/'.join(filename1) + '/10_Delay_Discounting_Task/'+files

print("测试十文件开始处理。")
# 文件数据读取
f = open(filename, 'r', encoding='utf-8')
filereader = csv.reader(f)
one_week=[]
two_weeks=[]
one_month=[]
six_months=[]
one_year=[]
five_years=[]
twenty_five_years=[]

for i,line in enumerate(filereader):
    if i==0:
        for j in range(len(line)):
            if line[j] == 'key_resp_1week.keys':
                one_week_num=j
            if line[j] == 'key_resp_2weeks.keys':
                two_weeks_num=j
            if line[j]=='key_resp_1month.keys':
                one_month_num=j
            if line[j] == 'key_resp_6months.keys':
                six_months_num=j
            if line[j] == 'key_resp_1year.keys':
                one_year_num=j
            if line[j] == 'key_resp5years.keys':
                five_years_num=j
            if line[j] == 'key_resp25years.keys':
                twenty_five_years_num=j
    if line[one_week_num] =='right' or line[one_week_num] == 'left':
         one_week.append(str(line[one_week_num]).strip())
    if line[two_weeks_num] == 'right' or line[two_weeks_num] == 'left':
        two_weeks.append(str(line[two_weeks_num]).strip())
    if line[one_month_num] == 'right' or line[one_month_num] == 'left':
        one_month.append(str(line[one_month_num]).strip())
    if line[six_months_num] == 'right' or line[six_months_num] == 'left':
        six_months.append(str(line[six_months_num]).strip())
    if line[one_year_num] == 'right' or line[one_year_num] == 'left':
        one_year.append(str(line[one_year_num]).strip())
    if line[five_years_num] == 'right' or line[five_years_num] == 'left':
        five_years.append(str(line[five_years_num]).strip())
    if line[twenty_five_years_num] == 'right' or line[twenty_five_years_num] == 'left':
        twenty_five_years.append(str(line[twenty_five_years_num]).strip())
# print(one_week)
# print(one_month)
# print(one_year)
# print(two_weeks)
# print(six_months)

def expected(data):
    x=500
    y=4
    for i in range(len(data)):
        if data[i] == 'left':
            x-=1000/y
        if  data[i] == 'right':
            x+=1000/y
        y*=2
    return x

total=[one_week,two_weeks,one_month,six_months,one_year,five_years,twenty_five_years]
expect=[]
for i in total:
    expect.append(expected(i))
# print(expect)

total=['一周','两周','一个月','六个月','一年','五年','二十五年']

# # 数据输出
# print("—————————————————————————————")
# print("           时间                预期")
# print("—————————————————————————————")
# for i in range(0,5):
#     print("           {}                {:.5f}".format(total[i],expect[i]))
# print("—————————————————————————————")

# 绘图
import matplotlib.pyplot as plt
plt.style.use('ggplot')
#解决中文显示问题
plt.rcParams['font.sans-serif'] = ['KaiTi'] # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题
# 平均反应时
fig=plt.figure()
ax1=fig.add_subplot(1,1,1)
ax1.bar(total, expect, align='center', color='darkblue',width=0.3)
# ax1.bar(expression,corratio,align='center',color='red')
ax1.xaxis.set_ticks_position("bottom")
ax1.yaxis.set_ticks_position("left")
plt.xlabel('延迟时间')
plt.ylabel('金币数')
plt.title('图1：预期期望')
plt.savefig('expectancy.png',dpi=400,bbox_inches='tight')
# plt.show()

# 绘制pdf文档
pdf.add_page()
pdf.add_font('hei','',fname=r'C:\Windows\Fonts\simhei.ttf',uni=True)
pdf.set_font("hei", size=18)
pdf.cell(180, 20, txt="电脑认知测试十：延迟满足能力", ln=1, align="C")
pdf.set_font('hei',size=12)
pdf.cell(180,13,txt='姓名：'+name,ln=1)
pdf.cell(180,13,txt='时间：'+expri_time,ln=1)
pdf.cell(180,7,txt='———————————————————————————',ln=1,align="C")
pdf.cell(180,7,txt='        延迟时间           即时获得金币(对比1000金币)  ',ln=1,align='C')
pdf.cell(180,7,txt='———————————————————————————',ln=1,align='C')
for i in range(0,7):
    text="  {}                     {:.5f}".format(total[i],expect[i])
    pdf.cell(180,7,txt=text,ln=1,align="C")
pdf.cell(180,7,txt='———————————————————————————',ln=1,align='C')
pdf.image('expectancy.png',x=50,y=160,w=100,h=86)
print("测试十文件处理完成。")

# 测试十一
reacttime = []
corratio = []
Standard_Deviation = []
if times == '1':
    filename=filename1[-1]+'_time1_Time_Perception'
elif times == '2':
    filename = filename1[-1]+'_time2_Time_Perception'
elif times == '3':
    filename = filename1[-1]+'_mother_Time_Perception'
elif times == '4':
    filename = filename1[-1] + '_father_Time_Perception'
else:
    filename = filename1[-1] + '_time1_Time_Perception'
for files in os.listdir('/'.join(filename1) + '/11_Time_Perception/'):
    if filename in files and '.csv'in files:
        expri_time=files[-20:-4]
        filename='/'.join(filename1) + '/11_Time_Perception/'+files
print("测试十一文件开始处理。")
# 文件数据读取
f = open(filename, 'r', encoding='utf-8')
filereader = csv.reader(f)
audio_rt=[]
image_rt=[]
timespan=[]
for i,line in enumerate(filereader):
    if i==0:
        for j in range(len(line)):
            if line[j] == 'key_resp_12.rt':
                audio_num=j
            if line[j] == 'key_resp_10.rt':
                image_num=j
            if line[j]=='key_resp_12.keys':
                switch1=j
            if line[j] == 'key_resp_10.keys':
                switch2=j
    if line[switch1] == 'right':
        audio_rt.append(float(str(line[audio_num]).strip())-float(str(line[0]).strip()))
    if line[switch2] == 'right':
        image_rt.append(float(str(line[image_num]).strip()) - float(str(line[0]).strip()))
# print(audio_rt)
# print(image_rt)
# print(len(audio_rt)+len(image_rt))

# 求正确率
def correct(data):
    right=0
    total=0
    for i in range(len(data)):
        if  data[i] =='1':
            total += 1
            right += 1
        else :
            total += 1
    ratio=right/total
    ratio=ratio*100
    return  ratio

# 求反应时平均值及方差
def aver(data):
    raw_rt=[]
    for i in range(len(data)):
        raw_rt.append(float(data[i]))
    aver=numpy.mean(raw_rt)
    std1=numpy.std(raw_rt)
    return aver,std1

# 计算结果
total_rt=[audio_rt,image_rt]
for i in range(len(total_rt)):
    aver_con,std=aver(total_rt[i])
    reacttime.append(aver_con)
    Standard_Deviation.append(std)
# print(reacttime)
# print(Standard_Deviation)
total=['听觉','视觉']

# # 数据输出
# print("—————————————————————————————")
# print("   知觉          误差          标准差")
# print("—————————————————————————————")
# for i in range(0,2):
#     print("   {}        {:.5f}        {:.5f}".format(total[i],reacttime[i],Standard_Deviation[i]))
# print("—————————————————————————————")

# 绘图
import matplotlib.pyplot as plt
plt.style.use('ggplot')
#解决中文显示问题
plt.rcParams['font.sans-serif'] = ['KaiTi'] # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题
# 平均反应时
fig=plt.figure()
ax1=fig.add_subplot(1,1,1)
ax1.bar(total, reacttime, align='center', color='darkblue',width=0.3)
ax1.errorbar(x=total,y=reacttime,yerr=Standard_Deviation,ecolor='grey',capsize=4,color='black',fmt='o')
# ax1.bar(expression,corratio,align='center',color='red')
ax1.xaxis.set_ticks_position("bottom")
ax1.yaxis.set_ticks_position("left")
plt.xlabel('Time_Perception')
plt.ylabel('时间(秒)')
plt.title('图1：误差时间（秒）')
plt.savefig('reaction_time.png',dpi=400,bbox_inches='tight')
# plt.show()

# 绘制pdf文档
pdf.add_page()
pdf.add_font('hei','',fname=r'C:\Windows\Fonts\simhei.ttf',uni=True)
pdf.set_font("hei", size=18)
pdf.cell(180, 20, txt="电脑认知测试十一：视觉和听觉的时间知觉能力", ln=1, align="C")
pdf.set_font('hei',size=12)
pdf.cell(180,13,txt='姓名：'+name,ln=1)
pdf.cell(180,13,txt='时间：'+expri_time,ln=1)
pdf.cell(180,7,txt='———————————————————————',ln=1,align="C")
pdf.cell(180,7,txt='知觉        误差时间（秒）       标准差',ln=1,align='C')
pdf.cell(180,7,txt='———————————————————————',ln=1,align='C')
for i in range(0,2):
    text="{}        {:.5f}       {:.5f}".format(total[i],reacttime[i],Standard_Deviation[i])
    pdf.cell(180,7,txt=text,ln=1,align="C")
pdf.cell(180,7,txt='———————————————————————',ln=1,align='C')
pdf.image('reaction_time.png',x=50,y=160,w=100,h=86)
pdf.output(pdfname)
print("测试十一文件处理完成。")

os.remove('correction_ratio.png')
os.remove('expectancy.png')
os.remove('reaction_time.png')
import tkinter as tk
def quit(root):
    root.destroy()
root=tk.Tk()
root.title('提示')
root.geometry('300x170+600+300')
w1 = tk.Label(root,text='测试数据已处理完成',font='黑体 15 ')
w1.pack(pady=30)
b1=tk.Button(root,text='确定',font='song 11',width=15,command=lambda root=root:quit(root))
b1.pack(anchor='center',pady=10)
root.mainloop()