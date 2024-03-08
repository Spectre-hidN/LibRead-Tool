import sys
import os
import shutil
import time
import asyncio
import configparser
from pynput import keyboard
from pywinctl import getActiveWindow
from utils.scrapper import checkConnection, search, getMetadata, getArticle
from utils.Prettify import clearScreen, Prettify, clearLine
from utils.tts import createTTSFromFile, createTTSFromText
from utils.configGenerator import create_default_config
from utils.ffmpegWrapper import performSanityCheck, mergeChunks

CONFIG_FILE = "libread-config.ini"

# Global varialbes. Values taken from the config file
DOMAIN_NAME = COVER_IMAGE_NAME = OUTPUT_FILE_NAME = REPLACEMENT_CHARACTER = ""
FORCE_USE_M1 = False

# global function declaration for simplicity
printInf = Prettify.printInf
printWar = Prettify.printWar
printErr = Prettify.printErr
printSuc = Prettify.printSuc
printFeaturedText = Prettify.printFeaturedText
progressBar = Prettify().progressBar

def _readConfig():
    if(os.path.isfile(CONFIG_FILE)):
        try:
            config = configparser.ConfigParser()
            config.read(CONFIG_FILE)
            global DOMAIN_NAME, COVER_IMAGE_NAME, OUTPUT_FILE_NAME, REPLACEMENT_CHARACTER, FORCE_USE_M1
            DOMAIN_NAME = config.get("DOMAIN", "domainName")
            COVER_IMAGE_NAME = config.get("NOMENCLATURES", "coverImageNomenclature")
            OUTPUT_FILE_NAME = config.get("NOMENCLATURES", "outputNomenclature")
            REPLACEMENT_CHARACTER = config.get("NOMENCLATURES", "whitespaceReplacementCharacter")
            FORCE_USE_M1 = config.getboolean("TTS_CONFIG", "forceGrabFirstThenConvert")
        except:
            printWar("Corrupted config file detected! Re-generating a new one...")
            time.sleep(2)
            create_default_config(CONFIG_FILE)
            _readConfig()
    else:
        create_default_config(CONFIG_FILE)
        _readConfig()


