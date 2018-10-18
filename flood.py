from datetime import datetime as dt
from datetime import timedelta as td
import queue
import telegram
class FloodLimit:
    
    def __init__(self,msgInit,banF=0.5,restrictT=32,threshold=3):
        self.messageSet=queue.Queue(40)
        self.userId=msgInit.from_user.id
        self.userName=msgInit.from_user.first_name
        self.chatId=msgInit.chat.id
        self.frequence=banF
        self.restrictT=restrictT
        self.threshold=threshold
        
        date=msgInit.date
        msgId=msgInit.message_id
        msgReco={'date':date,
                'msgId':msgId}
        self.messageSet.put(msgReco)
    def detectMsg(self,msg,bot):
        if msg.from_user.id != self.userId:
            return False
        if msg.chat.id !=self.chatId:
            return False
        
        date=msg.date
        msgId=msg.message_id
        msgReco={'date':date,
                'msgId':msgId}
        self.messageSet.put(msgReco)
        
        ban=self.floodCheck(msgReco,bot)
        return True
    def floodCheck(self,msgTop,bot):
         
        timeL=False
        t=0
        #check time ligal
        while not timeL:
            if self.messageSet.qsize()<2:
                break
            btm=self.messageSet.get()
            deltaT=(msgTop['date']-btm['date']).total_seconds()
            
            if deltaT<60 and deltaT>=self.threshold:
                t=deltaT
                timeL=True
            if deltaT<self.threshold:
                timeL=True
                return
            if self.messageSet.empty():
                timeL=True
                return
        #check frequence
        floodBan=False
        userF=self.messageSet.qsize()/t
        if userF>self.frequence:
            floodBan=True
        #ban user
        if floodBan:
            print(self.userName)
            #print(self.messageSet)
            bot.restrict_chat_member(self.chatId,self.userId,
            until_date=dt.now()+td(0,self.restrictT,0),
            can_send_messages=False, can_send_media_messages=False,
            can_send_other_messages=False)
            bot.send_message(chat_id=self.chatId, text=self.userName+'閉嘴\n秒速'+"{0:.2f}".format(userF)+'則訊息，很快嘛ㄏㄏ')

            self.messageSet=[msgTop]
            return True
        return False
        
def ban(msg,bot):
    if '@ban' in msg.text:
        