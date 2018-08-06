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
    dic['sticker']=input('sticker')
    if dic['sticker']=='':
        dic['sticker']=None
    dic['photo']=input('photo')
    if dic['photo']=='':
        dic['photo']=None
    dic['video']=input('video')
    if dic['video']=='':
        dic['video']=None
    dic['allco']=bool(input('allco(type anything for True,empty for False'))
    print(json.dumps(dic))
    