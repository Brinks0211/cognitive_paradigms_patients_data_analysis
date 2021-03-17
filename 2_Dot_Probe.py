import csv
import numpy
import tkinter as tk
from tkinter.filedialog import askopenfilename
reacttime = []
reacttime1=[]
corratio = []
Standard_Deviation = []
datalist = []

# GUI
root = tk.Tk()
root.wm_title("2_Dot_Probe")
root.geometry("700x200")
path=tk.StringVar()
w0=tk.Label(root, text='2_Dot_Probe',width=40)
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
database1 = []
direction=[]
type1 = []
type2 = []
for line in filereader:
    direction_con=str(line[3].strip())
    type1_com = str(line[5]).strip()
    type2_com = str(line[6]).strip()
    rt1=str(line[43]).strip()
    rt2=str(line[62]).strip()
    corr1=str(line[42]).strip()
    corr2=str(line[61]).strip()
    rt_con=rt1+rt2
    corr_con=corr1+corr2
    # print(line)
    if rt_con !='' and rt_con != 'key_resp_trial_1.rtkey_resp_trial_2.rt':
        reacttime1.append(rt_con)
    if corr_con !='' and corr_con !='key_resp_trial_1.corrkey_resp_trial_2.corr':
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
plt.show()

# 绘制pdf文档
from fpdf import FPDF
pdf = FPDF('p','mm','A4')
pdf.add_page()
pdf.add_font('hei','',fname=r'C:\Windows\Fonts\simhei.ttf',uni=True)
pdf.set_font("hei", size=18)
pdf.cell(180, 20, txt="电脑认知测试二：注意探测能力", ln=1, align="C")
pdf.set_font('hei',size=12)
pdf.cell(180,13,txt='姓名：'+name,ln=1)
pdf.cell(180,13,txt='时间：'+time,ln=1)
pdf.cell(180,7,txt='———————————————————————————————————',ln=1,align="C")
pdf.cell(180,7,txt='表情       准确率        反应时（秒）        标准差',ln=1,align='C')
pdf.cell(180,7,txt='———————————————————————————————————',ln=1,align='C')
for i in range(0,7):
    text="{}        {:.2f}%        {:.5f}            {:.5f}".format(expression1[i],corr[i],aver1[i],std1[i])
    pdf.cell(180,7,txt=text,ln=1,align="C")
pdf.cell(180,7,txt='———————————————————————————————————',ln=1,align='C')
pdf.image('reaction_time.png',x=0,y=160,w=100,h=86)
pdf.image('correction_ratio.png',x=110,y=160,w=100,h=86)
pdf.output("电脑认知测试二：注意探测能力.pdf")

print("文件处理完成。")