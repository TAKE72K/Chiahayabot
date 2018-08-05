#coding=utf-8
class key_word:
    def __init__(self,words,echo=None,prob=100,els=None,photo=None,video=None,allco=False):
        self.words=words
        self.echo=echo
        self.prob=prob
        self.els=els
        self.photo=photo
        self.video=video
        self.alloc=allco
    '''
    def find_word(words, echo=None, prob=100, els=None,photo =None, video=None, allco=False):
        # words: words need to reaction
        # echo: msg send after reaction
        # prob: probability, if not, send els msg
        # els: if not in prob
        key_words=update.message.text
        cid=update.message.chat_id
        # a random number from 0 to 99
        num = randrange(100)
        key_words_value=False
        for check in words:
            if allco == False:
                "one word correct will go"
                if key_words.find(check)!=-1:
                    key_words_value=True
            if allco == True:
                "all word correct will go"
                if key_words.find(check)!=-1:
                    key_words_value=True
                else:
                    key_words_value=False
                    break
        if echo != None:
            if key_words_value==True and num<prob:
                bot.send_message(chat_id=cid,text=echo)
                yuunou(bot,update)
            if key_words_value==True and num>=prob and els!=None:
                bot.send_message(chat_id=cid,text=els)
                yuunou(bot,update)
        elif video != None:
            if key_words_value==True and num<prob:
                bot.send_video(chat_id=cid, video=video)
                yuunou(bot,update)
        elif photo != None:
            if key_words_value==True and num<prob:
                bot.send_photo(chat_id=cid, photo=photo)
                yuunou(bot,update)
        return key_words_value
        '''