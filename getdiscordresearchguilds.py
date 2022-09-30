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

def getkeywordServers(keyword):
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
    
    r = requests.post(url, headers=headers, data=json.dumps(data))
    print(r.json())
    jsoni = r.json()
    nbserver = r.json()["nbHits"]
    server_data = jsoni['hits']
    for guild_data in server_data:
        guild_id = guild_data['id']
        guild_name = guild_data['name']
        guild_description = guild_data['description']
        guild_icon = guild_data['icon']
        guild_banner = guild_data['banner']
        presence_count = guild_data['approximate_presence_count']
        member_count = guild_data['approximate_member_count']
        vanity_url_code = guild_data['vanity_url_code']
        print(guild_id, guild_name, guild_description, guild_icon, guild_banner, presence_count, member_count, vanity_url_code)
    
def joinServerGuildId(token, guild_id):
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

    dcfduid, sdcfduid = request_cookie()
    headers["cookie"]= f"__dcfduid={dcfduid}; __sdcfduid={sdcfduid}; locale=en-US"
    
    r = requests.put(url, headers=headers, json={})
    print(r.status_code)
    print(r.content)
    
    
def getInvite():
    print("todo")
    
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
        
        
token = "OTY0OTY0MjIxMDI2NzE3NzM2.YlxJng.RV45kc6nmY5CzigOixGl_So0kSI"

getkeywordServers("nft")