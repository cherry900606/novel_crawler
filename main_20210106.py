import requests
from bs4 import BeautifulSoup
import tkinter as tk
import tkinter.messagebox


def download(window):
    index_page=url_entry.get()

    #網頁網址
    #index_page=input("請輸入欲下載小說的網址: ")
    home_page='https://www.shubaow.net'


    #目錄頁
    response = requests.get(index_page)
    response.encoding='gbk'
    soup=BeautifulSoup(response.text,"html.parser")

    index_list=soup.select('#list')[0]
    item=index_list.find_all('dd')
    for i in item:
        if i.text.find("第1章")!=-1:
            current_page=home_page+i.find('a')['href']
            break

    response = requests.get(current_page)
    response.encoding='gbk'
    soup=BeautifulSoup(response.text,"html.parser")

    book=soup.find('div',{'class':'bookname'}) # or book=soup.find('div',class_='bookname')
    index_page=book.find('div',class_='bottem1')
    index_page=index_page.find_all('a')[2]['href']

    #書名
    page=soup.find('div',class_='con_top')
    bookname=page.find_all('a')[2].text
    print(bookname+"下載中......")

    #輸出書名
    file=open(bookname+'.txt','w',encoding='utf-8')
    file.write("書名: "+bookname+'\n')



    while current_page!=index_page:
        response = requests.get(current_page)
        response.encoding='gbk'
        soup=BeautifulSoup(response.text,"html.parser")
        book=soup.find('div',{'class':'bookname'}) # or book=soup.find('div',class_='bookname')

        
        #章節名
        chapter=book.find('h1')
        chapter_name=chapter.text.lstrip()
        print(chapter_name)

        #內文
        context=soup.select('#content')[0].text

        file.write(chapter_name+'\n')
        file.write(context+'\n\n')

        #下一章
        next_chapter=book.find('div',class_='bottem1')
        next_chapter=next_chapter.find_all('a')
        next_chapter_link=home_page+next_chapter[3]['href']
        current_page=next_chapter_link

    file.close()
    print("下載結束")
    tk.messagebox.showinfo("提示","下載結束")
    window.destroy()
    


window=tk.Tk()
window.title("小說下載器")
window.geometry('800x600')
window.configure(background='white')

name_label=tk.Label(window,text='小說下載器')
name_label.pack()
notion_label=tk.Label(window,text='溫馨小提醒: 請輸入「書包網」的小說「目錄頁」網址！')
notion_label.pack()

url_frame=tk.Frame(window)
url_frame.pack(side=tk.TOP)

url_label=tk.Label(url_frame,text="網址: ")
url_label.pack(side=tk.LEFT)

url=tk.StringVar()
url_entry=tk.Entry(url_frame,textvariable=url)
url_entry.pack(side=tk.LEFT)

trigger_btn=tk.Button(window,text="下載",command=lambda:download(window))
trigger_btn.pack()

window.mainloop()
