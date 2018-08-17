#coding=utf-8
import requests
import json
from random import randrange
import os
import psycopg2
from psycopg2 import sql

DATABASE_URL = os.environ['DATABASE_URL']

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
     
def gasya():
    global card_pool
    global card_num
    
    if card_num[4]<3:
        refresh_pool()
    result=card_pool[randrange(len(card_pool))]
    card_pool.remove(result)
    card_num[result['rarity']]=card_num[result['rarity']]-1
    return result
