import tkinter as tk
from tkinter import ttk
import numpy as np
import pandas as pd
from pandas import ExcelWriter
import requests,re
from bs4 import BeautifulSoup
import tkinter as tk
import re 
from pandas.core.frame import DataFrame
import matplotlib.pyplot as plt
from tkinter import *
global c
def ini():#起始化
    main_url = 'https://www.cwb.gov.tw/V7/forecast/taiwan/Keelung_City.htm'
    main_html = requests.get(main_url)# 用 requests 的 get 方法把網頁抓下來
    main_html.encoding = 'utf-8'
    main = BeautifulSoup(main_html.text, 'html.parser',from_encoding="utf-8")#抓主網頁
    m_info = main.find('div', {'class':'CenterMenu'})
    m_city=m_info.find_all('option')
    global city,city_n
    city = [] # 建立一個空的 list，存網址關鍵字
    city_n = []#城市名
    for c in m_city:#對每個option裡找元素和值
        city.append(c.get('value'))
        city_n.append(c.string)
 
    
ini()
def search(p):#爬蟲
    s_city="https://www.cwb.gov.tw/V7/forecast/taiwan/inc/city/"+city[p]
    tables3 = pd.read_html(s_city ,encoding="utf-8")
    a_city="https://www.cwb.gov.tw/V7/forecast/taiwan/"+city[p]
    global tables
    tables = pd.read_html(a_city ,encoding="utf-8")
    #tables3 = pd.read_html("https://www.cwb.gov.tw/V7/forecast/taiwan/inc/city/Keelung_City.htm" ,encoding="utf-8")
    week_dowload='https://www.cwb.gov.tw/V7/forecast/taiwan/Data/W11.pdf?'
    x=len(tables)
    table = tables[x-4]
    main_url = 'https://www.cwb.gov.tw/V7/forecast/taiwan/'+city[p]
    main_html = requests.get(main_url)# 用 requests 的 get 方法把網頁抓下來
    main_html.encoding = 'utf-8'
    main = BeautifulSoup(main_html.text, 'html.parser',from_encoding="utf-8")#抓主網頁
    m_info = main.find('div', {'class':'CenterMenu'})
    m_city=m_info.find_all('option')#找css標籤
    m_at = main.find('table', {'class':'FcstBoxTable01'})#找table
    m_today=m_at.find_all('img')#最近天氣
    for c in m_city:#對每個option裡找元素和值
        city.append(c.get('value'))
        city_n.append(c.string)
    t_weather=[]#最近天氣
    for t in m_today:#
        t_weather.append(t.get('title'))
    for i in range(0,3):
        tables[0].ix[i,2]=t_weather[i]
    global df_today,df_month,df_raise
    df_today=tables[0]#今明預報
    df_month=tables[1]#月均溫
    df_raise=tables[2]#日月出沒
    url = 'https://www.cwb.gov.tw/V7/forecast/taiwan/inc/city/Keelung_City.htm'
    html = requests.get(s_city)# 用 requests 的 get 方法把網頁抓下來
    html.encoding = 'utf-8'
    sp = BeautifulSoup(html.text, 'html.parser',from_encoding="utf-8")
    t1 = sp.find('table', {'class':'FcstBoxTable01'})
    tbls=sp.find_all('table')      
    tr=sp.find_all('tr')
    img_title=sp.find_all('img')# 把每個img 抓出來
    dw=[]#天氣狀況
    for link in img_title:#對每個img裡找元素title
        dw.append(link.get('title'))
    global mor,nig
    mor=['白天_天氣']
    nig=['晚上_天氣']
    for i in range(0,7):
        mor.append(dw[i])
        nig.append(dw[i+7])
    place2=[mor,nig]#合併LIST
    df0=DataFrame(place2)#list轉DF
    df1=tables3[0]
    df1.ix[0,0]="白天_溫度"
    df1.ix[1,0]="晚上_溫度"
    df0.columns = df1.columns#複製欄位名稱
    global df
    df = df1.append(df0, ignore_index=True)#直向合併、忽視舊index
    index_w = [0, 2, 1,3]
    df=df.reindex(index=index_w)#交換索引序列，完整的df
    df= df.reset_index(drop=True)#重排索引
    


LARGE_FONT= ("Verdana", 20)