if __name__ == "__main__":
    if os.name == 'nt':
        os.system("title LibRead-Tool")
    else:
        os.system('echo -en "\033]0;LibRead-Tool\a"')
    
    clearScreen()

    if os.name == 'nt':
            os.system("echo \033[38;5;12m\033[0m\r")

    print("""\033[38;5;78m _        _  _      ______                     _      _______             _  \033[0m
\033[38;5;78m(_)      (_)| |    (_____ \                   | |    (_______)           | | \033[0m
\033[38;5;78m _        _ | |__   _____) ) _____  _____   __| | _____  _   ___    ___  | | \033[0m
\033[38;5;78m| |      | ||  _ \ |  __  / | ___ |(____ | / _  |(_____)| | / _ \  / _ \ | | \033[0m
| |_____ | || |_) )| |  \ \ | ____|/ ___ |( (_| |       | || |_| || |_| || | 
|_______)|_||____/ |_|   |_||_____)\_____| \____|       |_| \___/  \___/  \_)
""")
    
    _readConfig()
    print("\nChecking connection with libread...")
    time.sleep(2)
    if(checkConnection()):
        printSuc("Connection established with libread successfully!")
    else:
        printErr("Error occured while connecting to libread! Check your Internet connection or firewall settings.")
        sys.exit(100)
    
    canUseM2ForTTS = False
    if performSanityCheck():
        canUseM2ForTTS = True

    if(FORCE_USE_M1):
        canUseM2ForTTS = False

    print("\n")
    query = input("Type to search something: ")
    results = search(query=query)
    selectedIndex = -1
    if(len(results) == 0):
        printWar(f"No results found for the query '{query}'. Try any other keywords!")
        input()
        sys.exit(404)
    elif(len(results) == 1):
        printSuc(f"1 hit found for the query '{query}'. Automatically selecting it...")
        selectedIndex = 1
    else:
        printSuc(f"Multiple hits found for the query '{query}'. Select the desired index...")
        i = 0
        print("\n\033[38;5;162mIndex\033[0m  ----  \033[38;5;183mTitle\033[0m")
        for tag in results:
            print(f"\033[38;5;162m{i+1}\033[0m      ----  \033[38;5;183m{tag['title']}\033[0m") if i < 9 else print(f"\033[38;5;162m{i+1}\033[0m     ----  \033[38;5;183m{tag['title']}\033[0m")
            i+=1
        try:
            selectedIndex = int(input("Type the desired index from the above list: "))
        except:
            printErr("Invalid integer value! Aborting...")
            sys.exit(200)
        if(selectedIndex > len(results) or selectedIndex < 0):
            printWar("Index doesn't exists! Automatically selecting the last index...")
            selectedIndex = len(results) - 1
        
    selectedIndex-=1
    novelLink = f"https://{DOMAIN_NAME}" + results[selectedIndex]['href']
    print(f"\nSelected: {results[selectedIndex]['title']} || URL: {novelLink}")
    printInf(f"Getting metadata about {results[selectedIndex]['title']} from libread...")
    time.sleep(3)
    metadataResult = getMetadata(novelLink)
    totalChapters = len(metadataResult['chapters'])
    print(f"Total chapters found: \033[38;5;63m{len(metadataResult['chapters'])}\033[0m")
    print(f"Status: \033[38;5;51m{metadataResult['status']}\033[0m")
    print()
    startChapter = 1
    endChapter = totalChapters
    jump = 10
    try:
        startChapter = int(input("Mention the starting chapter [default = 1]: "))
        if(startChapter > startChapter):
            printWar("Starting chapter number exceeded total chapter found!")
            printInf("Setting starting chapter to 1...")
        else:
            printInf(f"Setting starting chapter to {startChapter}...")
    except:
        printWar("Invalid input detected!")
        printInf("Setting starting chapter to 1...")
    
    try:
        endChapter = int(input(f"Mention the last chapter [default = {totalChapters}]: "))
        if(endChapter < 1):
            printWar("Ending chapter number less than the first chapter!")
            printInf(f"Setting Ending chapter to {totalChapters}...")
        else:
            printInf(f"Setting Ending chapter to {endChapter}...")
    except:
        printWar("Invalid input detected!")
        printInf(f"Setting Ending chapter to {totalChapters}...")
    
    try:
        jump = int(input("Mention number of chapters in each part [default = 10]: "))
        if(jump > 30):
            printWar("Too many chapters detected in single part! Expect abnormal behaviour.")
    except:
        pass
    isPause = False
    pauseInput = input("Do you want to pause after each part? (y/n): ")
    isPause = True if pauseInput == "y" else False
    
    if(isPause):
        printInf("Process will pause after each part! Press 'R' to resume.")
    
    isTTS = False
    ttsInput = input("Do you want to convert text to speech? (y/n): ")
    isTTS = True if ttsInput == "y" else False

    if(isTTS):
        printInf("Texts will be converted to speech.")
    
    #Create a directory for saving the files
    if(not os.path.isdir(results[selectedIndex]['title']) and not os.path.isdir("Articles")):
            try:
                os.mkdir(results[selectedIndex]['title'])
            except:
                os.mkdir("Articles")
    
    #save cover image
    imageName = COVER_IMAGE_NAME.replace("!TITLE!", results[selectedIndex]['title']) + '.jpg'
    if(REPLACEMENT_CHARACTER != ""):
        imageName = imageName.replace(" ", REPLACEMENT_CHARACTER)
    if(metadataResult["cover-image"]!=None):
        printInf("\nSaving cover image...")
        try:
            with open(f"{results[selectedIndex]['title']}/{imageName}", 'wb') as bf:
                for chunk in metadataResult['cover-image']:
                    bf.write(chunk)
                bf.close()
        except:
            with open(f"Articles/{imageName}", 'wb') as bf:
                for chunk in metadataResult['cover-image']:
                    bf.write(chunk)
                bf.close()
        time.sleep(1)
        printSuc(f"Cover image saved as {results[selectedIndex]['title']}/{imageName}")
    
    part = 1
    progress = 0
    printInf("Getting articles from libread...")
    
    for i in range(startChapter-2, endChapter, jump):
        mergedArticle = ""
        for j in range(i+1, i+jump+1):
            if(j>endChapter-1):
                break
            articleLink = f"https://{DOMAIN_NAME}" + metadataResult['chapters'][j]['href']
            article = getArticle(articleLink)
            clearLine()
            progressBar(total_size=endChapter-startChapter, size_done=progress, fill_symbol="■", length=35, suffix="There")
            
            # use M2 for TTS
            if(isTTS and canUseM2ForTTS):
                progressBar(total_size=endChapter-startChapter, size_done=progress, fill_symbol="■", length=35, suffix="There \033[38;5;141m[CONVERTING]\033[0m {Chapter - {0}}".replace("{0}", str(j+1)))
                
                # Create the enviroment for the current cycle
                wd = results[selectedIndex]['title'] + "/.OPD"
                if not os.path.isdir(wd): os.mkdir(wd)
                
                try:
                    asyncio.run(createTTSFromText(text=article, outputPath=(wd+f"/Chapter-{str(j+1)}.mp3"), coverImagePath=f"{results[selectedIndex]['title']}/{imageName}"))
                except Exception as E:
                    printErr(f"Fatal Exception occured during conversion. Couldn't proceed further with TTS. {E}")
                    isTTs = False

            mergedArticle += article + "\n\n"
            progress += 1
        endChapterName = i+jump+1
        if(i+jump+1 > endChapter):
            endChapterName = endChapter
        #results[selectedIndex]['title']} ~ Chapter-{i+2}-{endChapterName}
        actualOutputFileName = OUTPUT_FILE_NAME.replace("!TITLE!", results[selectedIndex]['title']).replace("!STARTCHAPTER!", str((i+2))).replace("!ENDCHAPTER!", str(endChapterName))
        if(REPLACEMENT_CHARACTER != ""):
            actualOutputFileName = actualOutputFileName.replace(" ", REPLACEMENT_CHARACTER)
        if(i+1 < endChapter):
            try:
                with open(f"{results[selectedIndex]['title']}/{actualOutputFileName}.txt", "w", encoding='utf-8') as f:
                    f.write(mergedArticle)
                    f.close()
            except:   
                with open(f"Articles/{actualOutputFileName}.txt", "w", encoding='utf-8') as f:
                    f.write(mergedArticle)
                    f.close()
            
            # merge converted chunks and delete the opd folder
            if(isTTS and canUseM2ForTTS):
                clearLine()
                progressBar(total_size=endChapter-startChapter, size_done=progress, fill_symbol="■", length=35, suffix="There \033[38;5;87m[CONCATENATING]\033[0m             ")
                mergeChunks(chunkFilesDir=results[selectedIndex]['title'] + "/.OPD",
                            outputFilePrefix=f"{results[selectedIndex]['title']}/{actualOutputFileName}",
                            coverImagePath=f"{results[selectedIndex]['title']}/{imageName}")
                shutil.rmtree(results[selectedIndex]['title'] + "/.OPD")

            if(isTTS and not canUseM2ForTTS):
                clearLine()
                progressBar(total_size=endChapter-startChapter, size_done=progress, fill_symbol="■", length=35, suffix="There \033[38;5;141m[CONVERTING]\033[0m {Chapter: {startChapter}-{EndChapter}}".replace("{startChapter}", str(i+2)).replace("{EndChapter}", str(endChapterName)))
                try:
                    asyncio.run(createTTSFromFile(filepath=f"{results[selectedIndex]['title']}/{actualOutputFileName}.txt", outputFilePrefix=f"{results[selectedIndex]['title']}/{actualOutputFileName}", coverImagePath=f"{results[selectedIndex]['title']}/{imageName}"))
                except:
                    try:
                        asyncio.run(createTTSFromFile(filepath=f"Articles/{actualOutputFileName}.txt", outputFilePrefix=f"Articles/{actualOutputFileName}", coverImagePath=f"Articles/{imageName}"))
                    except Exception as E:
                            printErr("\nFatal error Occured while converting text to speech! Couldn't proceed further with TTS. {E}")

        # breaks on Windows and wayland 
        if(isPause and progress != ((endChapter-startChapter))+1):
            clearLine()
            progressBar(total_size=endChapter-startChapter, size_done=progress, fill_symbol="■", length=35, suffix="There \033[38;5;226m[PAUSED]\033[0m    ")
            def pause_process():
                with keyboard.Events() as events:
                    event = events.get(1e6)
                    if("libread-tool" in (" " + getActiveWindow().title.lower() + " ") or "visual studio code" in getActiveWindow().title.lower()):
                        if(event.key == keyboard.KeyCode.from_char('r')):
                            return
                        else:
                            event = None
                            pause_process()
                    else:
                        event = None
                        pause_process()
            pause_process()
        
        clearLine()
        progressBar(total_size=endChapter-startChapter, size_done=progress, fill_symbol="■", length=35, suffix="There             ")
                    
                
    clearLine()
    print()
    printFeaturedText("Fetched all chapters successfully!", msgColorCode=105, blinkersColorCode=46)
    print(f"All chapters are stored inside the {results[selectedIndex]['title']} directory.")
    input()
