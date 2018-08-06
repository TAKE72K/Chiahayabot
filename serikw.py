#coding=utf-8
import json
i=True
while i==True:
    dic={}
    key_words=[]
    kwi=False
    while kwi!=True:
        a=input('key_word')
        if a=='exit':
            kwi=True
        else:
            key_words.append(a)
    dic['key_words']=key_words
    dic['echo']=input('echo')
    dic['els']=input('els')
    if dic['els']=='':
        dic['els']=None
    try:
        dic['prob']=int(input('prob'))
    except:
        dic['prob']=100
    
    dic['allco']=bool(input('allco(type anything for True,empty for False'))
    print(json.dumps(dic))
    