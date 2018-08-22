import telegram
import re
import random
from random import randrange
import os
import sys
from telegram.utils.request import Request
import telegram.bot
from telegram.ext import messagequeue as mq
from threading import Thread
import logging
import time
import json
import datetime as dt
from datetime import datetime, tzinfo, timedelta
from datetime import time as stime
from telegram import InlineQueryResultArticle, InputTextMessageContent,InlineKeyboardMarkup,InlineKeyboardButton
from telegram.ext import Updater,CommandHandler,MessageHandler,Filters,InlineQueryHandler,JobQueue
from telegram.ext.dispatcher import run_async
import python3pickledb as pickledb
from key_word import key_word as kws
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests
from himeAPI import gasya,update_card,event_score
#db
import psycopg2
from psycopg2 import sql

DATABASE_URL = os.environ['DATABASE_URL']
eventing=os.environ['EVing']


conn = psycopg2.connect(DATABASE_URL, sslmode='require')
#db
debug_mode=False

curs=conn.cursor()

if debug_mode is False:
    token = os.environ['TELEGRAM_TOKEN']
    js=os.environ['JSON']
    spreadsheet_key=os.environ['SPREAD']
    # token will taken by heroku
'''not sure if need to import'''
#遊戲部ID:-1001232423456
'''
command list
start-名為72的偶像
help-72能做什麼?
time-現在幾點
gdmn-早安
set-set早安名
kenka-吵架
grave-擔當太尊而猝死的P用
quote-千早歌詞集
bomb-自爆吧P
count-test function count members
dice-N粒公正的骰子(N<1000)
gasya-一抽入魂
sticker-アイマス鯖STICKERまとめ
water-即時水量
about-關於此bot
'''

#tool func

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)

logger = logging.getLogger(__name__)

def get_cell(key_word,worksheet):
    try:
        cell=worksheet.find(key_word)
    except:#not find
        return None
    else:
        return cell

def build_menu(buttons,
               n_cols,
               header_buttons=None,
               footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu

def strfdelta(tdelta, fmt):
    d = {"days": tdelta.days}
    d["hours"], rem = divmod(tdelta.seconds, 3600)
    d["minutes"], d["seconds"] = divmod(rem, 60)
    return fmt.format(**d)
def del_cmd(bot,update):
    """Dectect bot if admin, if True, del cmd"""
    if bot_is_admin(bot,update):
        try:
            bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)
        except:
            pass
def bot_is_admin(bot,update):
    """Dectect bot if admin, return boolen value"""
    bot_auth=False
    if update.message.chat.type=='private':
        return bot_auth
    else:
        adminlist=update.message.chat.get_administrators()
        me=bot.get_me()
        for b in adminlist:
                if me.id==b.user.id:
                    bot_auth=True
        return bot_auth   
    
