import sys
import os
import random
import requests 
import time
from colorama import Fore
import base64
import json
import xlwt
from datetime import datetime

def readFile():
    with open("invites.txt", 'r', encoding='utf-8') as fp:
        Lines = fp.readlines()
    for line in Lines:
        invitesList.append(line.strip())
    return invitesList
    
def exportUnknownInvites(invite):
    try:
        file = open('invitesInvalid.txt', 'a', encoding="utf-8")
        if len(invite) < 8:
            file.write(f'{invite}\n')
        else:
            file.write(f'https://discord.gg/{invite}\n')
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
            
def exportDataToXls(guild_name, invite_code, expires_at, member_count, presence_count, guild_id, guild_icon, guild_banner, guild_description, verification_level, invite_channelid, invite_channelname, inviter_id, inviter_name, inviter_avatar, i):
    sheet.write(i, 0, str(datetime.today()))
    sheet.write(i, 1, guild_name)
    sheet.write(i, 2, invite_code)
    sheet.write(i, 3, expires_at)
    sheet.write(i, 4, member_count)
    sheet.write(i, 5, presence_count)
    sheet.write(i, 6, guild_id)
    sheet.write(i, 7, guild_icon)
    sheet.write(i, 8, guild_banner)
    sheet.write(i, 9, guild_description)
    sheet.write(i, 10, verification_level)
    sheet.write(i, 11, invite_channelid)
    sheet.write(i, 12, invite_channelname)
    sheet.write(i, 13, inviter_id)
    sheet.write(i, 14, inviter_name)
    sheet.write(i, 15, inviter_avatar)

def getInviteFromDb():
    url = "https://api.sos-epromotion.com/v1/invitesScrapper/getData/"
    try:
        r = requests.post(url)
        if r.status_code == 200:
            if '1' in str(r.content):
                print("No data in db")
                return False, None
            else:
                print(f"invite rec: {r.content}")
                return True, str(r.content)
        elif r.status_code == 500:
            print("SERVER internal error")
            return False, None
        else:
            print("Unknown error")
            print(r.status_code)
            print(r.content)
            return False, None
    except Exception as err:
        return False, None
        
def deleteInviteFromDb(invite):
    url = "https://api.sos-epromotion.com/v1/invitesScrapper/deleteData/"
    data = {
        'guild_invite' : invite
    }
    try:
        r = requests.post(url, data=data)
        if r.status_code == 200:
            print(r.content)
            if '1' in str(r.content):
                print("Data successfully deleted in db")
            elif '2' in str(r.content):
                print("Error while deleting data in server part")
            else:
                print("An unknown error occurred")
        elif r.status_code == 500:
            print("SERVER internal error")
        else:
            print("Unknown error")
            print(r.status_code)
            print(r.content)
            
    except Exception as err:
        print("a client error occurred")
    
def exportDataToDb(guild_name, invite_code, expires_at, member_count, presence_count, guild_id, guild_icon, guild_banner, guild_description, verification_level, invite_channelid, invite_channelname, inviter_id, inviter_name, inviter_avatar, i):
    url = "https://api.sos-epromotion.com/v1/invitesDataScrapper/simpleInvite/putData/"
    
    data = {
        'exploration_date': str(datetime.today()),
        'guild_name' : guild_name,
        'guild_invite': invite_code,
        'expiration_date': expires_at,
        'guild_members_count': member_count,
        'guild_members_online': presence_count,
        'guild_id': guild_id,
        'guild_icon': guild_icon,
        'guild_banner': guild_banner,
        'guild_description': guild_description,
        'verification_level': verification_level,
        'invite_channel_id': invite_channelid,
        'invite_channel_name': invite_channelname,
        'inviter_id': inviter_id,
        'inviter_name': inviter_name,
        'inviter_avatar': inviter_avatar
    }

    try:
        r = requests.post(url, data=data)
        if r.status_code == 200:
            if '1' in str(r.content):
                print("Data successfully sent to the server!")
            else:
                print("Data already in the server !")
        if r.status_code == 400:
            print("Bad request!")
        if r.status_code == 500:
            print("Server internal error!")
    except Exception as err:
        r = requests.post(url, data=data)
        if r.status_code == 200:
            print("invite successfully sent to the server!")
        if r.status_code == 400:
            print("Bad request!")
        if r.status_code == 500:
            print("Server internal error!")
        
