#coding=utf-8
import requests
import json
from random import randrange
import os
import psycopg2
from psycopg2 import sql

DATABASE_URL = os.environ['DATABASE_URL']
eventing=os.environ['EVing']
eventId=os.environ['EVENT_ID']

conn = psycopg2.connect(DATABASE_URL, sslmode='require')
curs=conn.cursor()
END_POINT='https://api.matsurihi.me/mltd/v1/'

card_pool=[]
card_num={4:0,3:0,2:0}
def refresh_pool():
    global card_pool
    global card_num
    temp_pool=[]
    q1="""SELECT detail FROM card where detail->>'rarity' = '%s' and detail->>'extraType'<>'5' and detail->>'extraType'<>'6'
    ORDER BY RANDOM() LIMIT %s """
    #pick 3 ssr
    def setpool(rare,num):
        try:
            curs.execute(q1,(rare,num))
        except:
            return
        else:
            card_pick=curs.fetchall()
            for i in card_pick:
                temp_pool.append(i[0])
            card_num[rare]=num
    setpool(4,3)
    setpool(3,12)
    setpool(2,85)
    card_pool=temp_pool

def update_card():
    api=requests.get(END_POINT+'cards').json()
    q1="""
    select id,detail 
    from card 
    order by id desc;
    """
    curs.execute(q1)
    dbdata=curs.fetchall()
    if len(api)>len(dbdata):
        insertstart=0
        match_last=False
        iter=len(api)-1
        while match_last!=True:
            if api[iter]['id']==dbdata[0][1]['id']:
                insertstart=iter+1
                match_last=True
            else:
                iter=iter-1
        q2="""
        insert into card(detail) values(%s)
        """
        for i in range(insertstart,len(api)):
            ins=json.dumps(api[i], ensure_ascii=False)
            try:
                curs.execute(q2,[ins])
            except:
                print('error')
            else:
                conn.commit()
                print('update success'+api[i]['name'])
    else:
        print('nothing new')
                
def gasya():
    global card_pool
    global card_num
    
    if card_num[4]<3:
        refresh_pool()
    result=card_pool[randrange(len(card_pool))]
    card_pool.remove(result)
    card_num[result['rarity']]=card_num[result['rarity']]-1
    return result

def event_score():
    q1="events/{}/rankings/logs/eventPoint/{}"
    q2="events/{}".format(eventId)
    event_name=requests.get(END_POINT+q2).json()['name']
    border_info={'name':event_name}
    def border(rank):
        api=requests.get(END_POINT+q1.format(eventId,rank)).json()[0]['data']
        now=api[len(api)-1]['score']
        past_2='--'
        if len(api)>2:
            past_2=api[len(api)-4]['score']
        return {'rank':rank,'now':now,'past_2':past_2}
    border_info[100]=border(100)
    border_info[2500]=border(2500)
    border_info[5000]=border(5000)
    border_info[10000]=border(10000)
    border_info[25000]=border(25000)
    return border_info

    
        
        