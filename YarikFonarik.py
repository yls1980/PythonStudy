#!pip install googletrans
# функция переводчик
import re
import logging
from googletrans import Translator

def ftranslator(vstr):
    translator = Translator()
    #pl = re.findall('[A-Z][a-z]*', vstr)
    #spl = vstr
    #f_n = " ".join(spl)
    dest = langDetect(vstr)
    if dest=="ru":
        dest="en"
    else:
        dest = "ru"
    #translated = translator.translate(vstr, src='en', dest=dest)
    translated = translator.translate(vstr, dest=dest)
    return translated.text


from gtts import gTTS
import re
import os
from textblob import TextBlob

def langDetect(sText):
    b = TextBlob(sText)
    res = b.detect_language()
    if res not in ['ru','en']:
        res = re.search(r'[А-Яа-я]{1,}',sText)
        if res!= None:
            res = 'ru'
    if res!='ru':
        res = 'en'
    return res

#import playsound
def Speaker (sText):
    language = langDetect(sText)
    speech = gTTS(text=sText, lang=language, slow=False)
    try:
        spath = os.path.join(os.environ['HOME'], "text.mp3")
    except:
        spath = "text.mp3"

    try:
        speech.save(spath)
        return spath
    except Exception as e:
        logging.error(e)
        return ""


def MyBot(wrd, user_data):
    res="Ёпта..."+wrd+"- не переводится"
    try:
        res = "Перевод: " + ' - ' + ftranslator(wrd)
    except Exception as e:
        logging.error(e)
    return res

import telebot;
from telebot import types
bot = telebot.TeleBot('801584528:AAGzwxntxlRDufHPwJPWqOAbDg6DPv2m_oo');

#@bot.message_handler(commands=["geo"])
def geo(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_geo = types.KeyboardButton(text="Отправить местоположение", request_location=True)
    keyboard.add(button_geo)
    bot.send_message(message.chat.id, "Привет! Нажми на кнопку и передай мне свое местоположение", reply_markup=keyboard)

@bot.message_handler(content_types=["location"])
def location(message):
    if message.location is not None:
        sMess = "Широта: %s; Долгота: %s" % (message.location.latitude, message.location.longitude)
        logging.info(sMess)
        bot.send_message(message.chat.id, sMess)

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    ruWord = message.text
    ud = bot.get_me()
    try:
        s1 = int(ruWord[0])
    except:
        s1 = -1000
    if s1 == 0:
        #Говорилка
        vText = ruWord[1:]
        mp3Path = Speaker(vText)
        if mp3Path != "":
            audio = open(mp3Path, 'rb')
            bot.send_audio(message.from_user.id, audio)
        else:
            bot.send_message(message.from_user.id, "Не могу прочитать.")
    elif s1==1:
        geo(message)
    else:
        #переводчик
        enWord = MyBot(ruWord, ud)
        bot.send_message(message.from_user.id, enWord)

logging.basicConfig(filename='tBot.log', filemode='w', format = u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', level = logging.INFO)
bot.polling(none_stop=True, interval=0)