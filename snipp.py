def dice(bot,update,args):
    """Send a message when the command /dice is issued."""
    dice=['?','?','?','?','?','?']
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
            if num>100:
                return
            else:
                for i in range(0,num):
                    j=randrange(6)
                    text=text+dice[j]
                    count[j]=count[j]+1
                msg=bot.send_message(chat_id=update.message.chat_id, text=text)
                text=''
                for i in range(0,6):
                    text=text+dice[i]+str(count[i])+'­Ó\n'
                if num>20:
                    msg1=bot.send_message(chat_id=update.message.chat_id, text=text)
                    time.sleep(5)
                    bot.delete_message(chat_id=update.message.chat_id, message_id=msg.message_id)
                    bot.delete_message(chat_id=update.message.chat_id, message_id=msg1.message_id)