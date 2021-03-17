import csv
import numpy
import tkinter as tk
from tkinter.filedialog import askopenfilename
reacttime = []
corratio = []
Standard_Deviation = []

# GUI
root = tk.Tk()
root.wm_title("11_Time_Perception")
root.geometry("700x200")
path=tk.StringVar()
w0=tk.Label(root, text='10_Delay_Discounting_Task',width=40)
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
one_week=[]
two_weeks=[]
one_month=[]
six_months=[]
one_year=[]

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

total=[one_week,two_weeks,one_month,six_months,one_year]
expect=[]
for i in total:
    expect.append(expected(i))
# print(expect)

total=['一周','两周','一个月','六个月','一年']

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
plt.show()

# 绘制pdf文档
from fpdf import FPDF
pdf = FPDF('p','mm','A4')
pdf.add_page()
pdf.add_font('hei','',fname=r'C:\Windows\Fonts\simhei.ttf',uni=True)
pdf.set_font("hei", size=18)
pdf.cell(180, 20, txt="电脑认知测试十：延迟满足能力", ln=1, align="C")
pdf.set_font('hei',size=12)
pdf.cell(180,13,txt='姓名：'+name,ln=1)
pdf.cell(180,13,txt='时间：'+time,ln=1)
pdf.cell(180,7,txt='———————————————————————————',ln=1,align="C")
pdf.cell(180,7,txt='        延迟时间           即时获得金币(对比1000金币)  ',ln=1,align='C')
pdf.cell(180,7,txt='———————————————————————————',ln=1,align='C')
for i in range(0,5):
    text="  {}                     {:.5f}".format(total[i],expect[i])
    pdf.cell(180,7,txt=text,ln=1,align="C")
pdf.cell(180,7,txt='———————————————————————————',ln=1,align='C')
pdf.image('expectancy.png',x=50,y=160,w=100,h=86)
pdf.output("10_Delay_Discounting_Task.pdf")

print("文件处理完成。")