import requests
import re
import os
from bs4 import BeautifulSoup
from selenium import webdriver
'''
chrome_exec_shim = os.environ.get("GOOGLE_CHROME_BIN", "chromedriver")'''
#self.selenium = webdriver.Chrome(executable_path=chrome_exec_shim)
def tohanear(con,pos):
    ntohaPos=con.find('とは')
    if ntohaPos==-1:
        ntohaPos=con.find('は')
    compare=1000
    nearT=None
    for i in pos:
        if abs(i-ntohaPos)<compare:
            compare=abs(i-ntohaPos)
            nearT=i
    if con.find('「'):
        nearT=con.find('「')
    return nearT
def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext
exist_url='http://api.nicodic.jp/page.exist/json/a/'
nicoDic='http://dic.nicovideo.jp/a/'
def summary(words):
#words=input()
#first check if the page exist with API
    exist=requests.get(exist_url+words)
    exist=exist.json()
    if exist: 
    #get html code by selenium
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        driver = webdriver.Chrome(executable_path='/app/.apt/usr/bin/google-chrome',chrome_options=options)
        driver.get(nicoDic+words)
        html = driver.page_source # get html
        driver.close()  # close driver
        soup=BeautifulSoup(html,features="html.parser")
        title=soup.title.string
        tohaPos=title.find('とは')
        title=title[:tohaPos]
        print(title)
        divPos=html.find('<div class="article" id="article">')
        h2Pos=html.find('<h2')
        content=html[divPos:h2Pos]
        #print (content)
        summaryPos=[h.start() for h in re.finditer(title, content)]
        content=content[tohanear(content,summaryPos):]
        content=cleanhtml(content)
        if content.find('\n\n')!=-1:
            content=content[:content.find('\n\n')]
        return cleanhtml(content)
    
    return None

