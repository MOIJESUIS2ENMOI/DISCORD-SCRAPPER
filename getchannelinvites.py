import requests
from colorama import Fore
import re
import os
import sys
import time
import random
import threading
import xlwt
from datetime import datetime

messagesexplored = 0
invitesfound = 0

def spoof():
    if os.name == 'nt':
        os.system("cls")
    else:
        os.system("clear")
        
def getMessages(channel_id, token, before_id):
    if before_id == "":
        url = f"https://discord.com/api/v9/channels/{channel_id}/messages?limit=100"
    else:
        url = f"https://discord.com/api/v9/channels/{channel_id}/messages?before={before_id}&limit=100"
        
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0",
        "Content-Type": "application/json",
        "Authorization": token,
        }
    try:
        r = requests.get(url, headers=headers)
        json = r.json()
        if json != {}:
            global messagesexplored
            messagesexplored = messagesexplored + 100
            return extractInformations(json, before_id)
        else:
            return None
    except:
        r = requests.get(url, headers=headers)
        json = r.json()
        if json != {}:
            messagesexplored = messagesexplored + 100
            return extractInformations(json, before_id)
        else:
            return None
    
def getExportedList():
    try:
        file = open('invites.txt', 'r', encoding='utf-8')
        text = file.read()
        file.close()
        return text
    except Exception as err:
        print(err)
    
def extractInformations(messageData, before_id):
    id = before_id
    content = ""
    try:
        for jsoni in (messageData):
            id = jsoni['id']
            content = jsoni['content']
            #print(f"--------------------------------------------------------------------------------------------------------------------------------")
            #print(f"Message id: {id}")
            #print(f"Message content: {content[:25]}...")
            #print(f"Message author: {author}")
            #print(f"Message sent date: {date}")
            
            extractInvite(clearContent(content))
        return id
    except Exception as err:
        return id

def clearContent(content):
    try:
        content = str(content).replace("(", " ")
        content = str(content).replace(")", " ")
        content = str(content).replace(",", " ")
        content = str(content).replace(" ", " ")
        content = str(content).replace("\'", " ")
        content = str(content).replace("[", " ")
        content = str(content).replace("]", " ")
        #print("content cleaned!")
        return content
    except Exception as err:
        print("An error occurred while cleaning the content!")
    
def extractInvite(content):
    inviteList = getUrl(content)
    for invite in inviteList:
        #print("invite loop start")
        try:
            invite = str(invite).replace("(", "")
            invite = str(invite).replace(")", "")
            invite = str(invite).replace(",", "")
            invite = str(invite).replace(" ", "")
            invite = str(invite).replace("\'", "")
            invite = str(invite).replace("[", "")
            invite = str(invite).replace("]", "")
            #print("invite cleaned!")
            if "discord" in invite and len(invite) < 50:
                #print(f"Message links: Invite Found:{invite}!")
                if invite not in inviteListFound:
                    inviteListFound.append(invite)
                    global invitesfound
                    invitesfound = invitesfound + 1
                    exportInvite(invite)
                    sendDataToServer(invite)
                
                    #print(f"Message links: Link already found in this channel...")
            
                #rint(f"Message links: Link is not an invite: {invite}")
        except Exception as err:
            print("An error occured while cleaning the invite...")
            print(err)

def getUrl(string):
    #print("url start")
    try: 
        regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
        url = re.findall(regex,string)
        #print("url end")
        return url
    except Exception as err:
        print("An error occured while extracting invites, skiping")
        return ""

def exportInvite(invite):
    #print("start export invite")
    try:
        file = open('invites.txt', 'a', encoding="utf-8")
        file.write(f'{invite}\n')
        file.close()
    except Exception as err:
        print(f"{Fore.YELLOW} [!]==> An error occured while writing to the file, retrying...{Fore.RESET}")
        try:
            file = open('invites.txt', 'a')
            file.write(f'{invite}\n')
            file.close()
        except Exception as err:
            print(f"{Fore.LIGHTRED_EX} [x]==> An error occured while writing to the file, skiping...{Fore.RESET}")
            print(f"{Fore.LIGHTRED_EX}          ⮡ Error: {err}{Fore.RESET}")
            
def sendDataToServer(invite):
    url = "https://api.sos-epromotion.com/v1/invitesScrapper/putData/"
    
    data = {
        'exploration_date': str(datetime.today()),
        'guild_invite': invite
    }
    
    try:
        r = requests.post(url, data=data)
        '''
        if r.status_code == 200:
            if '2' in str(r.content):
                print(r.content)
                print("data already in db")
            elif '1' in str(r.content):
                print("data successfully sent to server")
            else:
                print("unknow server error")    
        if r.status_code == 400:
            print("invalid data in request")
        elif r.status_code == 500:
            print("server error")
        else:
            print("Unknown error")
            print(r.status_code)
            print(r.content)
            '''
    except Exception as err:
        print("a client error occured")
        print(err)

def startaScrape(channel_id, before_id, token, alpha):
    i = 0
    try:
        myfile = open(f'save/{channel_id}', 'r')
        before_id = myfile.read()
    except Exception as err:
        before_id = ''
    while before_id != None:
        before_id = getMessages(channel_id, token, before_id)
        myfile = open(f'save/{channel_id}', 'w+')
        myfile.write(before_id)
        myfile.close()
        i = i + 100
        if alpha :
            sys.stdout.write(f"{Fore.LIGHTGREEN_EX}\rINVITES DISCOVERED: {invitesfound} | MESSAGES EXPLORED: {messagesexplored} | ACTIVE CHANNEL SCRAPE: {threading.active_count()}{Fore.RESET}")
            sys.stdout.flush()
        
    print(f"All messages where scapped in {channel_id}, found {len(inviteListFound)} invites!")
    print(f"Invites Found:\n\n{getExportedList()}")

invitesList = []
inviteListFound = []
channel_ids = ["892124683397373972", "823193298663505931", "951806635444146286", "862702853348917269", "957199228071989319", "898309173211725825", "950037144594948120", "915450629449728010", "937503665458131004", "937461024083279933", "952661093786992650", "961334238903431249", "923242029172011049", "936404837015359528", "922900609231888454", "957811276724178974", "890451455314653194", "896518266841890817", "952969773724078201", "948625881281220679", "950037144594948120", "915450629449728010", "950705363190169634", "937503665458131004", "937461024083279933", "954655972654194688"] #
before_id = ""
token = "OTY0OTY0MjIxMDI2NzE3NzM2.YlxJng.RV45kc6nmY5CzigOixGl_So0kSI"
i = 0

for channel_id in channel_ids:
    if threading.active_count() >= 1:
        alpha = True
    else:
        alpha = False
    threading.Thread(target= startaScrape, args=(channel_id, before_id, token, alpha)).start()


