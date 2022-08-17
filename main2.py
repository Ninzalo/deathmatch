import vk_api
import requests
import datetime
import time
import socket
import urllib3
from bs4 import BeautifulSoup
from vk_api.bot_longpoll import VkBotEventType, VkBotLongPoll
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from config import token_vk

vk_session = vk_api.VkApi(token=token_vk)
longpoll = VkBotLongPoll(vk_session, 207272622)

def chat_sender(id, text, keyboard=None):

    post = {
        "chat_id": id,
        "message": text,
        "random_id": 0
    }


    if keyboard != None:
        post["keyboard"] = keyboard.get_keyboard()
    else:
        post = post

    vk_session.method("messages.send", post)


while True:
    try:
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW and event.from_chat:

                msg = event.object.message['text'].lower()


                if "|онлайн|" in msg or msg == "/o" or msg == "/о":
                    id = event.chat_id
                    keyboard = VkKeyboard()
                    keyboard.add_button("|Онлайн|", color=VkKeyboardColor.PRIMARY)


                    headers = {
                                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 YaBrowser/21.8.2.381 Yowser/2.5 Safari/537.36"
                                }

                    url = "https://www.gametracker.com/server_info/46.174.49.31:27284"
                    r = requests.get(url=url, headers=headers)
                    soup = BeautifulSoup(r.text, "lxml")
                    text = ""
                    try:
                        online = soup.find("span", id="HTML_num_players").text.strip()
                        print(f"Онлайн {online}/14")
                        text = f"Онлайн на сервере - {online}/14"

                        online_players = soup.find("table", class_="table_lst table_lst_stp")
                        online_players = online_players.find_all("a")
                        names = []
                        for item in online_players:
                            name = item.text.strip()
                            names.append(f"{name}")
                            # print(name)
                        if online_players == None:
                            names = ["Игроков нет"]
                        players = ""
                        for item in names:
                            players = players + f"{item}\n"
                    except:
                        players = "Игроков нет"

                    text = f"{text}\n\n{str(players)}"

                    chat_sender(id, text, keyboard)
    except (requests.exceptions.ReadTimeout, socket.timeout, urllib3.exceptions.ReadTimeoutError, socket.gaierror, urllib3.exceptions.NewConnectionError, urllib3.exceptions.MaxRetryError, requests.exceptions.ConnectionError):
        time.sleep(1)
        print('_______Timeout______')