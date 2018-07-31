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
import datetime as dt
from datetime import datetime, tzinfo, timedelta
from datetime import time as stime
from telegram import InlineQueryResultArticle, InputTextMessageContent,InlineKeyboardMarkup,InlineKeyboardButton
from telegram.ext import Updater,CommandHandler,MessageHandler,Filters,InlineQueryHandler,JobQueue
from telegram.ext.dispatcher import run_async
import python3pickledb as pickledb
import gspread
from oauth2client.service_account import ServiceAccountCredentials
debug_mode=False



if debug_mode is False:
    token = os.environ['TELEGRAM_TOKEN']
    json=os.environ['JSON']
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

HALF2FULL = dict((i, i + 0xFEE0) for i in range(0x21, 0x7F))
HALF2FULL[0x20] = 0x3000
def fullen(s):
    '''
    Convert all ASCII characters to the full-width counterpart.
    '''
    
    text=s.replace(' ','　').replace('@','＠').replace('_','＿').replace('.','‧')
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
        spreadsheet.add_worksheet(worksheet_name,len(values),2)
        worksheet=spreadsheet.worksheet(worksheet_name)
        worksheet.insert_row(values,2)
    else:
        worksheet.insert_row(values,2)
#usage (values[list of string],worksheet_name[string])
#put a list of value and push to worksheet

def work_sheet_pop(key,woksheet_name):
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
#tool func
'''
daily_remind=updater.job_queue
def callback11(bot,job):
    bot.send_message(chat_id='580276512',text='想下班')
t = time(17, 30, 30, tzinfo=GMT8())
job_m=daily_remind.run_daily(callback11,t)
'''
#unsolve:TypeError: can't compare offset-naive and offset-aware times


def start(bot, update):
    bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
    bot.send_message(chat_id=update.message.chat_id, text="如月千早です。劇場という場所があることは、レッスンの励みにもなりますね。これからも、厳しいご指導をよろしくお願いします。")
    bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
    bot.send_message(chat_id=update.message.chat_id, text='私のコマンドリストです：\n/start-名為72的偶像\n/help-72能做什麼?\n/time-現在幾點\n/gdmn-早安\n/set-set早安名\n/kenka-吵架\n/grave-擔當太尊而猝死的P用\n/quote-千早歌詞集\n/bomb-自爆吧P\n/count-test function count members\n/dice-N粒公正的骰子(N<1000)\n/water-即時水量\n/about-關於此bot')
    
    button_list=[
        InlineKeyboardButton(text='start',switch_inline_query='/start',switch_inline_current_chat='/start'),
        InlineKeyboardButton(text='about 72',url='https://imasml-theater-wiki.gamerch.com/%E5%A6%82%E6%9C%88%E5%8D%83%E6%97%A9#content_2_13')
        ]
    
    reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=1))
    bot.send_message(chat_id=update.message.chat_id, text="A menu test", reply_markup=reply_markup)
    '''test of inline button'''

def help(bot,update):
    bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
    bot.send_message(chat_id=update.message.chat_id, text='私のコマンドリストです：\n/start-名為72的偶像\n/help-72能做什麼?\n/time-現在幾點\n/gdmn-早安\n/set-set早安名\n/kenka-吵架\n/grave-擔當太尊而猝死的P用\n/quote-千早歌詞集\n/bomb-自爆吧P\n/count-test function count members\n/dice-N粒公正的骰子(N<1000)\n/water-即時水量\n/about-關於此bot')

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
            plist=re.findall(r'\w{1,7}',pname)
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
        plist=re.findall(r'\w{1,1}',pname)
        for a in range(0,l):
            
            t=nak.replace('$name',plist[a])
            op+=t
        op+=bas
        bot.send_message(chat_id=update.message.chat_id,text=op)

'''
　　　／￣￣〈￣￣＼ :.＼ 
　　 |　　　　　　　　|: ::| 
　 　|　他給Ｐ　　　　|: ::| 
　 　|　　　　　　　　|: ::| 
　 　|　takep~~ 　　　|: ::| 
　 　|　　　　　　　　|: ::| 
　 　|　　　　　　　　|: ::| 
　 　|　　　　　　　　|: ::| 
￣"￣"￣'￣￣""￣""￣.￣'￣￣ 



'''


'''
　　 ＿ 
　　|ク| 
　　|ナ| 
　　|ウ| 
　　|ド| 
　　|＠| 
　　|蝉| 
　|￣￣￣| 
　| |三三| | 
￣￣￣￣￣￣ 



'''







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

@run_async
def quote(bot,update):
    scope = ['https://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_name('auth.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(spreadsheet_key)
    qsheet=sheet.worksheet('quote')
    quote=qsheet.get_all_values()
    num=random.randint(0,len(quote)-1)
    text='<pre>'+quote[num][0]+'</pre>\n'+'-----<b>'+quote[num][1]+'</b> より'
    bot.send_message(chat_id=update.message.chat_id,text=text,parse_mode='HTML')

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

def sora(bot,update):
    #an filter handler
    #predict to be unable if privacy mode is on(st bot can't heard text filter real time)
    scope = ['https://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_name('auth.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(spreadsheet_key)
    worksheet=sheet.worksheet('last_message')
    chat_id=update.message.chat_id
    lmessage_id=update.message.message_id
    list=[str(chat_id),lmessage_id]
    try:
        cell=worksheet.find(str(chat_id))
    except:#not found
        worksheet.insert_row(list, 2)
    else:
        worksheet.update_cell(cell.row,cell.col+1,lmessage_id)
    
    
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
        return
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
        if update.message.sticker!=None and update.message.chat.id==-313454366:
            bot.send_message(chat_id=-313454366,text=update.message.sticker.file_id)

def unknown(bot, update):
    if update.message.entities[4].id==bot.get_me().id:
        bot.send_message(chat_id=update.message.chat_id, text="すみません、よく分かりません。")

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

def main():
    q = mq.MessageQueue(all_burst_limit=3, all_time_limit_ms=3000)
    # set connection pool size for bot 
    request = Request(con_pool_size=14)
    chihabot = MQBot(token, request=request, mqueue=q)
    updater = Updater(workers=10,bot=chihabot)
    dispatcher = updater.dispatcher
    #global function
    global stop_and_restart
    def stop_and_restart():
        updater.stop()
        os.execl(sys.executable, sys.executable, *sys.argv)
    


    #job
    jd=False
    history_t=[stime(3,0,0),stime(9,0,0),stime(15,0,0),stime(21,0,0)]
    job_minute = updater.job_queue.run_repeating(wake, interval=600, first=0)
    for t in history_t:
        job_his = updater.job_queue.run_daily(history,t)
    #command
    dispatcher.add_handler(CommandHandler('title',title,pass_args=True))
    dispatcher.add_handler(CommandHandler('start', start))
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
    dispatcher.add_handler(CommandHandler('punch', punch, pass_args=True))
    dispatcher.add_handler(CommandHandler('caps', caps, pass_args=True))
    dispatcher.add_handler(CommandHandler('r', restart, filters=Filters.user(user_id=580276512)))
    #filters
    dispatcher.add_handler(MessageHandler(Filters.command, unknown))
    dispatcher.add_handler(MessageHandler(Filters.all,sora))
    
    #start bot
    updater.start_polling(clean=True)
    updater.idle()



if __name__ == '__main__':
    main()