import requests
import hrequests
from bs4 import BeautifulSoup
import os
import configparser
from .Prettify import Prettify
from .configGenerator import create_default_config
from requests.packages.urllib3.exceptions import InsecureRequestWarning #type: ignore
import urllib3

CONFIG_FILE = "libread-config.ini"
global DOMAIN_NAME
global SEARCH_PAGE_SELECTOR, STATUS_SELECTOR_I, STATUS_SELECTOR_II, STATUS_SELECTOR_III, CHAPTER_SELECTOR, IMAGE_URL_SELECTOR, ARTICLE_DIV_SELECTOR
global HEADERS

printWar = Prettify.printWar
printSuc = Prettify.printSuc
printErr = Prettify.printErr


def _readConfig():
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    if(os.path.isfile(CONFIG_FILE)):
        try:
            config = configparser.ConfigParser()
            config.read(CONFIG_FILE)

            global SEARCH_PAGE_SELECTOR, STATUS_SELECTOR_I, STATUS_SELECTOR_II, STATUS_SELECTOR_III, CHAPTER_SELECTOR, IMAGE_URL_SELECTOR, ARTICLE_DIV_SELECTOR
            SEARCH_PAGE_SELECTOR = config.get("SELECTOR_MAPS", "searchResultSelector")
            STATUS_SELECTOR_I = config.get("SELECTOR_MAPS", "statusSelectorI")
            STATUS_SELECTOR_II = config.get("SELECTOR_MAPS", "statusSelectorII")
            STATUS_SELECTOR_III = config.get("SELECTOR_MAPS", "statusSelectorIII")
            CHAPTER_SELECTOR = config.get("SELECTOR_MAPS", "totalChaptersSelector")
            IMAGE_URL_SELECTOR = config.get("SELECTOR_MAPS", "coverImageDivSelector")
            ARTICLE_DIV_SELECTOR = config.get("SELECTOR_MAPS", "articleDivSelector")

            global HEADERS
            HEADERS = {
                'authority': config.get("DOMAIN", "authority"),
                'User-Agent' : config.get("DOMAIN", "userAgent"),
                'origin': config.get("DOMAIN", "origin"),
                'referer': config.get("DOMAIN", "referer")}
            
            global DOMAIN_NAME
            DOMAIN_NAME = config.get("DOMAIN", "domainName")

        except:
            printWar("Corrupted config file detected! Re-generating a new one...")
            create_default_config(CONFIG_FILE)
            _readConfig()
    else:
        create_default_config(CONFIG_FILE)
        _readConfig()
    

def checkConnection():
    _readConfig()
    url = f"https://{DOMAIN_NAME}/"
    try:
        con = requests.get(url, timeout=10, verify=False)
        if(con.status_code == 200):
            return True
        else:
            print("Connection established with Status code " + con.status_code)
            return False
    except:
        return False

def search(query: str):
    _readConfig()

    payload = {"searchkey": query}
    res = requests.post(f"https://{DOMAIN_NAME}/search", data=payload, headers=HEADERS, verify=False)
    soup = BeautifulSoup(res.content, 'html.parser')

    #For Debugging purposes
    with open("searchResultDump.html", 'w', encoding='utf-8') as f:
        f.write(res.content.decode())
    
    results = soup.select(SEARCH_PAGE_SELECTOR)
    return results

def getMetadata(url: str):
    _readConfig()

    try:
        res = requests.get(url, headers=HEADERS, verify=False)
    except:
        try:
            res = requests.get(url, headers=HEADERS)
        except Exception as E:
            printErr(f"Error occured while fetching {url}. | Error: {E} |")
    soup = BeautifulSoup(res.content, 'html.parser')

    #For Debugging purposes
    with open("novelPageDump.html", 'w', encoding='utf-8') as f:
        f.write(res.content.decode())

    metadata = {'chapters': [], 'status' : None, 'cover-image': None}
    
    chapters = soup.select(CHAPTER_SELECTOR)
    metadata.update({'chapters' : chapters})
    status = "Unknow"
    try:
        status = soup.select(STATUS_SELECTOR_I)[0].text
    except:
        try:
            status = soup.select(STATUS_SELECTOR_II)[0].text
        except:
            try:
                status = soup.select(STATUS_SELECTOR_III)[0].text
            except:
                pass

    metadata.update({'status' : status})

    try:
        imageUrl = f"https://{DOMAIN_NAME}/" + soup.select(IMAGE_URL_SELECTOR)[0]["src"]

        image = requests.get(imageUrl, headers=HEADERS, stream=True)
        metadata.update({'cover-image':image})
    except:
        pass

    return metadata

def getArticle(url: str):
    _readConfig()
    
    try:
        res = hrequests.get(url, headers=HEADERS, verify=False)
    except:
        try:
            res = hrequests.get(url, headers=HEADERS)
        except Exception as E:
            printErr(f"Error occured while fetching {url}. | Error: {E} |")
        
    soup = BeautifulSoup(res.content, 'html.parser')

    #For Debugging purposes
    with open('articlePageDump.html', 'w', encoding='utf-8') as f:
        f.write(res.content.decode())
    
    articleDiv = soup.select(ARTICLE_DIV_SELECTOR)
    articleDiv = articleDiv[0:len(articleDiv)-1]
    articleStr = ""
    for article in articleDiv:
        if(article.text == "…" or article.text == "..."):
            continue
        #filter out words that can break tts
        articleStr += article.text.replace("𝙡𝓲𝒃𝓻𝓮𝙖𝒅.𝙘𝓸𝒎", "").replace("…", "").replace("...", "").replace("𝓵𝙞𝙗𝙧𝙚𝒂𝙙.𝓬𝒐𝒎", "").replace("“", "").replace("”", "").replace("𝒍𝒊𝙗𝒓𝒆𝒂𝒅.𝓬𝒐𝓶", "").replace("*", "")
        articleStr += "\n"
    return articleStr