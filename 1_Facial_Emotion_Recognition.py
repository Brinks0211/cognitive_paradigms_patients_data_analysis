import csv
import numpy
import tkinter as tk
from tkinter.filedialog import askopenfilename
reacttime = []
corratio = []
Standard_Deviation = []

# GUI
root = tk.Tk()
root.wm_title("1_Facial_Emotion_Recognition")
root.geometry("700x200")
path=tk.StringVar()
w0=tk.Label(root, text='1_Facial_Emotion_Recognition',width=40)
w0.place(x=190,y=10)
w1=tk.Label(root, text='姓名：').place(x=10, y=60)
name=tk.Entry(root, width=60)
name.place(x=100,y=60)
w2=tk.Label(root, text="时间：").place(x=10, y=90)
time=tk.Entry(root, width=60)
time.place(x=100, y=90)
w3=tk.Label(root, text='文件路径：').place(x=10, y=120)
path1=tk.Entry(root, textvariable=path, width=60)
path1.place(x=100, y=120)
def selectpath():
    path_ = askopenfilename()
    path.set(path_)
def filepathget():
    global filename,time,name
    name=name.get()
    time=time.get()
    filename=path1.get()
    # print(filename)
    root.withdraw()
    root.destroy()
b1 = tk.Button(root, text='确定', font=('Arial', 12), width=10,command=filepathget)
b1.place(x=300, y=150)
b2 = tk.Button(root,text="选择文件",font=('Arial', 10),width=7, height=1, command=selectpath)
b2.place(x=530, y=120)
root.mainloop()

print("文件开始处理。")
# 文件数据读取
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

# #输出表格
# print("—————————————————————————————")
# print("表情        准确率        反应时         标准差")
# print("—————————————————————————————")
# for i in range(0,7):
#     print("{}       {:.2f}%       {:.5f}        {:.5f}".format(expression[i],corratio[i],reacttime[i],Standard_Deviation[i]))
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
plt.show()

# 绘制pdf
from fpdf import FPDF
pdf = FPDF('p','mm','A4')
pdf.add_page()
pdf.add_font('hei','',fname=r'C:\Windows\Fonts\simhei.ttf',uni=True)
pdf.set_font("hei", size=18)
pdf.cell(180, 20, txt="电脑认知测试一：面孔情绪识别能力", ln=1, align="C")
pdf.set_font('hei',size=12)
pdf.cell(180,13,txt='姓名：'+name,ln=1)
pdf.cell(180,13,txt='时间：'+time,ln=1)
pdf.cell(180,7,txt='—————————————————————————',ln=1,align="C")
pdf.cell(180,7,txt='表情       准确率        反应时(秒)        标准差',ln=1,align='C')
pdf.cell(180,7,txt='—————————————————————————',ln=1,align='C')
for i in range(0,6):
    text="{}        {:.2f}%        {:.5f}       {:.5f}".format(expression[i],corratio[i],reacttime[i],Standard_Deviation[i])
    pdf.cell(180,7,txt=text,ln=1,align="C")
pdf.cell(180,7,txt='—————————————————————————',ln=1,align='C')
pdf.image('reaction_time.png',x=0,y=160,w=100,h=86)
pdf.image('correction_ratio.png',x=110,y=160,w=100,h=86)
pdf.output("1_Facial_Emotion_Recognition.pdf")

print("文件处理完成。")