import subprocess
import re
import os
import configparser
from .configGenerator import create_default_config
from .Prettify import Prettify, clearLine
from .twoSecondSilence import getFileBytes
import music_tag

printSuc = Prettify.printSuc
printWar = Prettify.printWar
printErr = Prettify.printErr
printFeaturedText = Prettify.printFeaturedText

CONFIG_FILE = "libread-config.ini"
global EMBED_SUBS

def _sorted_alphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(data, key=alphanum_key)

def _readConfig():
    if(os.path.isfile(CONFIG_FILE)):
        try:
            config = configparser.ConfigParser()
            config.read(CONFIG_FILE)
            global EMBED_SUBS
            EMBED_SUBS = config.getboolean("TTS_CONFIG", "embedSubtitles")
        except:
            printWar("Corrupted config file detected! Re-generating a new one...")
            create_default_config(CONFIG_FILE)
            _readConfig()
    else:
        create_default_config(CONFIG_FILE)
        _readConfig()

def performSanityCheck() -> bool:
    try:
        result = subprocess.check_output(["ffmpeg", "-version"]).decode()
    except:
        printFeaturedText(msg="FFMPEG not found in the path! LibRead-Tool will download all articles before converting them.")
        return False
    
    ffmpegVersion = re.search("ffmpeg version (.*) Copyright", result).group(1)
    printSuc(f"FFMPEG version {ffmpegVersion} found!")
    return True

# Will merge all mp3 files into one and embed the subtitles from subs.txt
def mergeChunks(chunkFilesDir: str, outputFilePrefix: str, coverImagePath = None) -> None:
    _readConfig()

    allMP3Files = _sorted_alphanumeric([f for f in os.listdir(chunkFilesDir) if (os.path.isfile(os.path.join(chunkFilesDir, f)) and (f.split(".")[-1] == "mp3"))])

    with open(f'{chunkFilesDir}/2s-delay.mp3', 'wb') as df:
        df.write(getFileBytes())

    ffmpegfileList = "".join(f"file '{f}'\nfile '2s-delay.mp3'\n" for f in allMP3Files)

    with open(f'{chunkFilesDir}/inputFiles.txt', 'w', encoding="utf=8") as cf:
        cf.write(ffmpegfileList)
    
    retCode = os.system(f'ffmpeg -f concat -safe 0 -i "{chunkFilesDir}/inputFiles.txt" -c copy -map_metadata 0 "{outputFilePrefix}.mp3" -loglevel panic')
    if(retCode != 0):
        clearLine()
        printErr(f"Merge Error occured! FFMPEG ReturnCode: {str(retCode)}")
        return
    
    # Add ID3 tags
    f = music_tag.load_file(f'{outputFilePrefix}.mp3')

    if(EMBED_SUBS):
        with open(f"{chunkFilesDir}/subs.txt", 'r', encoding="utf-8") as sf:
            f["lyrics"] = sf.read()
    
    if(coverImagePath):
        with open(coverImagePath, 'rb') as If:
            f["artwork"] = If.read()
    
    f.save()