def cleanInvite(invite):
    characters = "'!?[]{}|><~°^$£¥•\\§@#&\"€()-*%_+=;,"
    for x in range (len(characters)):
        invite = invite.replace(characters[x], "")
    return invite

def softClean(invite):
    if "\\n" in str(invite):
        invite = invite[2:][:-3]+"\n"
    else:
        invite = invite[2:][:-1]
    print(invite)
    return str(invite)
 
def prepareInvite(invite):
    if "https://discord.com/invites/" in invite:
        invite = invite.replace("https://discord.com/invites/", "")
        print(invite)
        return invite
    elif "https://discord.gg/" in invite:
        invite = invite.replace("https://discord.gg/", "")
        print(invite)
        return invite
    elif "discord.gg/" in invite:
        invite = invite.replace("discord.gg/", "")
        print(invite)
        return invite
    elif "discord.com/invites/":
        invite = invite.replace("discord.com/invites/", "")
        print(invite)
        return invite
    else:
        exportUnknownInvites(invite)
        return None
        
def getSuperproperties(data):
    poperties = base64.b64encode(json.dumps(data).encode()).decode()
    return poperties

def request_cookie():
    response1 = requests.get("https://discord.com")
    cookies = response1.cookies.get_dict()
    dcfduid = cookies.get('__dcfduid')
    sdcfduid = cookies.get('__sdcfduid')
    return dcfduid, sdcfduid

def getproxies():
    proxieslist = [] 
    with open('proxies.txt','r') as handle:
        proxies = handle.readlines()
        for x in proxies:
            proxieslist.append(x.rstrip())
    return proxieslist

def getInviteData(invite, token, proxies, i):
    
    data = {
        "os":  "Windows",
        "browser":  "Firefox",
        "device":  "",
        "system_locale":  "en-US",
        "browser_user_agent":  "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0",
        "browser_version":  "102.0",
        "os_version":  "10",
        "referrer":  "",
        "referring_domain":  "",
        "referrer_current":  "",
        "referring_domain_current":  "",
        "release_channel":  "stable",
        "client_build_number":  146284,
        "client_event_source":  None
    }
    
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0',
        'Accept': '*/*',
        'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/json',
        'X-Discord-Locale': 'en-US',
        'X-Debug-Options': 'bugReporterEnabled',
        'X-Super-Properties': getSuperproperties(data),
        'Authorization': token,
        'Origin': 'https://discord.com/',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Referer': 'https://discord.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'TE': 'trailers',
    }
    try:
        dcfduid, sdcfduid = request_cookie()
        headers["cookie"]= f"__dcfduid={dcfduid}; __sdcfduid={sdcfduid}; locale=en-US"
        r = requests.get(f"https://discord.com/api/v9/invites/{invite}?inputValue={invite}&with_counts=true&with_expiration=true", headers, proxies=proxies, timeout = 20)
        if r.status_code == 404:
            print("Invalid Invite!")
            exportUnknownInvites(invite)
        elif r.status_code == 401:
            print("Invalid Token")
            print(r.status_code)
        elif r.status_code == 200:
            r = r.json()
            invite_code = r["code"]
            expires_at = r["expires_at"]
            if expires_at == None:
                expires_at = "None"
            guild_id = r["guild"]["id"]
            guild_name = r["guild"]["name"]
            guild_banner = r["guild"]["banner"]
            if guild_banner == None:
                guild_banner = "None"
            guild_icon = r["guild"]["icon"]
            guild_description = r["guild"]["description"]
            if guild_description == None:
                guild_description = "None"
            verification_level = r["guild"]["verification_level"]
            invite_channelid = r["channel"]["id"]
            invite_channelname = r["channel"]["name"]
            try:
                inviter_id = r["inviter"]["id"]
                inviter_name = r["inviter"]["username"]
                inviter_discriminator = r["inviter"]["discriminator"]
                inviter_avatar = r["inviter"]["avatar"]
            except Exception as err:
                inviter_id = "None"
                inviter_name = "None"
                inviter_discriminator = "None"
                inviter_avatar = "None"
            member_count = r["approximate_member_count"]
            presence_count = r["approximate_presence_count"]
        
            #guild
            invite_code = f"https://discord.gg/{invite_code}"
            if guild_banner != None:
                guild_banner = f"https://cdn.discordapp.com/banners/{guild_id}/{guild_banner}.webp?size=128"
            if guild_icon != None:
                guild_icon = f"https://cdn.discordapp.com/icons/{guild_id}/{guild_icon}.webp?size=128"
            #inviter
            inviter = f"{inviter_name}#{inviter_discriminator}"
            if inviter_avatar != None:
                inviter_avatar = f"https://cdn.discordapp.com/avatars/{inviter_id}/{inviter_avatar}.webp"

            print(f"==================== INVITE SCRAPPED!=====================")
            print(" ")
            print(f"---------- INVITE INFORMATIONS ----------")
            print(f"INVITE: {invite_code}")
            print(f"EXPIRATION DATE: {expires_at}")
            print(f"---------- INVITER INFORMATIONS ----------")
            print(f"INVITER ID: {inviter_id}")
            print(f"INVITER NAME: {inviter}")
            print(f"INVITER AVATAR: {inviter_avatar}")
            print(f"---------- GUILD INFORMATIONS ----------")
            print(f"ID: {guild_id}")
            print(f"NAME: {guild_name}")
            print(f"GUILD ICON: {guild_icon}")
            print(f"GUILD BANNER: {guild_banner}")
            print(f"GUILD DESCRIPTION: {guild_description}")
            print(f"GUILD VERIFICATION LEVEL: {verification_level}")
            print(f"INVITE CHANNEL ID: {invite_channelid}")
            print(f"INVITE CHANNEL NAME: {invite_channelname}")
            print(f"MEMBER COUNT: {member_count}")
            print(f"MEMBER ONLINE COUNT: {presence_count}")
            
            exportDataToXls(guild_name, invite_code, expires_at, member_count, presence_count, guild_id, guild_icon, guild_banner, guild_description, verification_level, invite_channelid, invite_channelname, inviter_id, inviter_name, inviter_avatar, i)
            exportDataToDb(guild_name, invite_code, expires_at, member_count, presence_count, guild_id, guild_icon, guild_banner, guild_description, verification_level, invite_channelid, invite_channelname, inviter_id, inviter_name, inviter_avatar, i)

        else:
            print("Unknown error")
            print(r.status_code)
    except Exception as err:
        print("Invalid Invite!")
        exportUnknownInvites(invite)
    
