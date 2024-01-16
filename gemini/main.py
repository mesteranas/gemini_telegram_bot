import message,app
import telegram
import gtts
import os
import langdetect
from telegram import InlineKeyboardMarkup,InlineKeyboardButton
from telegram.ext import CommandHandler,MessageHandler,filters,ApplicationBuilder,CallbackQueryHandler
import google.generativeai as genai
import PIL.Image
genai.configure(api_key="your gemini api key")
IMGModel = genai.GenerativeModel('gemini-pro-vision')
TextModel=genai.GenerativeModel('gemini-pro')

with open("token.bot","r",encoding="utf-8") as file:
    bot=ApplicationBuilder().token(file.read()).build()
async def img(update,contextt):
    info=update.effective_user
    id=await message.Sendmessage(info.id,"downloading your photo")
    path=os.path.join("cach",str(info.id))
    if not os.path.exists(path):
        os.makedirs(path)
    try:
        get=await update.message.photo[-1].get_file()
        await get.download_to_drive(path+"/photo.png")
        img=PIL.Image.open(path+"/photo.png")
        await send(update,IMGModel,img,id)
        os.remove(path+"/photo.png")
    except Exception as e:
        await message.Editmessage(info.id,"error while downloading"+str(e),id)
async def listen(update,u,contextt):
    info=u.effective_user
    path=os.path.join("cach",str(info.id))
    if not os.path.exists(path):
        os.makedirs(path)
    id=await message.Sendmessage(info.id,"converting")
    try:
        lang=langdetect.detect(update.message.text)
        re=gtts.gTTS(update.message.text,lang=lang)
        re.save(path+"/result.mp3")
        await contextt.bot.send_document(chat_id=info.id,document=open(path+"/result.mp3","rb"))
        os.remove(path+"/result.mp3")
        await contextt .bot.delete_message(chat_id=info.id,messege_id=id)
    except Exception as e:
        await message.Editmessage(info.id,"error while converting",id)

async def text(update,contextt):
    info=update.effective_user
    id=await message.Sendmessage(info.id,"generating anser for you")
    await send(update,TextModel,update.message.text,id)
async def send(update,model,data,msgId):
    info=update.effective_user
    keyboard=InlineKeyboardMarkup([[InlineKeyboardButton("listen",callback_data="Listen")]])
    try:
        response = model.generate_content(data)
        await message.Editmessage(info.id,response.text,msgId,reply_markup=keyboard)
    except:
        await message.Editmessage(info.id,"error while generating anser for you",msgId)
async def start(update,contextt):
    info=update.effective_user
    keyboard=InlineKeyboardMarkup([[InlineKeyboardButton("donate",url="https://www.paypal.me/AMohammed231")],[InlineKeyboardButton("help",callback_data="help")]])
    await message.Sendmessage(chat_id=info.id,text="welcome " + str(info.first_name) + "to this bot. this bot make you to use gemini AI tool from google.please send text message or image and i'll send it to gemini and give you result",reply_markup=keyboard)
async def helb(update,contextt):
    links="""<a href="https://t.me/mesteranasm">telegram</a>

<a href="https://t.me/tprogrammers">telegram channel</a>

<a href="https://x.com/mesteranasm">x</a>

<a href="https://Github.com/mesteranas">Github</a>

email:
anasformohammed@gmail.com

<a href="https://Github.com/mesteranas/gemini_telegram_bot">visite project on Github</a>
"""
    info=update.effective_user
    await message.Sendmessage(info.id,"""name: {}\nversion: {}\ndescription: {}\n developer: {}\n contect us {}""".format(app.name,str(app.version),app.description,app.developer,links))
async def callBake(update,contextt):
    q=update.callback_query
    await q.answer()
    if q.data=="help":
        await helb(update,contextt)
    elif q.data=="Listen":
        await listen(q,update,contextt)
print("running")
bot.add_handler(CommandHandler("start",start))
bot.add_handler(CommandHandler("help",helb))
bot.add_handler(CallbackQueryHandler(callBake))
bot.add_handler(MessageHandler(filters.TEXT,text))
bot.add_handler(MessageHandler(filters.PHOTO,img))
bot.run_polling()