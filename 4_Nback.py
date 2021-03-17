import csv
import numpy
import tkinter as tk
from tkinter.filedialog import askopenfilename
reacttime = []
corratio = []
Standard_Deviation = []

# GUI
root = tk.Tk()
root.wm_title("4_Nback")
root.geometry("700x200")
path=tk.StringVar()
w0=tk.Label(root, text='4_Nback',width=40)
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
back0_rt_list=[]
back0_rt_list1=[]
back1_corr_list=[]
back2_corr_list=[]
back1_rt_list=[]
back2_rt_list=[]
for i,line in enumerate(filereader):
    if i==0:
        for j in range(len(line)):
            if line[j] == 'key_resp_0back.rt':
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
print(reacttime)
print(Standard_Deviation)
print(corratio)

corratio_print=[100]+corratio
back_rt_list=['0back','1back','2back']
# 数据输出
print("—————————————————————————————")
print("    Nback       准确率        反应时         标准差")
print("—————————————————————————————")
for i in range(0,3):
    print("   {}        {:.2f}%       {:.5f}        {:.5f}".format(back_rt_list[i],corratio_print[i],reacttime[i],Standard_Deviation[i]))
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
ax1.bar(back_rt_list, reacttime, align='center', color='darkblue',width=0.3)
ax1.errorbar(x=back_rt_list,y=reacttime,yerr=Standard_Deviation,ecolor='grey',capsize=4,color='black',fmt='o')
# ax1.bar(expression,corratio,align='center',color='red')
ax1.xaxis.set_ticks_position("bottom")
ax1.yaxis.set_ticks_position("left")
plt.xlabel('Nback')
plt.ylabel('时间(秒)')
plt.title('图1：平均反应时间（秒）')
plt.savefig('reaction_time.png',dpi=400,bbox_inches='tight')
plt.show()
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
plt.show()

# 绘制pdf文档
from fpdf import FPDF
pdf = FPDF('p','mm','A4')
pdf.add_page()
pdf.add_font('hei','',fname=r'C:\Windows\Fonts\simhei.ttf',uni=True)
pdf.set_font("hei", size=18)
pdf.cell(180, 20, txt="电脑认知测试四：短时记忆能力", ln=1, align="C")
pdf.set_font('hei',size=12)
pdf.cell(180,13,txt='姓名：'+name,ln=1)
pdf.cell(180,13,txt='时间：'+time,ln=1)
pdf.cell(180,7,txt='———————————————————————',ln=1,align="C")
pdf.cell(180,7,txt='Nback       准确率        反应时(秒)        标准差',ln=1,align='C')
pdf.cell(180,7,txt='———————————————————————',ln=1,align='C')
for i in range(0,3):
    text="{}        {:.2f}%        {:.5f}       {:.5f}".format(back_rt_list[i],corratio_print[i],reacttime[i],Standard_Deviation[i])
    pdf.cell(180,7,txt=text,ln=1,align="C")
pdf.cell(180,7,txt='———————————————————————',ln=1,align='C')
pdf.image('reaction_time.png',x=0,y=160,w=100,h=86)
pdf.image('correction_ratio.png',x=110,y=160,w=100,h=86)
pdf.output("4_Nback.pdf")

print("文件处理完成。")