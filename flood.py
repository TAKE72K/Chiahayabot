from datetime import datetime as dt
from datetime import timedelta as td
from functools import wraps
import telegram

listFloodLimit=[]
class FloodLimit:
    
    def __init__(self,msgInit,banF=1,restrictT=60,threshold=3):
        self.messageSet=[]
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
        print('cre'+self.userName+str(msgReco))
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
        print('det'+self.userName+str(msgReco))
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
            if deltaT<60 and deltaT>=self.threshold:
                t=deltaT
                timeL=True
                self.messageSet.insert(0,btm)
            if deltaT<self.threshold:
                timeL=True
                self.messageSet.insert(0,btm)
                return
        #check frequence
        floodBan=False
        userF=len(self.messageSet)/t
        print(self.userName+str(userF))
        if userF>self.frequence:
            floodBan=True
        #ban user
        if floodBan:
            print(self.userName)
            print(self.messageSet)
            bot.restrict_chat_member(self.chatId,self.userId,
            until_date=dt.now()+td(0,self.restrictT,0),
            can_send_messages=False, can_send_media_messages=False,
            can_send_other_messages=False)
            bot.send_message(chat_id=self.chatId, text=self.userName+'閉嘴\n秒速'+"{0:.2f}".format(userF)+'則訊息，很快嘛ㄏㄏ')

            self.messageSet=[msgTop]
            return True
        return False
def floodDec(funct):
    global listFloodLimit
    ban=False
    for i in listFloodLimit:
        retu=i.detectMsg(update.message,bot)
        if retu:
            ban=True
    if not ban:
        a=FloodLimit(update.message)
        listFloodLimit.append(a)
    return funct
def ban(msg,bot):
    if '@ban' in msg.text:
        day=msg.text.replace('@ban')
        day=int(day)
        