workbook = xlwt.Workbook()
sheet = workbook.add_sheet('invites')
sheet.write(0, 0, "EXPLORATION DATE") #datetime.today()
sheet.write(0, 1, "GUILD NAME")
sheet.write(0, 2, "GUILD INVITE")
sheet.write(0, 3, "GUILD EXPIRATION DATE")
sheet.write(0, 4, "GUILD MEMBER COUNT")
sheet.write(0, 5, "GUILD MEMBER ONLINE")
sheet.write(0, 6, "GUILD ID")
sheet.write(0, 7, "GUILD ICON")
sheet.write(0, 8, "GUILD BANNER")
sheet.write(0, 9, "GUILD DESCRIPTION")
sheet.write(0, 10, "GUILD VERIFICATION LEVEL")
sheet.write(0, 11, "INVITE CHANNEL ID")
sheet.write(0, 12, "INVITE CHANNEL NAME")
sheet.write(0, 13, "INVITER ID")
sheet.write(0, 14, "INVITER NAME")
sheet.write(0, 15, "INVITER AVATAR")

invitesList = []
token = "OTY0OTY0MjIxMDI2NzE3NzM2.YlxJng.RV45kc6nmY5CzigOixGl_So0kSI"

proxiesList = getproxies()
i = 0 
while True:
    i = i + 1
    work, invite = getInviteFromDb()
    print(invite)
    if work == True:
        if "\\n" in str(invite):
            inviteC = invite[2:][:-3]
            print("invitec"+inviteC)
        else:
            inviteC = invite[2:][:-1]
            print("invitec"+inviteC)
        inviteC = cleanInvite(inviteC)
        inviteC = prepareInvite(inviteC)
        proxie = { # use the proxies
            "http": f"https://{random.choice(proxiesList)}",
            "https": f"https://{random.choice(proxiesList)}"
            }
        proxies = None
        getInviteData(invite, token, proxies, i)
        deleteInviteFromDb(softClean(invite))
        workbook.save("invites.xls")
        wait = random.randint(2, 10)
        print(f"Waiting {wait} seconds")
        time.sleep(wait)
    else:
        time.sleep(10)
