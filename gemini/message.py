from telegram import Bot
with open("token.bot","r",encoding="utf-8") as file:
    bot=Bot(file.read())


async def Sendmessage(chat_id, text,reply_markup=None):
    try:
        message = await bot.send_message(chat_id=chat_id, text=text, reply_to_message_id=None,parse_mode="HTML", reply_markup=reply_markup)
        msg_id = message.message_id
        return msg_id
    except Exception as e:
        print(str(e))


async def Editmessage(chat_id, text, msg_id, reply_markup=None):
    try:
        await bot.edit_message_text(chat_id=chat_id, text=text, message_id=msg_id,parse_mode="HTML", reply_markup=reply_markup)
    except Exception as e:
        pass
