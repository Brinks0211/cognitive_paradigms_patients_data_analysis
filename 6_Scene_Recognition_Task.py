import csv
import numpy
import tkinter as tk
from tkinter.filedialog import askopenfilename
reacttime = []
corratio = []
Standard_Deviation = []

# GUI
root = tk.Tk()
root.wm_title("6_Scene_Recognition_Task")
root.geometry("700x200")
path=tk.StringVar()
w0=tk.Label(root, text='6_Scene_Recognition_Task',width=40)
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
print("—————————————————————————————")
print("    分类          准确率        反应时         标准差")
print("—————————————————————————————")
for i in range(0,3):
    print("   {}        {:.2f}%       {:.5f}        {:.5f}".format(total[i],corratio[i],reacttime[i],Standard_Deviation[i]))
print("—————————————————————————————")

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
plt.show()
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
plt.show()

# 绘制pdf文档
from fpdf import FPDF
pdf = FPDF('p','mm','A4')
pdf.add_page()
pdf.add_font('hei','',fname=r'C:\Windows\Fonts\simhei.ttf',uni=True)
pdf.set_font("hei", size=18)
pdf.cell(180, 20, txt="电脑认知测试六：空间识别能力", ln=1, align="C")
pdf.set_font('hei',size=12)
pdf.cell(180,13,txt='姓名：'+name,ln=1)
pdf.cell(180,13,txt='时间：'+time,ln=1)
pdf.cell(180,7,txt='—————————————————————————',ln=1,align="C")
pdf.cell(180,7,txt='分类        准确率        反应时(秒)        标准差',ln=1,align='C')
pdf.cell(180,7,txt='—————————————————————————',ln=1,align='C')
for i in range(0,3):
    text="{}        {:.2f}%        {:.5f}       {:.5f}".format(total[i],corratio[i],reacttime[i],Standard_Deviation[i])
    pdf.cell(180,7,txt=text,ln=1,align="C")
pdf.cell(180,7,txt='—————————————————————————',ln=1,align='C')
pdf.image('reaction_time.png',x=0,y=160,w=100,h=86)
pdf.image('correction_ratio.png',x=110,y=160,w=100,h=86)
pdf.output("6_Scene_Recognition_Task.pdf")

print("文件处理完成。")