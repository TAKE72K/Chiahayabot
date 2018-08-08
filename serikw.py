#coding=utf-8
import json
i=True



while i==True:
    text_file = open("Output.txt", "a")
    dic={}
    key_words=[]
    kwi=False
    while kwi!=True:
        a=input('key_word')
        if a=='exit':
            kwi=True
        elif a=='':
            pass
        else:
            key_words.append(a)
    dic['key_words']=key_words
    dic['echo']=input('echo')
    if dic['echo']=='':
        dic['echo']=None
    dic['els']=input('els')
    if dic['els']=='':
        dic['els']=None
    try:
        dic['prob']=int(input('prob'))
    except:
        dic['prob']=1000


    sti=False
    stic=[]
    while sti!=True:
        s=input('sticker')
        if s=='':
            sti=True
        else:
            stic.append(s)
    if bool(stic):
        dic['sticker']=stic
    else:
        dic['sticker']=None
    dic['photo']=input('photo')
    if dic['photo']=='':
        dic['photo']=None
    dic['video']=input('video')
    if dic['video']=='':
        dic['video']=None
    dic['allco']=bool(input('allco(type anything for True,empty for False'))
    print(json.dumps(dic))
    s= json.dumps(dic)+'\n'
    text_file.write(s)
    text_file.close()
    