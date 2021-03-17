import csv
import numpy
import tkinter as tk
from tkinter.filedialog import askopenfilename
reacttime = []
corratio = []
Standard_Deviation = []

# GUI
root = tk.Tk()
root.wm_title("3_Go_Nogo")
root.geometry("700x200")
path=tk.StringVar()
w0=tk.Label(root, text='3_Go_Nogo',width=40)
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
plt.show()

# 绘制pdf文档
from fpdf import FPDF
pdf = FPDF('p','mm','A4')
pdf.add_page()
pdf.add_font('hei','',fname=r'C:\Windows\Fonts\simhei.ttf',uni=True)
pdf.set_font("hei", size=18)
pdf.cell(180, 20, txt="电脑认知测试三：注意探测能力", ln=1, align="C")
pdf.set_font('hei',size=12)
pdf.cell(180,13,txt='姓名：'+name,ln=1)
pdf.cell(180,13,txt='时间：'+time,ln=1)
pdf.cell(180,7,txt='———————————————————————————',ln=1,align="C")
pdf.cell(180,7,txt='灯光/表情       准确率        反应时(秒)        标准差',ln=1,align='C')
pdf.cell(180,7,txt='———————————————————————————',ln=1,align='C')
for i in range(0,2):
    text="{}        {:.2f}%        {:.5f}       {:.5f}".format(expression1[i],corratio[i],reacttime[i],Standard_Deviation[i])
    pdf.cell(180,7,txt=text,ln=1,align="C")
pdf.cell(180,7,txt='———————————————————————————',ln=1,align='C')
pdf.image('reaction_time.png',x=0,y=160,w=100,h=86)
pdf.image('correction_ratio.png',x=110,y=160,w=100,h=86)
pdf.output("3_Go_Nogo.pdf")

print("文件处理完成。")