import requests
import httpx
import random
import time
from datetime import datetime

def cleanInvite(invite):
    characters = "'!?[]{}|><~°^$£¥•\\§@#&\"€()-*%_+=;,"
    for x in range (len(characters)):
        invite = invite.replace(characters[x], "")
    return invite

def readFiles():
    i = 0
    invitesList = []
    with open("invitest.txt", 'r', encoding='utf-8') as fp:
        Lines = fp.readlines()
    for line in Lines:
        if line not in invitesList:
            print(line)
            invitesList.append(line.strip())
            invite = cleanInvite(line)
            sendDataToServer(invite)
            i = i + 1
    with open("invites2.txt", 'r', encoding='utf-8') as fp:
        Lines = fp.readlines()
    for line in Lines:
        if line not in invitesList:
            print(line)
            invitesList.append(line.strip())
            invite = cleanInvite(line)
            sendDataToServer(invite)
            i = i + 1
    with open("invites.2.txt", 'r', encoding='utf-8') as fp:
        Lines = fp.readlines()
    for line in Lines:
        if line not in invitesList:
            print(line)
            invitesList.append(line.strip())
            invite = cleanInvite(line)
            sendDataToServer(invite)
            i = i + 1
    with open("invites3.txt", 'r', encoding='utf-8') as fp:
        Lines = fp.readlines()
    for line in Lines:
        if line not in invitesList:
            print(line)
            invitesList.append(line.strip())
            invite = cleanInvite(line)
            sendDataToServer(invite)
            i = i + 1
            print(f"{i} server sent to server")
    with open("invites4.txt", 'r', encoding='utf-8') as fp:
        Lines = fp.readlines()
    for line in Lines:
        if line not in invitesList:
            print(line)
            invitesList.append(line.strip())
            invite = cleanInvite(line)
            sendDataToServer(invite)
            i = i + 1
            print(f"{i} server sent to server")
    return invitesList

def sendDataToServer(invite):
    url = "https://api.sos-epromotion.com/v1/invitesScrapper/putData/"
    
    data = {
        'exploration_date': str(datetime.today()),
        'guild_invite': invite
    }
    
    try:
        r = requests.post(url, data=data)
        if r.status_code == 200:
            if '2' in str(r.content):
                print(r.content)
                print("data already in db")
            elif '1' in str(r.content):
                print("data successfully sent to server")
            else:
                print("unknow server error")    
        elif r.status_code == 400:
            print("invalid data in request")
        elif r.status_code == 500:
            print("server error")
        else:
            print("Unknown error")
            print(r.status_code)
            print(r.content)
    except Exception as err:
        print("a client error occured")
        print(err)
            
invitesList = readFiles()

    