#GUI版面
class Application(tk.Tk):

    def __init__(self):#宣告時會自動執行的函式
        
        super().__init__()
        
        self.wm_title("天氣易得器 U0424041_43")
        self.wm_geometry("1000x800")
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, PageOne, PageTwo, PageThree):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")  # 設定多頁面grid(row=0, column=0)
        self.show_frame(StartPage)
        
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise() #切換頁面，類似z軸
        
    def end(self):#結束視窗
        self.destroy() 

        
class StartPage(tk.Frame):
    def __init__(self, parent, root):
        super().__init__(parent)
        label = tk.Label(self, text="主功能畫面", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="下載工具", command=lambda: root.show_frame(PageOne))#lambda運算式
        button2 = ttk.Button(self, text="旅遊推薦區", command=lambda: root.show_frame(PageTwo)).pack(pady=5)
        button3 = ttk.Button(self, text="各類天氣查詢", command=lambda: root.show_frame(PageThree)).pack(pady=5)
        button4 = ttk.Button(self, text="結束", command=lambda: root.end())
        button4.pack(pady=20,padx=20,side='bottom',anchor='se')#布局在下方
        button1.pack(pady=5)
        #label+img
        bm = PhotoImage(file = '1200px-ROC_Central_Weather_Bureau_svg.png')
        label2 = tk.Label(self,image = bm,fg = 'blue', bg = 'red',font=40,text='資料皆來自中央氣象局CWB', width = 600, height = 500,compound = 'center')
        label2.bm = bm
        label2.pack(pady=20,padx=20,side='bottom')


class PageOne(tk.Frame):
    def __init__(self, parent, root):
        super().__init__(parent)
        label = tk.Label(self, text="下載工具", font=LARGE_FONT)
        label.pack(pady=10,padx=10) 
        
        button1 = ttk.Button(self, text="回到主頁面", command=lambda: root.show_frame(StartPage)).pack()
        button2 = ttk.Button(self, text="旅遊推薦", command=lambda: root.show_frame(PageTwo)).pack()
        button4 = ttk.Button(self, text="結束", command=lambda: root.end())
        button4.pack(pady=20,padx=20,side='bottom',anchor='se')#擺放
        ch=ttk.Label(self, text="施工中，請見諒:",
        font=('Arial', 30))
        ch.pack(padx=5) 
        #label+img
        bm = PhotoImage(file = 'warning.png')
        label2 = tk.Label(self,image = bm,width = 300, height = 200)
        label2.bm = bm
        label2.pack()
        #label3 = Label(self, fg = 'blue', bg = 'red',width = 30, height = 12, text = "color").pack()
        
        
        
        
        
        
        

