import telegram
import re
import random
import os
import logging
from datetime import datetime,time, tzinfo, timedelta
from telegram import InlineQueryResultArticle, InputTextMessageContent,InlineKeyboardMarkup,InlineKeyboardButton
from telegram.ext import Updater,CommandHandler,MessageHandler,Filters,InlineQueryHandler,JobQueue
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
kenka-吵架
grave-擔當太尊而猝死的P用
c-test function count members
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

HALF2FULL = dict((i, i + 0xFEE0) for i in range(0x21, 0x7F))
HALF2FULL[0x20] = 0x3000
def fullen(s):
    '''
    Convert all ASCII characters to the full-width counterpart.
    '''
    return str(s).translate(HALF2FULL)  
    
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
    bot.send_message(chat_id=update.message.chat_id, text='私のコマンドリストです：\n/start-名為72的偶像\n/help-72能做什麼?\n/time-現在幾點\n/gdmn-早安\n/kenka-吵架\n/grave-擔當太尊而猝死的P用\n/c-test function count members')
    
    button_list=[
        InlineKeyboardButton(text='start',switch_inline_query='/start',switch_inline_current_chat='/start'),
        InlineKeyboardButton(text='about 72',url='https://imasml-theater-wiki.gamerch.com/%E5%A6%82%E6%9C%88%E5%8D%83%E6%97%A9#content_2_13')
        ]
    
    reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=1))
    bot.send_message(chat_id=update.message.chat_id, text="A menu test", reply_markup=reply_markup)
    '''test of inline button'''

def help(bot,update):
    bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
    bot.send_message(chat_id=update.message.chat_id, text='私のコマンドリストです：\n/start-名為72的偶像\n/help-72能做什麼?\n/time-現在幾點\n/gdmn-早安\n/kenka-吵架\n/grave-擔當太尊而猝死的P用\n/c-test function count members')
    
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
            bot.send_message(chat_id=update.message.chat_id,text='Bot:Not enough rights to change chat title')
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









def history(bot,job):
    chat_id=-1001232423456
    time = datetime.now().strftime("%d %m %y %H:%M:%S")
    message_id=''
    count=bot.get_chat_members_count(chat_id)
    list=[time,message_id,str(count)]
    work_sheet_push(list,'gr')

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
    test=str(update.message.text)

    chat_id=update.message.chat_id
    lmessage_id=update.message.message_id
    list=[chat_id,lmessage_id]
    work_sheet_push(list,'last_message)
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


def main():
    updater = Updater(token)
    dispatcher = updater.dispatcher



    #job
    jd=False
    job_minute = updater.job_queue.run_repeating(wake, interval=600, first=0)
    job_his = updater.job_queue.run_repeating(history, interval=600, first=0)
    #command
    dispatcher.add_handler(CommandHandler('title',title,pass_args=True))
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('help', help))
    dispatcher.add_handler(CommandHandler('linkstart',invite))
    dispatcher.add_handler(CommandHandler('bomb',bomb,pass_args=True))
    dispatcher.add_handler(CommandHandler('gdmn',gdmn))
    dispatcher.add_handler(CommandHandler('set',set_name,pass_args=True))
    dispatcher.add_handler(CommandHandler('count',count))
    dispatcher.add_handler(CommandHandler('grave',grave))
    dispatcher.add_handler(CommandHandler('time',tis))
    dispatcher.add_handler(CommandHandler('kenka',kenka))
    dispatcher.add_handler(CommandHandler('punch', punch, pass_args=True))
    dispatcher.add_handler(CommandHandler('caps', caps, pass_args=True))
    #filters
    dispatcher.add_handler(MessageHandler(Filters.command, unknown))
    dispatcher.add_handler(MessageHandler(Filters.all,sora))
    
    #start bot
    updater.start_polling()
    updater.idle()



if __name__ == '__main__':
    main()