def set_config(id,command):
    scope = ['https://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_name('auth.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(spreadsheet_key)
    worksheet=sheet.worksheet('config')
    user_id=id
    try:
        #find chat_id
        cell=worksheet.find(str(user_id))
    except:
        #ERROR:not found
        #creat new record
        worksheet.insert_row([user_id,command], 1)
    else:
        #replace record
        setting=worksheet.cell(cell.row,cell.col+1).value
        if setting.find(command)!=-1:
            setting=setting.replace(command,'')
        else:
            setting=setting+command
        worksheet.update_cell(cell.row,cell.col+1,setting)
def dbsave(table,data,col):
    q1 = sql.SQL("insert into {} ({}) values ({})").format(sql.Identifier(table),sql.SQL(', ').join(map(sql.Identifier, col)),sql.SQL(', ').join(sql.Placeholder() * len(col)))
    
    
    try:
        curs.execute(q1,data)
        #curs.execute("INSERT INTO randchihaya(name,url) VALUES(%s,%s)",(data[0],data[1]))
    except:
        print('???')
        conn.rollback()
    else:
        conn.commit()
def dbget(table,col):
    q1=sql.SQL("SELECT {} FROM {} ORDER BY ID").format(sql.Identifier(col),sql.Identifier(table))
    try:
        curs.execute(q1)
    except:
        conn.rollback()
    else:
        data=curs.fetchall()
        return data
def dbrandGet(table,col):
    q1=sql.SQL("SELECT {} FROM {} ORDER BY RANDOM() LIMIT 1").format(sql.Identifier(col),sql.Identifier(table))
    str=''
    try:
        curs.execute(q1)
        #curs.execute("""SELECT url FROM randchihaya
        #                ORDER BY RANDOM()
        #               LIMIT 1""")
    except:
        conn.rollback()
    else:
        str=curs.fetchone()[0]
    return str
    
def get_config(id,setting):
    scope = ['https://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_name('auth.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(spreadsheet_key)
    worksheet=sheet.worksheet('config')
    user_id=id
    try:
        #find chat_id
        cell=worksheet.find(str(user_id))
    except:
        return False
    else:
        config=worksheet.cell(cell.row,cell.col+1).value
        if config.find(setting)!=-1:
            return True
        else:
            return False
def dbupdate(bot,job):
    update_card()
def daily_reset(bot,job):
    scope = ['https://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_name('auth.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(spreadsheet_key)
    user_config=sheet.worksheet('config').get_all_values()
    for i in user_config:
        if i[1].find('q') != -1:
            set_config(i[0],'q')
            
HALF2FULL = dict((i, i + 0xFEE0) for i in range(0x21, 0x7F))
HALF2FULL[0x20] = 0x3000
def fullen(s):
    '''
    Convert all ASCII characters to the full-width counterpart.
    '''
    text=s

    text=str(text).translate(HALF2FULL)
    return text
    
class GMT8(tzinfo):
    def utcoffset(self, dt):
        return timedelta(hours=8)
    def dst(self, dt):
        return timedelta(0)
    def tzname(self,dt):
        return "TAIWAN"
def work_sheet_push(values,worksheet_name):
    scope = ['https://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_name('auth.json', scope)
    #got from google api
    #attach mine for example
    #try to set in environ values but got fail
    client = gspread.authorize(creds)
    spreadsheet = client.open_by_key(spreadsheet_key)
    try:
        worksheet=spreadsheet.worksheet(worksheet_name)
    except:#there is no this worksheet
        spreadsheet.add_worksheet(worksheet_name,len(values),1)
        worksheet=spreadsheet.worksheet(worksheet_name)
        worksheet.insert_row(values,1)
    else:
        worksheet.insert_row(values,1)
#usage (values[list of string],worksheet_name[string])
#put a list of value and push to worksheet

def work_sheet_fpop(key,woksheet_name):
    scope = ['https://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_name('auth.json', scope)
    #got from google api
    #attach mine for example
    #try to set in environ values but got fail
    client = gspread.authorize(creds)
    spreadsheet = client.open_by_key(spreadsheet_key)
    worksheet=spreadsheet.worksheet(worksheet_name)
    cell=get_cell(key,worksheet)
    if cell!=None:
        row=worksheet.row_values(cell.row)
        worksheet.delete_row(cell.row)
    else:
        return None     

def work_sheet_pop(worksheet_name):
    scope = ['https://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_name('auth.json', scope)
    #got from google api
    #attach mine for example
    #try to set in environ values but got fail
    client = gspread.authorize(creds)
    spreadsheet = client.open_by_key(spreadsheet_key)
    worksheet=spreadsheet.worksheet(worksheet_name)
    try:
        cell=worksheet(1,1)
    except:
        return None
    else:
        row=[]
        for k in range(1,worksheet.col_count+1):
            row.append(worksheet(1,k))
        worksheet.delete_row(1)
        return row
        
def get_sheet(name):
    scope = ['https://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_name('auth.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(spreadsheet_key)
    try:
        worksheet=sheet.worksheet(name)
    except:
        return None
    else:
        return worksheet
#tool func
'''
daily_remind=updater.job_queue
def callback11(bot,job):
    bot.send_message(chat_id='580276512',text='想下班')
t = time(17, 30, 30, tzinfo=GMT8())
job_m=daily_remind.run_daily(callback11,t)
'''
#unsolve:TypeError: can't compare offset-naive and offset-aware times


def start(bot, update,args):
    payload=' '.join(args)
    if payload=='sticker':
        sticker_matome(bot,update)
        return
        
    
        
    bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
    bot.send_message(chat_id=update.message.chat_id, text="如月千早です。劇場という場所があることは、レッスンの励みにもなりますね。これからも、厳しいご指導をよろしくお願いします。")
    bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
    #bot.send_message(chat_id=update.message.chat_id, text='私のコマンドリストです：\n/start-名為72的偶像\n/help-72能做什麼?\n/time-現在幾點\n/gdmn-早安\n/set-set早安名\n/kenka-吵架\n/grave-擔當太尊而猝死的P用\n/quote-千早歌詞集\n/bomb-自爆吧P\n/count-test function count members\n/dice-N粒公正的骰子(N<1000)\n/water-即時水量\n/about-關於此bot')
    bot.send_message(chat_id=update.message.chat_id, text="気軽にお声をおかけください～～　/help")
    button_list=[
        InlineKeyboardButton(text='start me in PM',url='https://telegram.me/Chiahayabot?start=hello'),
        InlineKeyboardButton(text='about Chihaya.K',url='https://imasml-theater-wiki.gamerch.com/%E5%A6%82%E6%9C%88%E5%8D%83%E6%97%A9#content_2_13')
        ]
    
    reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=1))
    bot.send_message(chat_id=update.message.chat_id, text="button da!", reply_markup=reply_markup)
    '''test of inline button'''

def help(bot,update):
    bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
    bot.send_message(chat_id=update.message.chat_id, text="""
    私のコマンドリストです：
/start-名為72的偶像
/help-72能做什麼?
/time-現在幾點
/gdmn-早安
/set-set早安名
/kenka-吵架
/grave-擔當太尊而猝死的P用
/quote-千早歌詞集
/bomb-自爆吧P
/count-test function count members
/dice-N粒公正的骰子(N<1000)
/gasya-一抽入魂
/sticker-アイマス鯖STICKERまとめ
/water-即時水量
/about-關於此bot
    """)

def about(bot,update):
    text_a='''
本機器人由一個支離滅裂的千早P製作 code也很支離滅裂
BUG什麼的還請多多回報 多多包涵

至於BOT的名字 相信大家都注意到了
是Chiahayabot喲(Chiayi+Chihaya=Chiahaya)
坐車經過嘉義時想到的

        【Chiahayabot】
    releases v.87
    有事請找<a href="https://t.me/joinchat/IFtWTxKu7x6vuSK8HsFgsQ">〔765技術部〕</a>
    '''
    bot.send_message(chat_id=update.message.chat_id,text=text_a,parse_mode='HTML')
def set_kw(bot,update,args):
    text=' '.join(args)
    text=text.split(';')
    kws={'word':text[0],'echo':text[1],'prog':text[2],'els':text[3],'photo':text[4],'video':text[5],'allco':text[6]}
    s=json.dumps(kws)
    work_sheet_push([s],'key_word')

def state(bot,update):
    #Date:   Thu Jul 19 09:07:15 2018 +0800
    start_oper=datetime(year=2018,month=7,day=19,hour=1,minute=7,second=15)
    oper_time=datetime.now()-start_oper
    text=strfdelta(oper_time, "本BOT已運行{days}天{hours}小時又{minutes}分")
    scope = ['https://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_name('auth.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(spreadsheet_key)
    qsheet=sheet.worksheet('quote')
    num=qsheet.row_count
    text=text+'\n名言共有'+str(num)+'句'
    bot.send_message(chat_id=update.message.chat_id,text=text)
    


def invite(bot,update):
#generate unvite link
    bot.send_message(chat_id=update.message.chat_id, text='加入阿克西斯教，just now')
    bot.export_chat_invite_link(chat_id=update.message.chat_id)

def title(bot,update,args):
#change group title
    title = ' '.join(args)
    adminlist=update.message.chat.get_administrators()
    is_admin=False
    
    me=bot.get_me()
    bot_auth=False
    for i in adminlist:
        if update.message.from_user.id==i.user.id:
            is_admin=True
    for b in adminlist:
            if me.id==b.user.id:
                bot_auth=True
    if is_admin==True:
        if bot_auth==True:
            bot.set_chat_title(chat_id=update.message.chat_id, title=title)
            bot.send_message(chat_id=update.message.chat_id,text='title changed')
        else:
            bot.send_message(chat_id=update.message.chat_id,text='Bot:Not enough rights to change chat title')
    else:
        test='list:your id'+str(update.message.from_user.id)+'\n'+'admin id:'
        for i in adminlist:
            test=test+str(i.user.id)+'\n'
        bot.send_message(chat_id=update.message.chat_id,text=test)
        bot.send_message(chat_id=update.message.chat_id,text='User:Not enough rights to change chat title')
        if bot_auth==True:
            
            bot.send_message(chat_id=update.message.chat_id,text='Bot:Auth comfirm')
        else:
            bot.send_message(chat_id=update.message.chat_id,text='Bot:Not enough rights to change chat title')

def set_name(bot,update,args):
    scope = ['https://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_name('auth.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(spreadsheet_key)
    if not args:
        bot.send_message(chat_id=update.message.chat_id,text='input emep')
        return
    else:
        name=' '.join(args)
        nsheet=sheet.worksheet('name')
        try:
            cell=nsheet.find(str(update.message.from_user.id))
        except:#not found
            nsheet.insert_row([update.message.from_user.id,name], 2)
            #bot.send_message(chat_id=update.message.chat_id,text='Bot:Not enough rights to change chat title')
        else:
            nsheet.update_cell(cell.row,cell.col+1,name)
def randchihaya(bot,update):
    url=dbrandGet('randchihaya','url')
    bot.send_photo(chat_id=update.message.chat_id,photo=url)
def randtsumugi(bot,update):
    url=dbrandGet('randtsumugi','url')
    bot.send_photo(chat_id=update.message.chat_id,photo=url)
def gdmn(bot,update):
    #a good morning func
    scope = ['https://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_name('auth.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(spreadsheet_key)
    bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)#type effect

    text=" $username P、おはようございます。今日も一日頑張るぞい"
    #aoba kawaii na--
    
    message=update.message
    chat_id = message.chat.id
    bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
    nsheet=sheet.worksheet('name')
    #replace $username
    try:
        cellid=nsheet.find(str(update.message.from_user.id))
    except:
        name=None
    else:
        name=nsheet.cell(cellid.row,cellid.col+1).value
    #name=ndb.get(str(update.message.from_user.id))
    if name==None:
        text=text.replace("$username",str(update.message.from_user.first_name))
    else:
        text=text.replace("$username",name)
    
    #bot.send_photo(chat_id,photo='AgADBQADSagxG3VSeVaStO9CCRE_trYo1TIABKGMGsglQ3cr9BoCAAEC')
    #doc:photo=a filelike object ,suggest to be replace with file_id
    
    bot.send_message(chat_id=update.message.chat_id,text=text)
    
    #custom_keyboard = [['/start', '/gdmn'], ['72', '找飯店'],['そらそら']]
    
    #reply_markup = telegram.ReplyKeyboardMarkup(keyboard=custom_keyboard,one_time_keyboard=True)#one_time_kb:initial false ,dissapear after touch once
    
    #bot.send_message(chat_id=chat_id, text="KeyBoard test~~", reply_markup=reply_markup)

def count(bot,update):
    time = datetime.now().strftime("%H:%M:%S")
    time='現在時間:'+time
    count=bot.get_chat_members_count(chat_id=update.message.chat.id)
    text='室內人數'+str(count)+'\n'+time
    bot.send_message(chat_id=update.message.chat_id,text=text)
    
def bomb(bot,update,args):
    text=('≡=- -=≡≡≡=- =＝≡\n'
    '　　 ノ⌒⌒⌒ヽ\n'
    '　 (( ⌒ ⌒ ヾ ))\n'
    '　(( 　⌒　⌒　 ))\n'
    '=- `(（　　　）)ノ-=\n'
    '≡＝ヽヽ|　|ノノ＝=≡\n'
    '　 ノ⌒~|i |~⌒ヽ\n'
    '嚇( (~⌒|| |⌒~) )=噐\n'
    '噐ヽ ﾞ～⌒～⌒″ノ=咫\n'
    '咫=-ﾞー～―～ー″-=哥\n'
    '哥-　　 ||||　　 -歌A\n'
    'A咀=-　ノ从ヽ　 -=F味\n'
    'FH品=--　　　--==E唄H\n'
    'H呈幵Fﾛ==---==呵且F品\n')
    if not args:
        ta='剛才聽到如月千早唱的歌'
    else:
        ta='剛才$event'
        ta=ta.replace('$event',''.join(args))
    tb='熱情奔放、創意無限、燃點起我$username心中的一團火'
    tc='我$username感覺到，在這個時刻，要爆了。'
    tb=tb.replace('$username',update.message.from_user.first_name)
    tc=tc.replace('$username',update.message.from_user.first_name)
    bot.send_message(chat_id=update.message.chat_id,text=ta)
    bot.send_message(chat_id=update.message.chat_id,text=tb)
    bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
    bot.send_message(chat_id=update.message.chat_id,text=tc)
    bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
    bot.send_message(chat_id=update.message.chat_id,text=text)

def splen(seq, length):
    return [seq[i:i+length] for i in range(0, len(seq), length)]
def grave(bot,update):
    par=random.randint(0,1)
    if par==0:
        text=('　　　／￣￣〈￣￣＼ :.＼ \n'
            '　　 |　　　　　　　　|: ::| \n'
            '　 　|　$pname|: ::| \n'
            '　 　|　$s2|: ::| \n'
            '　 　|　$s3|: ::| \n'
            '　 　|　　　　　　　　|: ::| \n'
            '　 　|　　安息於此　　|: ::| \n'
            '　 　|　　　　　　　　|: ::| \n'
            '￣\"￣\"￣\'￣￣\"\"￣\"\"￣.￣\'￣￣\n '
            )
        pname=update.message.from_user.first_name
        pname=fullen(pname)
        op=pname
        l=len(pname)
        if len(pname)<7:
            
            for l in range(l,7):
                op+='　'
            text=text.replace('$pname',op)
            text=text.replace('$s2','　　　　　　　')
            text=text.replace('$s3','　　　　　　　')
        if len(pname)==7:
            text=text.replace('$pname',op)
            text=text.replace('$s2','　　　　　　　')
            text=text.replace('$s3','　　　　　　　')
        if len(pname)>7:
            plist=splen(pname,7)
            if l>7 and l<15:
                l2=len(plist[1])
                for l2 in range(l2,7):
                    plist[1]+='　'
                text=text.replace('$pname',plist[0])
                text=text.replace('$s2',plist[1])
                text=text.replace('$s3','　　　　　　　')
            if l>14:
                l2=len(plist[1])
                
                l3=len(plist[2])
                for l3 in range(l3,7):
                    plist[2]+='　'
                text=text.replace('$pname',plist[0])
                text=text.replace('$s2',plist[1])
                text=text.replace('$s3',plist[2])
        bot.send_message(chat_id=update.message.chat_id,text=text)
    if par>0:
        top='　　 ＿ \n'
        nak='　　|$name| \n'
        bas=('　|￣￣￣| \n'
            '　| |三三| | \n'
            '￣￣￣￣￣￣ \n')
        op=top
        pname=update.message.from_user.first_name
        pname=fullen(pname)
        l=len(pname)
        
        for a in range(0,l):
            
            t=nak.replace('$name',pname[a])
            op+=t
        op+=bas
        bot.send_message(chat_id=update.message.chat_id,text=op)

def restart(bot, update):
    update.message.reply_text('Bot is restarting...')
    Thread(target=stop_and_restart).start()

@run_async
def history(bot,job):
    chat_id=-1001232423456
    
    time = datetime.now().strftime("%y/%m/%d %H:%M:%S")
    
    scope = ['https://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_name('auth.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(spreadsheet_key)
    worksheet=sheet.worksheet('last_message')
    
    c=get_cell(str(chat_id),worksheet)
    message_id=worksheet.cell(c.row,c.col+1).value
    count=bot.get_chat_members_count(chat_id)
    list=[str(chat_id),time,message_id,str(count)]
    work_sheet_push(list,'gr')
    
    worksheet=sheet.worksheet('gr')
    w=get_cell(str(chat_id),worksheet)
    water=int(worksheet.cell(w.row,w.col+2).value)-int(worksheet.cell(w.row+1,w.col+2).value)
    human=int(worksheet.cell(w.row,w.col+3).value)-int(worksheet.cell(w.row+1,w.col+3).value)
    rate='在過去的幾個小時內，水量上漲了$water個千早的高度，出現了$human個野生的P，看來今天是$weather'
    rate=rate.replace('$water',str(water))
    rate=rate.replace('$human',str(human))
    if water<200:
        weather='風和日麗的好天氣'
    elif water>=200 and water<250:
        weather='下著雨的衝浪天'
    elif water>=250 and water<400:
        weather='人狼泛舟的颱風天'
    elif water>=400 and water<650:
        weather='美咲不能釣魚的一天'
    elif water>=650 and water<1000:
        weather='志保阿克亞雨宮天'
    elif water>=1000 and water<1500:
        weather='南南東方向颱風來襲，已發佈陸警'
    else:
        weather='765劇場愚人節'
    rate=rate.replace('$weather',weather)
    if water>20 or human!=0:
        bot.send_message(chat_id=-1001232423456,text=rate)


def realtime_history(bot,update):
    chat_id=-1001232423456
    
    time = datetime.now().strftime("%y/%m/%d %H:%M:%S")
    
    scope = ['https://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_name('auth.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(spreadsheet_key)
    worksheet=sheet.worksheet('last_message')
    
    c=get_cell(str(chat_id),worksheet)
    message_id=worksheet.cell(c.row,c.col+1).value
    count=bot.get_chat_members_count(chat_id)
    list=[str(chat_id),time,message_id,str(count)]
    
    worksheet=sheet.worksheet('gr')
    w=get_cell(str(chat_id),worksheet)
    water=int(message_id)-int(worksheet.cell(w.row,w.col+2).value)
    human=count-int(worksheet.cell(w.row,w.col+3).value)
    rate='在過去的幾個小時內，水量上漲了$water個千早的高度，出現了$human個野生的P，看來今天是$weather'
    rate=rate.replace('$water',str(water))
    rate=rate.replace('$human',str(human))
    if water<200:
        weather='風和日麗的好天氣'
    elif water>=200 and water<250:
        weather='下著雨的衝浪天'
    elif water>=250 and water<400:
        weather='人狼泛舟的颱風天'
    elif water>=400 and water<650:
        weather='美咲不能釣魚的一天'
    elif water>=650 and water<1000:
        weather='志保阿克亞雨宮天'
    elif water>=1000 and water<1500:
        weather='南南東方向颱風來襲，已發佈陸警'
    else:
        weather='765劇場愚人節'
    rate=rate.replace('$weather',weather)
    bot.send_message(chat_id=update.message.chat_id,text=rate,reply_to_message_id=update.message.message_id)


def tis(bot,update):
    time = datetime.now().strftime("%H:%M:%S")
    time='現在時間:'+time
    #datetime.datetime.now()
    bot.send_message(chat_id=update.message.chat_id,text=time)
    
def kenka(bot,update):
    text='$888 你要我打誰？'
    text=text.replace("$888",str(update.message.from_user.first_name))
    bot.send_message(chat_id=update.message.chat_id,text=text)
    
def punch(bot,update,args):
    bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
    text = ' '.join(args)+'吃我木蘭飛彈ㄅ'
    bot.send_message(chat_id=update.message.chat_id, text=text)
    
def caps(bot, update, args):
    bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
    text_caps = ' '.join(args).upper()
    bot.send_message(chat_id=update.message.chat_id, text=text_caps)
    
def urope(bot,update):
    result=gasya()
    text_1='<pre>'+result['flavorText']+'</pre>\n\n'
    text_1=text_1.replace('{$P$}',update.message.from_user.first_name+'P')
    text_2='<pre>'+result['name']+'</pre>'
    rare=result['rarity']
    if rare==2:
        rare='(R)'
    elif rare==3:
        rare='(SR)'
    else:
        rare='(SSR)'
    bot.send_message(chat_id=update.message.chat_id,text=text_1+text_2+rare,parse_mode='HTML')

def pt():
    data=event_score()
    name=data['name']
    output='{0:>5}{1:>8}{2:>8} +{3:>6}/120mins\n'
    border=[]
    for i in (100,2500,5000,10000,25000):
        ostr=output.format(data[i]['rank'],data[i]['now'],data[i]['past_2'],data[i]['now']-data[i]['past_2'])
        border.append(ostr)
    text='<pre>'+name+'\n'+output.format('排名','最近集計','2h前集計','增加pt')
    for i in border:
        text=text+i
    text=text+'</pre>'
    return text
    
def Ept(bot,update):
    bot.send_message(chat_id=update.message.chat_id,text=pt(),parse_mode='HTML')
    
def Ept2h(bot,job):
    bot.send_message(chat_id=-313454366,text=pt(),parse_mode='HTML')
    
renda_id=0
combo=0
buffer_quote=[]
buffer_config=[]
def buffer_refresh(bot,job):
    global buffer_quote

    qsheet=get_sheet('quote')
    buffer_quote=qsheet.get_all_values()
    
    
@run_async
def quote(bot,update):
    
    global renda_id
    global combo
    global buffer_quote
    global del_list
    if renda_id==update.message.from_user.id:
        combo=combo+1
    else:
        renda_id=update.message.from_user.id
        combo=1
    if combo>4 and combo<7:
        msg=bot.send_message(chat_id=update.message.chat_id,text='又ㄅ是7az，連打ㄍㄆ')
        del_list.append([update.message.chat_id,msg.message_id])
        
        del_cmd(bot,update)
        return
    if combo>6:
        del_cmd(bot,update)
        return
    num=random.randint(0,len(buffer_quote)-1)
    text='<pre>'+buffer_quote[num][0]+'</pre>\n'+'-----<b>'+buffer_quote[num][1]+'</b> より'
    msg=bot.send_message(chat_id=update.message.chat_id,text=text,parse_mode='HTML')
    
    del_list.append([update.message.chat_id,msg.message_id])
    del_cmd(bot,update)

def inline_quote(bot,update):
    global renda_id
    global combo
    global buffer_quote
    query=update.inline_query.query
    if not query:
        return
    if query=='quote':
    if renda_id==update.inline_query.from_user.id:
        combo=combo+1
    else:
        renda_id=update.inline_query.from_user.id
        combo=1
    num=random.randint(0,len(buffer_quote)-1)
    text='<pre>'+buffer_quote[num][0]+'</pre>\n'+'-----<b>'+buffer_quote[num][1]+'</b> より'
    if combo>4 and combo<7:
        text='又ㄅ是7az，連打ㄍㄆ'
        return
    if combo>6:
        return

    
    iquote=InlineQueryResultArticle(
            id=str(datetime.now()),
            title='quote',
            input_message_content=InputTextMessageContent(message_text=text,parse_mode='HTML')
            )
    bot.answer_inline_query(inline_query_id=update.inline_query.id,results=[iquote])
    
        
del_list=[]
def del_quote(bot,job):
    global del_list
    game_del=False
    for i in del_list:
        chat_id=i[0]
        if chat_id=='-1001232423456':
            game_del=True
        message_id=i[1]
        if chat_id!='':
            try:
                bot.delete_message(chat_id=chat_id, message_id=message_id)
            except:
                pass
    if game_del==True:
        msg=bot.send_sticker(chat_id=-1001232423456,sticker='CAADBQAD_gQAAsZRxhWSuVC6Vxj01gI')
        msg1=bot.send_message(chat_id=-1001232423456,text='好ㄘ')
        time.sleep(5)
        bot.delete_message(chat_id=-1001232423456, message_id=msg.message_id)
        bot.delete_message(chat_id=-1001232423456, message_id=msg1.message_id)
            
    
@run_async
def dice(bot,update,args):
    """Send a message when the command /dice is issued."""
    dice=['⚀','⚁','⚂','⚃','⚄','⚅']
    count=[0,0,0,0,0,0]
    text=''
    
    if not args:
        #dice 1
            msg=bot.send_message(chat_id=update.message.chat_id, text=dice[randrange(6)])
    else:
        dice_num=' '.join(args)
        try:
            num=int(dice_num)
        except:
            #value error
            return
        else:
            if num>1000:
                return
            else:
                for i in range(0,num):
                    j=randrange(6)
                    text=text+dice[j]
                    count[j]=count[j]+1
                msg=bot.send_message(chat_id=update.message.chat_id, text=text)
                text=''
                for i in range(0,6):
                    text=text+dice[i]+str(count[i])+'個\n'
                if num>20:
                    msg1=bot.send_message(chat_id=update.message.chat_id, text=text)
                    time.sleep(7)
                    bot.delete_message(chat_id=update.message.chat_id, message_id=msg.message_id)
                    bot.delete_message(chat_id=update.message.chat_id, message_id=msg1.message_id)
    
def inline_ku(bot,update):
    query=update.inline_query.query+"?\nくっ......"
    
    if not query:
        return
    results = list()
    result=InlineQueryResultArticle(
        id=query.upper(),
        title='KU',
        input_message_content=InputTextMessageContent(query)
        )
    bot.answer_inline_query(update.inline_query.id, results)

#inline_ku_handler = InlineQueryHandler(inline_ku)
#dispatcher.add_handler(inline_ku_handler)
last_message_list=[]
def update_lastm(bot,job):
    global last_message_list
    scope = ['https://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_name('auth.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(spreadsheet_key)
    worksheet=sheet.worksheet('last_message')
    
    for i in last_message_list:
        try:
            cell=worksheet.find(i[0])
        except:#not found
            worksheet.insert_row(i, 1)
        else:
            worksheet.update_cell(cell.row,cell.col+1,i[1])

def sora(bot,update):
    y=key_word_reaction_json(update.message.text)
    if y!=None:
        for i in y:
            if i[0]=='t':
                bot.send_message(chat_id=update.message.chat_id, text=i[1])
            elif i[0]=='p':
                bot.send_photo(chat_id=update.message.chat_id, photo=i[1])
            elif i[0]=='s':
                bot.send_sticker(chat_id=update.message.chat_id, sticker=i[1])
            elif i[0]=='v':
                bot.send_video(chat_id=update.message.chat_id, video=i[1])
    #an filter handler
    #predict to be unable if privacy mode is on(st bot can't heard text filter real time)
    chat_id=update.message.chat_id
    lmessage_id=update.message.message_id
    list=[str(chat_id),lmessage_id]
    global last_message_list
    fvalue=False
    for i in last_message_list:
        if i[0].find(list[0])!=-1:
            fvalue=True
            i[1]=list[1]
            break
    if fvalue==False:
        last_message_list.append(list)
    
    
    test=str(update.message.text)
    
    if test.find(' #名言')!=-1 or test.find('#名言 ')!=-1:
        if update.message.reply_to_message==None and update.message.from_user.is_bot==False:
            test=test.replace(' #名言','').replace('#名言 ','')
            qlist=[test,update.message.from_user.first_name]
            work_sheet_push(qlist,'quote')
            return
    if test.find('#名言')!=-1:
        if update.message.reply_to_message is not None and update.message.reply_to_message.from_user.is_bot==False:
            qlist=[update.message.reply_to_message.text,update.message.reply_to_message.from_user.first_name]
            work_sheet_push(qlist,'quote')
            return
    if test.find('adp@db')!=-1:
        rmsg=update.message.reply_to_message
        col=['name','url']
        if rmsg.text.find('http')!=-1:
            data=['adp',rmsg.text]
            dbsave('randchihaya',data,col)
            return
        if rmsg.photo!=None:
            data=['adph',rmsg.photo[len(rmsg.photo)-1].file_id]
            dbsave('randchihaya',data,col)
            return
        
    if test.find('tsumu@db')!=-1:
        rmsg=update.message.reply_to_message
        col=['name','url']
        if rmsg.text.find('http')!=-1:
            data=['adp',rmsg.text]
            dbsave('randtsumugi',data,col)
            return
        if rmsg.photo!=None:
            data=['adph',rmsg.photo[len(rmsg.photo)-1].file_id]
            dbsave('randtsumugi',data,col)
            return
    if test.find('stm@db')!=-1:
        rmsg=update.message.reply_to_message
        if rmsg.sticker!=None:
            N=rmsg.sticker.set_name
            set=bot.get_sticker_set(N)
            
            col=['setname','about']
            dbsave('sticker',[N,set.title],col)
    
    if test.find('fid')!=-1:
        rmsg=update.message.reply_to_message
        if rmsg.photo!=None:
            for i in rmsg.photo:
                bot.send_message(chat_id=update.message.chat_id, text=i.file_id)
                text=str(i.width)+'x'+str(i.height)
                bot.send_message(chat_id=update.message.chat_id, text=text)
        if rmsg.video!=None:
            bot.send_message(chat_id=update.message.chat_id, text=rmsg.video.file_id)
        if rmsg.sticker!=None:
            bot.send_message(chat_id=update.message.chat_id, text=rmsg.sticker.file_id)
        if rmsg.document!=None:
            bot.send_message(chat_id=update.message.chat_id, text=rmsg.document.file_id)
    if test.find(' #とは')!=-1 or test.find('#とは ')!=-1:
        if update.message.reply_to_message==None:
            test=test.replace(' #とは','').replace('#とは ','')
            exist='http://api.nicodic.jp/page.exist/n/a/'+test
            r=requests.get(exist).text
            if r=='n(1);':
                summary='http://api.nicodic.jp/page.summary/n/a/'+test
                r=requests.get(summary).text
                r=r.replace('n(','').replace(');','')
                dicc=json.loads(r)
                bot.send_message(chat_id=update.message.chat_id, text=dicc['summary'])
                #bot.send_message(chat_id=update.message.chat_id, text=summary(test))
            
            return


    #work_sheet_push(list,'last_message')
    if test.find('我也愛そらそら')!=-1:
        bot.send_message(chat_id=update.message.chat_id, text="我愛そらそら一生一世")
    elif test.find('我愛そらそら')!=-1:
        bot.send_message(chat_id=update.message.chat_id, text="我愛そらそら一生一世")
    elif test.find('そらそら')!=-1:
        bot.send_message(chat_id=update.message.chat_id,text="我愛そらそら")
    
    elif test.find("72")!=-1:
        bot.send_sticker(chat_id=update.message.chat_id, sticker="CAADBQAD5gQAAsZRxhVjgK6PcwABUaUC")
        #bot.send_message(chat_id=update.message.chat_id, text="媽的，72是有錯一樣！一直7272不會煩嗎？")
        #bot.leave_chat(chat_id=update.message.chat_id)
        #bot.send_message(chat_id=update.message.chat_id, text="939393939393939393!!!!!!!!!!")
        
    elif test.find("飯店")!=-1:
        bot.send_message(chat_id=update.message.chat_id, text="TRIVAGO!!!!!!!!!!")
    elif test=='下班':
        return
        time = datetime.now().strftime("%H:%M:%S")
        time='現在時間:'+time+'\n下班囉XDD'
        #datetime.datetime.now()
        bot.send_message(chat_id=update.message.chat_id,text=time)
    else:
        #bot.send_message(chat_id='', text="不要玩弄我ㄉ感情")
        #bot.send_message(chat_id='', text=str(update.message.date))
        if update.message.new_chat_members!=None:
            new_chat_members=update.message.new_chat_members
            for u in new_chat_members:
                text='野生的'+u.first_name+'出現了'
                bot.send_message(chat_id=update.message.chat_id,text=text)
        if update.message.left_chat_member!=None:
            text=update.message.left_chat_member.first_name+'，6666666666！'
            bot.send_message(chat_id=update.message.chat_id,text=text)
        '''if update.message.sticker!=None and update.message.chat.id==-313454366:
            bot.send_message(chat_id=-313454366,text=update.message.sticker.file_id)'''

def unknown(bot, update):
    if update.message.entities[4].id==bot.get_me().id:
        bot.send_message(chat_id=update.message.chat_id, text="すみません、よく分かりません。")

def sticker_matome(bot,update):
'''
    query = update.inline_query
    mode=False
    if not query:
        pass
    elif query.query=='sticker':
        mode=True
    '''
    link=dbget('sticker','setname')
    stitle=dbget('sticker','about')
    slink=''
    for i in range(len(link)):
        slink=slink+'<a href="https://telegram.me/addstickers/'+link[i][0]+'">'+stitle[i][0]+'</a>\n'
    startme='<a href="https://telegram.me/Chiahayabot?start=sticker">請先在私訊START</a>'
    
    '''
    if mode:
        results=[]
        qok=InlineQueryResultArticle(
            
            id=str(datetime.now()),title='MATOME',
            input_message_content=InputTextMessageContent(message_text='傳送中~~')
            )
        bot.answer_inline_query(update.inline_query.id,[qok],switch_pm_text='sticker',switch_pm_parameter='sticker')
        try:
            bot.send_message(chat_id=query.from_user.id,text=slink,parse_mode='HTML')
        except:
            result.append(qstartme)
            qstartme=InlineQueryResultArticle(
                id=str(datetime.now()),
                title='MATOME',
                input_message_content=InputTextMessageContent(message_text=startme,parse_mode='HTML')
                )

            

        
    else: 
'''    
    try:
        bot.send_message(chat_id=update.message.from_user.id,text=slink,parse_mode='HTML')
    except:
        bot.send_message(chat_id=update.message.chat_id,text=startme,parse_mode='HTML')

def wake(bot,update):
#prevent bot from going to sleep
    bot.send_message(chat_id=580276512, text="すみません、よく分かりません。")

class MQBot(telegram.bot.Bot):
    '''A subclass of Bot which delegates send method handling to MQ'''
    def __init__(self, *args, is_queued_def=True, mqueue=None, **kwargs):
        super(MQBot, self).__init__(*args, **kwargs)
        # below 2 attributes should be provided for decorator usage
        self._is_messages_queued_default = is_queued_def
        self._msg_queue = mqueue or mq.MessageQueue()

    def __del__(self):
        try:
            self._msg_queue.stop()
        except:
            pass
        super(MQBot, self).__del__()

    @mq.queuedmessage
    def send_message(self, *args, **kwargs):
        '''Wrapped method would accept new `queued` and `isgroup`
        OPTIONAL arguments'''
        return super(MQBot, self).send_message(*args, **kwargs)

kw_j_buffer=[]
def key_word_j_buffer(bot,job):
    global kw_j_buffer
    kw_j_buffer_temp=[]
    k=[]
    key_word_j=get_sheet('key_word_j')
    try:
        k=key_word_j.get_all_values()
    except:
        return
    else:
        for i in k:
            try:
                temp=json.loads(i[0])
            except:
                pass
            else:
                kw_j_buffer_temp.append(temp)
    kw_j_buffer=kw_j_buffer_temp

def key_word_reaction_json(word):
    global kw_j_buffer
    list_k=[]
    for i in kw_j_buffer:
        temp_t=find_word(word,i['key_words'],echo=i['echo'],prob=i['prob'],els=i['els'],allco=i['allco'],photo =i['photo'], video=i['video'],sticker=i['sticker'])
        if temp_t != None:
            list_k.append(temp_t)
    return list_k
    '''
    key_word_j=get_sheet('key_word_j')
    list_k=[]
    try:
        kw=key_word_j.get_all_values()
    except:
        return None
    else:
        for i in kw:
            temp=json.loads(i[0])
            temp_t=find_word(word,temp['key_words'],echo=temp['echo'],prob=temp['prob'],els=temp['els'],allco=temp['allco'],photo =temp['photo'], video=temp['video'],sticker=temp['sticker'])
            if temp_t != None:
                list_k.append(temp_t)
        return list_k
    '''

def find_word(sentence,key_words, echo=None, prob=100, els=None,photo =None, video=None,sticker=None, allco=False):
    #sentence:sentence user send
    # words: words need to reaction
    # echo: msg send after reaction
    # prob: probability, if not, send els msg
    # els: if not in prob
    list_r=['','']
    # a random number from 0 to 99
    num = randrange(100)
    key_words_value=False
    for check in key_words:
        if allco == False:
             if sentence.find(check)!=-1:
                key_words_value=True
        if allco == True:
            if sentence.find(check)!=-1:
                key_words_value=True
            else:
                key_words_value=False
                break
    if echo != None:
        if key_words_value==True and num<prob:
            list_r[0]='t'
            list_r[1]=echo
            return list_r
        if key_words_value==True and num>=prob and els!=None:
            list_r[0]='t'
            list_r[1]=els
            return list_r
    elif photo!=None:
        if key_words_value==True and num<prob:
            list_r[0]='p'
            list_r[1]=photo
            return list_r
    elif video != None:
        if key_words_value==True and num<prob:
            list_r[0]='v'
            list_r[1]=video
            return list_r
    elif sticker != None:
        if key_words_value==True and num<prob:
            list_r[0]='s'
            list_r[1]=sticker[randrange(len(sticker))]
            return list_r
    return None

def key_word_reaction(word):
    a=get_sheet('key_word')
    try:
        kw=a.get_all_values()
    except:
        return None
    else:
        for i in kw:
            if word.find(i[0])!=-1:
                return i[1]
        return None
def quote_d(bot,update):
    #daily quote
    if get_config(update.message.from_user.id,'q')==True:
        del_cmd(bot,update)
        return
    else:
        set_config(update.message.from_user.id,'q')
        del_cmd(bot,update)
    scope = ['https://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_name('auth.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(spreadspreadsheet_key)
    quote=sheet.worksheet('quote_main').get_all_values()
    num=random.randint(0,len(quote)-1)
    text='<pre>'+quote[num][0]+'</pre>\n'+'-----<b>'+quote[num][1]+'</b> より'
    msg=bot.send_message(chat_id=update.message.chat_id,text=text,parse_mode='HTML')

def main():
    q = mq.MessageQueue(all_burst_limit=3, all_time_limit_ms=3000)
    # set connection pool size for bot 
    request = Request(con_pool_size=14)
    chihabot = MQBot(token, request=request, mqueue=q)
    updater = Updater(token,workers=10)
    dispatcher = updater.dispatcher
    #global function
    global stop_and_restart
    def stop_and_restart():
        updater.stop()
        os.execl(sys.executable, sys.executable, *sys.argv)
    


    #job
    #updater.job_queue.run_daily(daily_reset,stime(18,22,0))
    updater.job_queue.run_repeating(del_quote, interval=72, first=0)
    updater.job_queue.run_repeating(key_word_j_buffer, interval=60, first=0)
    updater.job_queue.run_repeating(update_lastm, interval=60, first=0)
    updater.job_queue.run_repeating(buffer_refresh, interval=60, first=0)
    updater.job_queue.run_repeating(wake, interval=600, first=0)
    updater.job_queue.run_repeating(dbupdate, interval=86400, first=0)
    jd=False
    eventborder=[stime(0,0,40),stime(2,0,40),stime(0,0,40),stime(2,0,40),stime(4,0,40),stime(6,0,40),stime(8,0,40),stime(10,0,40),stime(12,0,40),stime(14,0,40),stime(16,0,40),stime(18,0,40),stime(20,0,40),stime(22,0,40)]
    for t in eventborder:
        updater.job_queue.run_daily(Ept2h,t)
    
    history_t=[stime(3,0,0),stime(9,0,0),stime(15,0,0),stime(21,0,0)]
    
    for t in history_t:
        job_his = updater.job_queue.run_daily(history,t)
    #command
    dispatcher.add_handler(CommandHandler('taitoru',title,pass_args=True))
    dispatcher.add_handler(CommandHandler('start', start,pass_args=True))
    dispatcher.add_handler(CommandHandler('help', help))
    dispatcher.add_handler(CommandHandler('linkstart',invite))
    dispatcher.add_handler(CommandHandler('bomb',bomb,pass_args=True))
    dispatcher.add_handler(CommandHandler('gdmn',gdmn))
    dispatcher.add_handler(CommandHandler('set',set_name,pass_args=True))
    dispatcher.add_handler(CommandHandler('dice',dice,pass_args=True))#dic
    dispatcher.add_handler(CommandHandler('count',count))
    dispatcher.add_handler(CommandHandler('water',realtime_history))
    dispatcher.add_handler(CommandHandler('grave',grave))
    dispatcher.add_handler(CommandHandler('time',tis))
    dispatcher.add_handler(CommandHandler('kenka',kenka))
    dispatcher.add_handler(CommandHandler('about',about))
    dispatcher.add_handler(CommandHandler('state',state))
    dispatcher.add_handler(CommandHandler('quote',quote))
    dispatcher.add_handler(CommandHandler('qt',quote_d))
    dispatcher.add_handler(CommandHandler('pt',Ept))
    dispatcher.add_handler(CommandHandler('sticker',sticker_matome))
    dispatcher.add_handler(CommandHandler('randChihaya',randchihaya))
    dispatcher.add_handler(CommandHandler('randTsumugi',randtsumugi))
    dispatcher.add_handler(CommandHandler('gasya',urope))
    dispatcher.add_handler(CommandHandler('sk',set_kw,pass_args=True))
    dispatcher.add_handler(CommandHandler('punch', punch, pass_args=True))
    dispatcher.add_handler(CommandHandler('caps', caps, pass_args=True))
    dispatcher.add_handler(CommandHandler('r', restart, filters=Filters.user(user_id=580276512)))
    
    
    dispatcher.add_handler(InlineQueryHandler(iquote))
    #filters
    dispatcher.add_handler(MessageHandler(Filters.command, unknown))
    dispatcher.add_handler(MessageHandler(Filters.all,sora))
    
    #start bot
    updater.start_polling(clean=True)
    updater.idle()



if __name__ == '__main__':
    main()