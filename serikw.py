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
        if a=='':
            kwi=True
        
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
        
    sti=False
    stic=[]
    while sti!=True:
        s=input('photo')
        if s=='':
            sti=True
        else:
            stic.append(s)
    if bool(stic):
        dic['photo']=stic
    else:
        dic['photo']=None
    
    
    sti=False
    stic=[]
    while sti!=True:
        s=input('video')
        if s=='':
            sti=True
        else:
            stic.append(s)
    if bool(stic):
        dic['video']=stic
    else:
        dic['video']=None

    sti=False 
    stic=[]
    while sti!=True:
        s=input('passArg')
        if s=='':
            sti=True
        else:
            stic.append(s)
    if bool(stic):
        dic['passArg']=stic
    else:
        dic['passArg']=None
    dic['allco']=bool(input('allco(type anything for True,empty for False'))
    
    
    print(json.dumps(dic))
    s= json.dumps(dic, ensure_ascii=False)
    text_file.write(s)
    text_file.close()
    