import edge_tts
import os
import configparser
import re
from .Prettify import Prettify
from .configGenerator import create_default_config
import music_tag


CONFIG_FILE = "libread-config.ini"
global EMBED_SUBS
global VOICE_NAME

printWar = Prettify.printWar

def _readConfig():
    if(os.path.isfile(CONFIG_FILE)):
        try:
            config = configparser.ConfigParser()
            config.read(CONFIG_FILE)
            global VOICE_NAME
            VOICE_NAME = config.get("TTS_CONFIG", "Voice")
            global EMBED_SUBS
            EMBED_SUBS = config.getboolean("TTS_CONFIG", "embedSubtitles")
        except:
            printWar("Corrupted config file detected! Re-generating a new one...")
            create_default_config(CONFIG_FILE)
            _readConfig()
    else:
        create_default_config(CONFIG_FILE)
        _readConfig()

async def createTTSFromFile(filepath: str, outputFilePrefix: str, coverImagePath = None):
    _readConfig()

    inputFile = open(filepath, 'r', encoding='utf-8')
    communicate = edge_tts.Communicate(inputFile.read(), VOICE_NAME)
    submaker = edge_tts.SubMaker()
    with open(outputFilePrefix+".mp3", "wb") as f:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                f.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                submaker.create_sub((chunk["offset"], chunk["duration"]), chunk["text"])
    
    subs = submaker.generate_subs()
    with open(outputFilePrefix+".vtt", "w", encoding="utf-8") as sf:
        sf.write(subs)

    subs = subs.replace("""WEBVTT""", "")
    subs = re.sub("[0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{3} --> [0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{3}", "", subs)
    subs = re.sub(r'(\n\s*)+', "\n", subs)

    f = music_tag.load_file(outputFilePrefix+".mp3")

    if(EMBED_SUBS):
        f["lyrics"] = subs

    if(coverImagePath):
        with open(coverImagePath, 'rb') as img_in:
            f["artwork"] = img_in.read()
    
    f.save()

async def createTTSFromText(text: str, outputPath: str, coverImagePath = None, embedSubtitles = False):
    _readConfig()

    if(os.path.isfile(outputPath)): os.remove(outputPath)

    communicate = edge_tts.Communicate(text, VOICE_NAME)
    subFile = open(os.path.dirname(outputPath)+"/subs.txt", "a+", encoding="utf-8")
    submaker = edge_tts.SubMaker()
    
    with open(outputPath, "ab") as ttsFile:
        async for chunk in communicate.stream():
            if(chunk["type"] == "audio"):
                ttsFile.write(chunk["data"])
            elif(chunk["type"] == "WordBoundary"):
                submaker.create_sub((chunk["offset"], chunk["duration"]), chunk["text"])
    
    subs = submaker.generate_subs()
    subs = subs.replace("""WEBVTT""", "")
    subs = re.sub("[0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{3} --> [0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{3}", "", subs)
    subs = re.sub(r'(\n\s*)+', "\n", subs)
    
    subFile.write(f"{subs}\n")
    subFile.close()

    # Add ID3 tags
    f = music_tag.load_file(outputPath)
    if(embedSubtitles): f["lyrics"] = subs
    if(coverImagePath):
        with open(coverImagePath, 'rb') as img_in:
            f["artwork"] = img_in.read()
    
    f.save()