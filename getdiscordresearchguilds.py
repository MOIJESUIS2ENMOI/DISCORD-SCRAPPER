import random
import requests
import base64
import json
import random
import threading
import time
import os
import sys
import xlwt
from colorama import Fore
from datetime import datetime

def request_cookie():
    response1 = requests.get("https://discord.com")
    cookies = response1.cookies.get_dict()
    dcfduid = cookies.get('__dcfduid')
    sdcfduid = cookies.get('__sdcfduid')
    return dcfduid, sdcfduid

def getSuperproperties(data):
    poperties = base64.b64encode(json.dumps(data).encode()).decode()
    return poperties

def getkeywordServers(keyword, proxiesList):
    url = f"https://nktzz4aizu-dsn.algolia.net/1/indexes/prod_discoverable_guilds/query?x-algolia-agent=Algolia+for+JavaScript+%284.1.0%29%3B+Browser"
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate, br',
        'x-algolia-api-key': 'aca0d7082e4e63af5ba5917d5e96bed0',
        'x-algolia-application-id': 'NKTZZ4AIZU',
        "Content-Length": "140",
        'content-type': 'application/x-www-form-urlencoded',
        'Origin': 'https://discord.com',
        'Connection': 'keep-alive',
        'Referer': 'https://discord.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
    }
    
    data ={
        "query":"nft",
        "filters":"auto_removed:false AND approximate_presence_count> 0 AND approximate_member_count>200",
        "optionalFilters":["preferred_locale: en-US"],
        "length":12,
        "offset":12,
        "restrictSearchableAttributes":["name","description","keywords","categories.name","categories.name_localizations.en-US","primary_category.name","primary_category.name_localizations.en-US","vanity_url_code"]
    }
    
    proxie = { # use the proxies
        "http": f"https://{random.choice(proxiesList)}",
        "https": f"https://{random.choice(proxiesList)}"
        }
    
    proxies = None
    r = requests.post(url, headers=headers, data=json.dumps(data))
    print(r.json())
    jsoni = r.json()
    nbserver = r.json()["nbHits"]
    serverScrapped = 0
    while serverScrapped < nbserver:
        server_data = jsoni['hits']
        for guild_data in server_data:
            guild_id = guild_data['id']
            vanity_url_code = guild_data['vanity_url_code']
            if vanity_url_code is not None:
                joinServerGuildId(token, guild_id, proxies, invite=vanity_url_code)
            else:
                joinServerGuildId(token, guild_id, proxies, invite=None)
        serverScrapped = serverScrapped + 12
        
    
def joinServerGuildId(token, guild_id, proxies, invite):
    url = f'https://discord.com/api/v9/guilds/{guild_id}/members/@me'

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
        "client_build_number":  149043,
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

    dcfduid, sdcfduid = request_cookie()
    headers["cookie"]= f"__dcfduid={dcfduid}; __sdcfduid={sdcfduid}; locale=en-US"
    try:
        r = requests.put(url, headers=headers, proxies=proxies, json={}, timeout=10)
    except:
        r = requests.put(url, headers=headers, proxies=proxies, json={}, timeout=10) 
    if r.status_code == 200:
        if invite is not None:
            getInviteData(invite, token, proxies)
        else:
            pass
            url = f'https://discord.com/guilds/{guild_id}/channels'
            r = requests.get(url, headers=headers, proxies=proxies)
            print(r.content)
            invite = getInvite(token, channel_id, proxies)
            getInviteData(invite, token, proxies)
    
def getInviteData(invite, token, proxies):
    
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
        url = f"https://discord.com/api/v9/invites/{invite}?inputValue={invite}&with_counts=true&with_expiration=true"
        r = requests.get(url, headers, proxies=proxies, timeout = 20)
        if r.status_code == 404:
            print("Invalid Invite!")
            exportUnknownInvites(invite)
            return True
        elif r.status_code == 401:
            print("Invalid Token")
            print(r.status_code)
            return False
        elif r.status_code == 429:
            print("ratelimited!")
            print(r.status_code)
            print("waiting 1 minute")
            time.sleep(60)
            return False
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
            
            exportDataToDb(guild_name, invite_code, expires_at, member_count, presence_count, guild_id, guild_icon, guild_banner, guild_description, verification_level, invite_channelid, invite_channelname, inviter_id, inviter_name, inviter_avatar)
            return True
        else:
            print("Unknown error")
            print(r.status_code)
            return False
    except Exception as err:
        print("Invalid Invite!")
        exportUnknownInvites(invite)

def exportDataToDb(guild_name, invite_code, expires_at, member_count, presence_count, guild_id, guild_icon, guild_banner, guild_description, verification_level, invite_channelid, invite_channelname, inviter_id, inviter_name, inviter_avatar):
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
            
def getInvite(token, channel_id, proxies):
    url = f"https://discord.com/api/v9/channels/{channel_id}/invites"
    
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
    
    rdata = {
        "max_age":0,
        "max_uses":0,
        "temporary":False,
    }
    
    r = requests.post(url, headers=headers, data=json.dumps(rdata), proxies=proxies)
    if r.status_code == 200:
        invite = r.json()["code"]
        return invite
    else:
        print (r.status_code)
        print (r.content)
        
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
        if r.status_code == 400:
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
        
def getproxies():
    proxieslist = [] 
    with open('proxies.txt','r') as handle:
        proxies = handle.readlines()
        for x in proxies:
            proxieslist.append(x.rstrip())
    return proxieslist
      
token = "OTY0OTY0MjIxMDI2NzE3NzM2.YlxJng.RV45kc6nmY5CzigOixGl_So0kSI"
keyworklist = ['nft', 'NFT', 'nfts', 'NFTS', 'crypto', 'cryptocurrency', 'art', 'investis']
proxylist = getproxies()
getkeywordServers("nft", proxylist)