class PageTwo(tk.Frame):
    def __init__(self, parent, root):
        super().__init__(parent)
        label = tk.Label(self, text="旅遊推薦", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="回到主頁面", command=lambda: root.show_frame(StartPage)).pack()
        button2 = ttk.Button(self, text="下載工具", command=lambda: root.show_frame(PageOne)).pack()
        button4 = ttk.Button(self, text="結束", command=lambda: root.end())
        button4.pack(pady=20,padx=20,side='bottom',anchor='se')#擺放
        #圖示
        mt = PhotoImage(file = 'mt.gif')
        label2 = tk.Label(self,image = mt,fg = 'blue',font=20, width = 150, height = 150,compound = 'center')
        label2.mt = mt
        label2.pack(padx=20,side='top',anchor='n')
        
        ch=ttk.Label(self, text="選擇模式:")     
        ch.pack(padx=5) 
        #下拉      
        model= tk.StringVar()
        numberChosen = ttk.Combobox(self, width=12, textvariable=model, state='readonly')#下拉1
        numberChosen.pack(padx=5,pady=5)
        numberChosen['values'] = ['全國推薦','地區旅遊日推薦']
        numberChosen.current()
        i=numberChosen.current()#下拉索引
        city_name = tk.StringVar()
        numberChosen2 = ttk.Combobox(self, width=12, textvariable=city_name, state='readonly')#下拉2
        numberChosen2['values'] = ("請先選擇模式")
        numberChosen2.current()
        def cmodel():#模式選擇
            i=numberChosen.current()
            if(i==0):
                model_cri.set("類別")
                numberChosen2['values'] = ("無需選擇")
            else:
                numberChosen2['values'] =city_n
                model_cri.set("選擇想要旅遊地區:")
        button_m = ttk.Button(self, text='確認', command=cmodel)
        button_m.pack(pady=5,padx=5)  
        model_cri = tk.StringVar()
        ch2=ttk.Label(self, textvariable=model_cri)
        model_cri.set("選擇想要旅遊地區:")
        ch2.pack(padx=5)  
        numberChosen2.pack(pady=10,padx=10)
        #cou=tables[3].values.tolist()#抓table
        global city_t
        city_t=[]
        def clickMe():
            i1=numberChosen.current()
            i2=numberChosen2.current()
            if(i1==0):
                text.delete(0.0, 'end')#清空
                text.insert(tk.INSERT,"明日推薦旅遊縣市(降雨率<30%):\n\n")
                for k in range(0,22):
                    search(k)
                    cc=r'[650].'
                    c=re.compile('[3-8]')#正規表示物件
                    rain=df_today.columns[4]
                    ok=df_today[df_today[rain].str.contains(c)]
                    print(ok)
                    if ok.empty:  
                        text.insert(tk.INSERT, city_n[k])
                        text.insert(tk.INSERT,", ")
                        city_t.append(city_n[k]+", ")
                        print(city_t)
            if(i1==1):
                i2=numberChosen2.current()#縣市索引
                text.delete(0.0, 'end')#清空
                text.insert(tk.INSERT, city_n[i2])
                text.insert(tk.INSERT," 推薦旅遊日(非下雨日):\n\n")
                search(i2)
                c=re.compile('[雨]')#正規表示物件
                rain=df.columns[1]
                temd="白"
                temn="晚"
                temp=[]
                for i in range(1,8):
                    temd=str(df.ix[1,i])
                    temm=str(df.ix[3,i])
                    if "雨"  in temd:
                        temp.append(i)
                    else:
                        if "雨"  in temn:
                            temp.append(i)
                df_rain=df.ix[:,temp]#做出未下雨的DF
                if df_rain.empty:
                    text.insert(tk.INSERT,"\n\n")
                    text.insert(tk.INSERT,"建議本周不要出遊比較好\n\n除非您喜好下雨天Σ(｀L_｀ ) ")
                else:
                    text.insert(tk.INSERT, list(df_rain))
                    text.insert(tk.INSERT,"\n\n")
                    for l in range(0,4):
                        text.insert(tk.INSERT, list(df_rain.ix[l]))
                        text.insert(tk.INSERT,"\n\n")
               

        button3 = ttk.Button(self, text='查詢', command=clickMe)
        text = tk.Text(self,font=25,width=500,height=100)
        text.insert(tk.INSERT, "資料顯示區\n")     
        button3.pack(pady=10,padx=10)
        text.pack(padx=5,pady=5)
        
            
