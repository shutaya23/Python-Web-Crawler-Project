# -*- coding: utf-8 -*-
"""
Created on Sat Mar 31 18:36:05 2018

@author: User
"""
import requests,re
import tkinter as tk
 
def end():#結束視窗
    global win
    win.destroy() 
    
def search():#查榜
    url = 'https://www.caac.ccu.edu.tw/CacLink/apply107/107apply_Sieve_pg58e3q/html_sieve_107yaya/ColPost/common/apply/' 
    name=['師大','政大','中央']
    school=['002212','006372','016202']
    global win,text1
    a=num.get()
    count=int(0)
    data.set("U0424041")
    text1.insert(tk.INSERT,"searching..."+a+"\n") #印在text上
    regex=re.compile('[0-9]{8}$') # 連續8位數字(準考證號碼)結束
    e=regex.match(a)#檢查有效
    if(e):
        for i in range(0,3):
            strr= a+name[i]+"APCS組"
            nurl=url+school[i]+'.htm'
            html = requests.get(nurl)#帶入網頁
            if a in html.text:
                count+=1
                strr= a+"錄取:"+name[i]+"APCS組\n"
                text1.insert(tk.INSERT, strr)    
        if(count>0):
            strr= "共錄取"+str(count)+"間學校\n"
            text1.insert(tk.INSERT,strr)
    else:
        text1.insert(tk.INSERT, "非准考證號碼\n")    

win = tk.Tk()
#text = tk.Text(win)
num = tk.StringVar()
data=tk.StringVar()

win.geometry("450x500")
win.title("申請入學資工APCS組查榜")

frame1 = tk.Frame(win)#視窗win上的區塊1
frame1.pack()#簡易排版
label1=tk.Label(frame1,text="轉考證查榜：", padx=20, pady=10)
entry = tk.Entry(frame1, textvariable=num)#輸入的內容變數為num
label1.grid(row=0, column=0)#Gridview排版
entry.grid(row=0, column=1)

frame2 = tk.Frame(win)
frame2.pack()
button1 = tk.Button(frame2, text="開始查詢",command=search)
button2 = tk.Button(frame2, text="結束",command=end)#按下執行command
label2=tk.Label(frame2,text="",textvariable=data)
button1.grid(row=0, column=0)
button2.grid(row=0, column=1)
label2.grid(row=1, column=0)

frame3 = tk.Frame(win)
text1=tk.Text(frame3)#本文
text1.grid(row=0, column=0)
frame3.pack()

#text.config(state=tk.DISABLED)
win.mainloop()

