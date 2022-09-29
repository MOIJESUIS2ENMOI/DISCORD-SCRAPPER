import requests
import base64
import json

def request_cookie():
    response1 = requests.get("https://discord.com")
    cookies = response1.cookies.get_dict()
    dcfduid = cookies.get('__dcfduid')
    sdcfduid = cookies.get('__sdcfduid')
    return dcfduid, sdcfduid

def getSuperproperties(data):
    poperties = base64.b64encode(json.dumps(data).encode()).decode()
    return poperties

token = "OTY0OTY0MjIxMDI2NzE3NzM2.YlxJng.RV45kc6nmY5CzigOixGl_So0kSI"
guild_id = '982646972232126585'
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