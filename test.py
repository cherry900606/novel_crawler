import requests
from bs4 import BeautifulSoup

#todo:
# 1) 使用者輸入 (done)
# 2) 簡介
# 3) 函式包裝
# 4) 從首頁進入 (done)
# 5) 整理好看點

#網頁網址
index_page=input("請輸入欲下載小說的網址: ")
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
    #print(context)

    file.write(chapter_name+'\n')
    file.write(context+'\n\n')

    #下一章
    next_chapter=book.find('div',class_='bottem1')
    next_chapter=next_chapter.find_all('a')
    next_chapter_link=home_page+next_chapter[3]['href']
    #print(next_chapter_link)
    current_page=next_chapter_link

file.close()
print("下載結束")