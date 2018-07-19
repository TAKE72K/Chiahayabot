import telegram
from datetime import datetime,time, tzinfo, timedelta
from telegram import InlineQueryResultArticle, InputTextMessageContent,InlineKeyboardMarkup,InlineKeyboardButton
from telegram.ext import Updater,CommandHandler,MessageHandler,Filters,InlineQueryHandler,JobQueue
'''not sure if need to import'''
#遊戲部ID:-1001232423456

updater=Updater(token='TOKEN')

dispatcher = updater.dispatcher
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)

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

	
	
class GMT8(tzinfo):
	def utcoffset(self, dt):
		return timedelta(hours=8)
	def dst(self, dt):
		return timedelta(0)
	def tzname(self,dt):
		return "TAIWAN"
	
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
	
	button_list=[
		InlineKeyboardButton(text='start',switch_inline_query='Chiahayabot',switch_inline_current_chat='/start'),
		InlineKeyboardButton(text='about 72',url='https://imasml-theater-wiki.gamerch.com/%E5%A6%82%E6%9C%88%E5%8D%83%E6%97%A9#content_2_13')
		]
	reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=1))
	bot.send_message(chat_id=update.message.chat_id, text="A menu test", reply_markup=reply_markup)
	'''test of inline button'''


start_handler = CommandHandler(['start','help'], start)
dispatcher.add_handler(start_handler)

def gdmn(bot,update):
	#a good morning func
	bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)#type effect
	
	
	text=" $username P、おはようございます。今日も一日頑張るぞい"
	#aoba kawaii na--
	
	message=update.message
	chat_id = message.chat.id
	bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
	#replace $username
	text=text.replace("$username",str(update.message.from_user.first_name))
	
	#bot.send_photo(chat_id,photo='AgADBQADSagxG3VSeVaStO9CCRE_trYo1TIABKGMGsglQ3cr9BoCAAEC')
	#doc:photo=a filelike object ,suggest to be replace with file_id
	
	bot.send_message(chat_id=update.message.chat_id,text=text)
	
	
	custom_keyboard = [['/start', '/gdmn'], ['72', '找飯店'],['そらそら']]
	
	reply_markup = telegram.ReplyKeyboardMarkup(keyboard=custom_keyboard,one_time_keyboard=True)#one_time_kb:initial false ,dissapear after touch once
	
	bot.send_message(chat_id=chat_id, text="KeyBoard test~~", reply_markup=reply_markup)


	
gdmn_handler=CommandHandler('gdmn',gdmn)
dispatcher.add_handler(gdmn_handler)



def tis(bot,update):
	time = datetime.now().strftime("%H:%M:%S")
	time='現在時間:'+time
	#datetime.datetime.now()
	bot.send_message(chat_id=update.message.chat_id,text=time)
	
tis_handler=CommandHandler('time',tis)
dispatcher.add_handler(tis_handler)





def sora(bot,update):
	#an filter handler
	#predict to be unable if privacy mode is on(st bot can't heard text filter real time)
	test=update.message.text
	if test=="そらそら":
		bot.send_message(chat_id=update.message.chat_id, text="我愛そらそら")
		
	elif test=="飯店" or test=="找飯店":
		bot.send_message(chat_id=update.message.chat_id, text="TRIVAGO!!!!!!!!!!")
	elif test=="72" :
		bot.send_message(chat_id=update.message.chat_id, text="939393939393939393!!!!!!!!!!")
		bot.send_sticker(chat_id=update.message.chat_id, sticker="CAADBQAD5gQAAsZRxhVjgK6PcwABUaUC")
	elif test=='下班':
		time = datetime.now().strftime("%H:%M:%S")
		time='現在時間:'+time+'\n下班囉XDD'
		#datetime.datetime.now()
		bot.send_message(chat_id=update.message.chat_id,text=time)
	else:
		bot.send_sticker(chat_id=update.message.chat_id, sticker="CAADBQAD5gQAAsZRxhVjgK6PcwABUaUC")

#Method: channels.inviteToChannel
#Result: {"_":"rpc_error","error_code":400,"error_message":"USER_KICKED"}
sora_handler=MessageHandler(Filters.all,sora)
dispatcher.add_handler(sora_handler)

'''def trivago(bot,update):
	test=update.message.text
	if test=="飯店":
		bot.send_message(chat_id=update.message.chat_id, text="TRIVAGO!!!!!")


trivago_handler=MessageHandler(Filters.text,trivago)
dispatcher.add_handler(trivago_handler)'''

'''def echo(bot, update):
	#bot.send_message(chat_id=update.message.chat_id, text="くっ......")
	bot.send_document(chat_id=update.message.chat_id, document="CAADBQAD5gQAAsZRxhVjgK6PcwABUaUC")
	bot.send_sticker(chat_id=update.message.chat_id, sticker="CAADBQAD5gQAAsZRxhVjgK6PcwABUaUC")
	
echo_handler = MessageHandler(Filters.text, echo)
dispatcher.add_handler(echo_handler)'''

def caps(bot, update, args):
	bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
	text_caps = ' '.join(args).upper()
	bot.send_message(chat_id=update.message.chat_id, text=text_caps)

caps_handler = CommandHandler('caps', caps, pass_args=True)
dispatcher.add_handler(caps_handler)


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

inline_ku_handler = InlineQueryHandler(inline_ku)
dispatcher.add_handler(inline_ku_handler)

def unknown(bot, update):
	bot.send_message(chat_id=update.message.chat_id, text="すみません、よく分かりません。")

unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)




updater.start_polling()
updater.idle()

updater.stop()