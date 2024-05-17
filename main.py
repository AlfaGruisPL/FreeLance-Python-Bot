import requests
from bs4 import BeautifulSoup
import time, threading
import functools
import sched
import asyncio
from telegram import Bot
import re

from tinydb import TinyDB, Query, where
global db
db = TinyDB('ordersDB.json')
global freelanceUA
freelanceUA = db.table('freelanceUA')
TOKEN = '7001102698:AAEvTBq0Iuqzk23h4EMnABd-f2S6S3Xkfd0'
CHANNEL_ID = '-1002042541420'
#CHANNEL_ID = '-1002070856386'
#CHANNEL_ID = '1221345107'

from datetime import datetime
global botObj
bot = Bot(token=TOKEN)

async def send_message(message, retries=5):
    bot = Bot(token=TOKEN)

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    if now.hour >= 23 and now.hour < 9:
        print("Bot is sleeping đź´, Current time:", current_time)
    else:
        for attempt in range(retries):
            try:
                # WysĹ‚anie wiadomoĹ›ci przez bota
                await bot.send_message(chat_id=CHANNEL_ID, message_thread_id=10,text=message, disable_web_page_preview=True)
                print("Message sent successfully at:", current_time)
                break  # Przerwij pÄ™tlÄ™ jeĹ›li wysyĹ‚ka siÄ™ powiodĹ‚a
            except Exception as e:
                print(f"Error occurred while sending message (attempt {attempt + 1}): {e}")
                if attempt == retries - 1:
                    print("Max retries reached. Unable to send message.")


async def updateStatus(message):
    bot = Bot(token=TOKEN)
    try:
        await bot.editMessageText(chat_id=CHANNEL_ID,message_id=103,text=message)
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print("Message edit successfully at:", current_time)
    except Exception as e:
        print("Error occurred while edit message:", e)


s = sched.scheduler(time.time, time.sleep)
def setInterval(sec):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*argv, **kw):
            setInterval(sec)(func)
            func(*argv, **kw)
        s.enter(sec, 1, wrapper, ())
        return wrapper
    s.run()
    return decorator


def check():
    try:

        now = datetime.now()
        current_time = now.strftime("%H:%M")
        if now.hour >= 23 or now.hour < 9:
            if now.hour == 8:
                asyncio.run(updateStatus("Bot je Ĺ›niadanie đźŚ­  Czas: " + current_time))
                print("Bot is eatingđź´ Current time:", current_time)
                return
            if now.hour == 23:
                asyncio.run(updateStatus("Bot je kolacje đźŚ­  Czas: " + current_time))
                print("Bot is eatingđź´ Current time:", current_time)
                return
            asyncio.run(updateStatus("Bot Ĺ›pi đź´ Czas: "+ current_time))
            print("Bot is sleepingđź´ Current time:", current_time)
            return
        if now.hour == 12:
            asyncio.run(updateStatus('Bot je obiad đźĄ—: ' + current_time))
        else:
            asyncio.run(updateStatus('Ostatnie sprawdzenie: '+current_time +'đź€'))
        URL = "https://freelance.ua/orders/?orders=sajt-pod-kljuch%2Conline-shops%2Crefinement-sites%2Cverstka%2Cwap-pda-sites%2Cusability&pc=1"
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        headers = soup.find_all("header", class_="l-project-title")

        for header in headers:
            now = datetime.now()
            a = header.find("a")
            id_match = re.search('\/\d+\-', a.get('href'))
            string = str(id_match.group(0)).replace('/','').replace("-",'')
            isFind = len(freelanceUA.search(where('orderId') == string)) != 0
            if isFind == False:
                freelanceUA.insert({'orderId':string})
                print('nowe zlecenia---------------------'+ current_time)
                print(a.text)
                mess = ''
                mess = mess + '------------------'+current_time+ '------------------'
                mess = mess + '\nNowe zlecenie, https://freelance.ua: '
                mess = mess + '\n'+a.text
                mess = mess + '\n'+a.get('href')
                asyncio.run(send_message(mess))
                time.sleep(1)
            else:
                print(".")
    except Exception as e:
        print("WystÄ…piĹ‚ wyjÄ…tek:", e)
check()

@setInterval(sec=80)
def testInterval():
    check()
testInterval()

