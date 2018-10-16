from datetime import datetime as dt
from datetime import timedelta as td
import telegram
class FloodLimit:
    
    def __init__(self,msgInit,banF=0.5):
        self.messageSet=[]
        self.userId=msgInit.from_user.id
        self.userName=msgInit.from_user.first_name
        self.chatId=msgInit.chat.id
        self.frequence=banF
        
        date=msgInit.date
        msgId=msgInit.message_id
        msgReco={'date':date,
                'msgId':msgId}
        self.messageSet.append(msgReco)
    def detectMsg(self,msg,bot):
        if msg.from_user.id != self.userId:
            return False
        if msg.chat.id !=self.chatId:
            return False
        
        date=msg.date
        msgId=msg.message_id
        msgReco={'date':date,
                'msgId':msgId}
        self.messageSet.append(msgReco)
        
        ban=self.floodCheck(msgReco,bot)
        return True
    def floodCheck(self,msgTop,bot):
        timeL=False
        t=0
        #check time ligal
        while not timeL:
            btm=self.messageSet.pop(0)
            deltaT=(msgTop['date']-btm['date']).total_seconds()
            if deltaT<60 and deltaT>=1:
                t=deltaT
                timeL=True
                self.messageSet.insert(0,btm)
            if deltaT<3:
                timeL=True
                self.messageSet.insert(0,btm)
                return
        #check frequence
        floodBan=False
        userF=len(self.messageSet)/t
        if userF>self.frequence:
            floodBan=True
        #ban user
        if floodBan:
            bot.restrict_chat_member(self.chatId,self.userId,
            until_date=dt.now()+td(0,32,0),
            can_send_messages=False, can_send_media_messages=False,
            can_send_other_messages=False)
            bot.send_message(chat_id=self.chatId, text=self.userName+'閉嘴')

            self.messageSet=[msgTop]
            return True
        return False