class PageThree(tk.Frame):
    def __init__(self, parent, root):
        super().__init__(parent)
 

        tk.Label(self, text="查詢頁面", font=LARGE_FONT).pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="回到主頁面", command=lambda: root.show_frame(StartPage)).pack(pady=10)
        button4 = ttk.Button(self, text="結束", command=lambda: root.end())
        button4.pack(pady=20,padx=20,side='bottom',anchor='se')#擺放
        m1 = PhotoImage(file = 'm1.png')
        label2 = tk.Label(self,image = m1,fg = 'blue',font=20, width = 150, height = 150,compound = 'center')
        label2.m1 = m1
        label2.pack(padx=20,side='top',anchor='n')

        ttk.Label(self, text="查詢事項:").pack(padx=5,pady=10)
        number = tk.StringVar()
        numberChosen = ttk.Combobox(self, width=12, textvariable=number, state='readonly')
        numberChosen.pack(padx=5)
        numberChosen['values'] = ('今明預報','一週預報','月均溫','日月出沒')
        numberChosen.current(1)
        
        
        ttk.Label(self, text="選擇地區:").pack(padx=5)
        
        city_name = tk.StringVar()
        numberChosen2 = ttk.Combobox(self, width=12, textvariable=city_name, state='readonly')
        numberChosen2.pack(padx=5)
        #cou=tables[3].values.tolist()#抓table
        numberChosen2['values'] = city_n
        numberChosen2.current(1)
            
        #Treeview
        text = tk.Text(self,font=25,width=700,height=100)
        text.insert(tk.INSERT, "資料顯示區\n")
        #text.config(state=tk.DISABLED)
        
        
        def clickMe():
            global c,i
            c=numberChosen.current()#下拉索引
            if(c==0):#今明預報
                text.delete(0.0, 'end')#清空
                i=numberChosen2.current()#下拉索引
                search(i)
                text.insert(tk.INSERT,"\n")
                text.insert(tk.INSERT, list(df_today))
                text.insert(tk.INSERT,"\n\n")
                for l in range(0,3):
                    text.insert(tk.INSERT, list(df_today.ix[l]))
                    text.insert(tk.INSERT,"\n\n")
                #text.config(state=tk.DISABLED)#不開放編輯
                #save()
            if(c==1):#一周天氣
                text.delete(0.0, 'end')#清空
                #text.insert(tk.INSERT,city_name.get()+"test\n")
                i=numberChosen2.current()#下拉索引
                search(i)
                text.insert(tk.INSERT,"\n")
                #text.insert(tk.INSERT, city[0])
                text.insert(tk.INSERT, list(df))
                text.insert(tk.INSERT,"\n\n")
                for l in range(0,4):
                    text.insert(tk.INSERT, list(df.ix[l]))
                    text.insert(tk.INSERT,"\n\n")
            
            if(c==2):#月均溫
                text.delete(0.0, 'end')#清空
                i=numberChosen2.current()#下拉索引
                search(i)
                text.insert(tk.INSERT,"\n")
                text.insert(tk.INSERT, list(df_month))
                text.insert(tk.INSERT,"\n\n")
                text.insert(tk.INSERT, list(df_month.ix[0]))
            if(c==3):#日月出沒
                text.delete(0.0, 'end')#清空
                i=numberChosen2.current()#下拉索引
                search(i)
                text.insert(tk.INSERT,"\n")
                text.insert(tk.INSERT, list(df_raise))
                text.insert(tk.INSERT,"\n\n")
                text.insert(tk.INSERT, list(df_raise.ix[0]))
        def save():
            if(c==0):
                name=city_n[i]+"今明預報.xlsx"
                writer = ExcelWriter(name) #寫入新檔案
                df_today.to_excel(writer,'Sheet2')#指定工作表
                workbook = writer.book
                worksheet = writer.sheets['Sheet2']
                worksheet.conditional_format('A1:E90', {'type': '3_color_scale'}) #著色
                text.insert(tk.INSERT, "\n\n儲存成功 ")
                text.insert(tk.INSERT, name)
            if(c==1):
                name=city_n[i]+"一週預報.xlsx"
                writer = ExcelWriter(name) #寫入新檔案
                df.to_excel(writer,'Sheet2')#指定工作表
                workbook = writer.book
                worksheet = writer.sheets['Sheet2']
                worksheet.conditional_format('A1:E90', {'type': '3_color_scale'}) #著色
                text.insert(tk.INSERT, "\n\n儲存成功 ")
                text.insert(tk.INSERT, name)
            if(c==2):
                name=city_n[i]+"月均溫.xlsx"
                writer = ExcelWriter(name) #寫入新檔案
                df_month.to_excel(writer,'Sheet2')#指定工作表
                workbook = writer.book
                worksheet = writer.sheets['Sheet2']
                worksheet.conditional_format('A1:E90', {'type': '3_color_scale'}) #著色
                text.insert(tk.INSERT, "\n\n儲存成功 ")
                text.insert(tk.INSERT, name)
            if(c==3):
                name=city_n[i]+"日月出沒.xlsx"
                writer = ExcelWriter(name) #寫入新檔案
                df_raise.to_excel(writer,'Sheet2')#指定工作表
                workbook = writer.book
                worksheet = writer.sheets['Sheet2']
                worksheet.conditional_format('A1:E90', {'type': '3_color_scale'}) #著色
                text.insert(tk.INSERT, "\n\n儲存成功 ")
                text.insert(tk.INSERT, name)
            
        
        button2 = ttk.Button(self, text='查詢', command=clickMe).pack(pady=10,padx=10)
        button_m = ttk.Button(self, text='儲存', command=save)
        button_m.pack(pady=5,padx=5,side='bottom')  
        text.pack(padx=5,pady=5)
        
        
        
    
       


#if __name__ == '__main__':
    # 实例化Application
ini()
app = Application()
    
    # 主消息循环:
    #app.geometry("500x800")
    
    
    
    
    
app.mainloop()