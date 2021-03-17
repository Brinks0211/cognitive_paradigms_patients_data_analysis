import csv
import numpy
import tkinter as tk
from tkinter.filedialog import askopenfilename
reacttime = []
corratio = []
Standard_Deviation = []

# GUI
root = tk.Tk()
root.wm_title("9_Simple_Guessing_Task")
root.geometry("700x200")
path=tk.StringVar()
w0=tk.Label(root, text='9_Simple_Guessing_Task',width=40)
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
plt.show()

# 绘制pdf文档
from fpdf import FPDF
pdf = FPDF('p','mm','A4')
pdf.add_page()
pdf.add_font('hei','',fname=r'C:\Windows\Fonts\simhei.ttf',uni=True)
pdf.set_font("hei", size=18)
pdf.cell(180, 20, txt="电脑认知测试九：奖赏反应情况", ln=1, align="C")
pdf.set_font('hei',size=12)
pdf.cell(180,13,txt='姓名：'+name,ln=1)
pdf.cell(180,13,txt='时间：'+time,ln=1)
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
pdf.output("9_Simple_Guessing_Task.pdf")

print("文件处理完成。")