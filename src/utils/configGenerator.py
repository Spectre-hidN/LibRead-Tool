def create_default_config(config_name):

    searchResultSelector = "body > div.main > div.wp > div.row-box > div.col-content > div > div > div > div > div.txt > h3 > a"
    statusSelectorI = "body > div.main > div > div > div.col-content > div.m-info > div.m-book1 > div.m-imgtxt > div.txt > div:nth-child(6) > div > span"
    statusSelectorII = "body > div.main > div > div > div.col-content > div.m-info > div.m-book1 > div.m-imgtxt > div.txt > div:nth-child(5) > div > span"
    statusSelectorIII = "body > div.main > div > div > div.col-content > div.m-info > div.m-book1 > div.m-imgtxt > div.txt > div:nth-child(4) > div > span"
    totalChaptersSelector = "#idData > li > a"
    coverImageDivSelector = "body > div.main > div > div > div.col-content > div.m-info > div.m-book1 > div.m-imgtxt > div.pic > img"
    articleDivSelector = "#article > p"
    
    with open(config_name, 'w', encoding='utf-8') as cf:
        cf.write(f"""[DOMAIN]

; Change the domain name

domainName = libread.com

; Modify the headers if the server is blocking your requests for being headless.
origin = https://libread.com
referer = https://libread.com/
authority = libread.com
userAgent = Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36
                 

[SELECTOR_MAPS]

; These are the advanced settings to fix if the website changes its document structure.
; IT IS NOT RECOMMENDED TO MODIFY.

searchResultSelector = {searchResultSelector}
statusSelectorI = {statusSelectorI}
statusSelectorII = {statusSelectorII}
statusSelectorIII = {statusSelectorIII}
totalChaptersSelector = {totalChaptersSelector}
coverImageDivSelector = {coverImageDivSelector}
articleDivSelector = {articleDivSelector}

[NOMENCLATURES]

; You can only use the below variables to set up a name. use ! at both ends to indicate its a variable.
; TITLE -> Name of the novel
; STARTCHAPTER -> Indicates the starting chapter number of the part
; ENDCHAPTER -> Indicates the ending chapter number of the part

; Change the nomenclature for the output file. Affects both .txt and .mp3 file
outputNomenclature = !TITLE! ~ Chapter-!STARTCHAPTER!-!ENDCHAPTER!

; Nomenclature for the cover image
coverImageNomenclature = !TITLE! ~ Cover

; Replace WHITESPACE
; By befault it doesn't replace any WHITESPACE.
; But, if any of the variable has a WHITESPACE then it will be replaced by the given charater

whitespaceReplacementCharacter = 


[TTS_CONFIG]

; Choose a voice name from the below list
Voice = en-GB-SoniaNeural

; Embed unsynced subtitles to the mp3 file
; 1 = yes, 0 = no
embedSubtitles = 1

; Enabling the below switch will force LibRead-Tool to fetch all the articles first in a part, then convert Text-To-Speech.
; Usually, this happens when FFMPEG is not accessible by LibRead-Tool.
; 1 = yes, 0 = no
forceGrabFirstThenConvert = 0
                 
; All Voices are lsited below
; Name: af-ZA-AdriNeural
; Gender: Female
; 
; Name: af-ZA-WillemNeural
; Gender: Male
; 
; Name: am-ET-AmehaNeural
; Gender: Male
; 
; Name: am-ET-MekdesNeural
; Gender: Female
; 
; Name: ar-AE-FatimaNeural
; Gender: Female
; 
; Name: ar-AE-HamdanNeural
; Gender: Male
; 
; Name: ar-BH-AliNeural
; Gender: Male
; 
; Name: ar-BH-LailaNeural
; Gender: Female
; 
; Name: ar-DZ-AminaNeural
; Gender: Female
; 
; Name: ar-DZ-IsmaelNeural
; Gender: Male
; 
; Name: ar-EG-SalmaNeural
; Gender: Female
; 
; Name: ar-EG-ShakirNeural
; Gender: Male
; 
; Name: ar-IQ-BasselNeural
; Gender: Male
; 
; Name: ar-IQ-RanaNeural
; Gender: Female
; 
; Name: ar-JO-SanaNeural
; Gender: Female
; 
; Name: ar-JO-TaimNeural
; Gender: Male
; 
; Name: ar-KW-FahedNeural
; Gender: Male
; 
; Name: ar-KW-NouraNeural
; Gender: Female
; 
; Name: ar-LB-LaylaNeural
; Gender: Female
; 
; Name: ar-LB-RamiNeural
; Gender: Male
; 
; Name: ar-LY-ImanNeural
; Gender: Female
; 
; Name: ar-LY-OmarNeural
; Gender: Male
; 
; Name: ar-MA-JamalNeural
; Gender: Male
; 
; Name: ar-MA-MounaNeural
; Gender: Female
; 
; Name: ar-OM-AbdullahNeural
; Gender: Male
; 
; Name: ar-OM-AyshaNeural
; Gender: Female
; 
; Name: ar-QA-AmalNeural
; Gender: Female
; 
; Name: ar-QA-MoazNeural
; Gender: Male
; 
; Name: ar-SA-HamedNeural
; Gender: Male
; 
; Name: ar-SA-ZariyahNeural
; Gender: Female
; 
; Name: ar-SY-AmanyNeural
; Gender: Female
; 
; Name: ar-SY-LaithNeural
; Gender: Male
; 
; Name: ar-TN-HediNeural
; Gender: Male
; 
; Name: ar-TN-ReemNeural
; Gender: Female
; 
; Name: ar-YE-MaryamNeural
; Gender: Female
; 
; Name: ar-YE-SalehNeural
; Gender: Male
; 
; Name: az-AZ-BabekNeural
; Gender: Male
; 
; Name: az-AZ-BanuNeural
; Gender: Female
; 
; Name: bg-BG-BorislavNeural
; Gender: Male
; 
; Name: bg-BG-KalinaNeural
; Gender: Female
; 
; Name: bn-BD-NabanitaNeural
; Gender: Female
; 
; Name: bn-BD-PradeepNeural
; Gender: Male
; 
; Name: bn-IN-BashkarNeural
; Gender: Male
; 
; Name: bn-IN-TanishaaNeural
; Gender: Female
; 
; Name: bs-BA-GoranNeural
; Gender: Male
; 
; Name: bs-BA-VesnaNeural
; Gender: Female
; 
; Name: ca-ES-EnricNeural
; Gender: Male
; 
; Name: ca-ES-JoanaNeural
; Gender: Female
; 
; Name: cs-CZ-AntoninNeural
; Gender: Male
; 
; Name: cs-CZ-VlastaNeural
; Gender: Female
; 
; Name: cy-GB-AledNeural
; Gender: Male
; 
; Name: cy-GB-NiaNeural
; Gender: Female
; 
; Name: da-DK-ChristelNeural
; Gender: Female
; 
; Name: da-DK-JeppeNeural
; Gender: Male
; 
; Name: de-AT-IngridNeural
; Gender: Female
; 
; Name: de-AT-JonasNeural
; Gender: Male
; 
; Name: de-CH-JanNeural
; Gender: Male
; 
; Name: de-CH-LeniNeural
; Gender: Female
; 
; Name: de-DE-AmalaNeural
; Gender: Female
; 
; Name: de-DE-ConradNeural
; Gender: Male
; 
; Name: de-DE-FlorianMultilingualNeural
; Gender: Male
; 
; Name: de-DE-KatjaNeural
; Gender: Female
; 
; Name: de-DE-KillianNeural
; Gender: Male
; 
; Name: de-DE-SeraphinaMultilingualNeural
; Gender: Female
; 
; Name: el-GR-AthinaNeural
; Gender: Female
; 
; Name: el-GR-NestorasNeural
; Gender: Male
; 
; Name: en-AU-NatashaNeural
; Gender: Female
; 
; Name: en-AU-WilliamNeural
; Gender: Male
; 
; Name: en-CA-ClaraNeural
; Gender: Female
; 
; Name: en-CA-LiamNeural
; Gender: Male
; 
; Name: en-GB-LibbyNeural
; Gender: Female
; 
; Name: en-GB-MaisieNeural
; Gender: Female
; 
; Name: en-GB-RyanNeural
; Gender: Male
; 
; Name: en-GB-SoniaNeural
; Gender: Female
; 
; Name: en-GB-ThomasNeural
; Gender: Male
; 
; Name: en-HK-SamNeural
; Gender: Male
; 
; Name: en-HK-YanNeural
; Gender: Female
; 
; Name: en-IE-ConnorNeural
; Gender: Male
; 
; Name: en-IE-EmilyNeural
; Gender: Female
; 
; Name: en-IN-NeerjaExpressiveNeural
; Gender: Female
; 
; Name: en-IN-NeerjaNeural
; Gender: Female
; 
; Name: en-IN-PrabhatNeural
; Gender: Male
; 
; Name: en-KE-AsiliaNeural
; Gender: Female
; 
; Name: en-KE-ChilembaNeural
; Gender: Male
; 
; Name: en-NG-AbeoNeural
; Gender: Male
; 
; Name: en-NG-EzinneNeural
; Gender: Female
; 
; Name: en-NZ-MitchellNeural
; Gender: Male
; 
; Name: en-NZ-MollyNeural
; Gender: Female
; 
; Name: en-PH-JamesNeural
; Gender: Male
; 
; Name: en-PH-RosaNeural
; Gender: Female
; 
; Name: en-SG-LunaNeural
; Gender: Female
; 
; Name: en-SG-WayneNeural
; Gender: Male
; 
; Name: en-TZ-ElimuNeural
; Gender: Male
; 
; Name: en-TZ-ImaniNeural
; Gender: Female
; 
; Name: en-US-AnaNeural
; Gender: Female
; 
; Name: en-US-AndrewNeural
; Gender: Male
; 
; Name: en-US-AriaNeural
; Gender: Female
; 
; Name: en-US-AvaNeural
; Gender: Female
; 
; Name: en-US-BrianNeural
; Gender: Male
; 
; Name: en-US-ChristopherNeural
; Gender: Male
; 
; Name: en-US-EmmaNeural
; Gender: Female
; 
; Name: en-US-EricNeural
; Gender: Male
; 
; Name: en-US-GuyNeural
; Gender: Male
; 
; Name: en-US-JennyNeural
; Gender: Female
; 
; Name: en-US-MichelleNeural
; Gender: Female
; 
; Name: en-US-RogerNeural
; Gender: Male
; 
; Name: en-US-SteffanNeural
; Gender: Male
; 
; Name: en-ZA-LeahNeural
; Gender: Female
; 
; Name: en-ZA-LukeNeural
; Gender: Male
; 
; Name: es-AR-ElenaNeural
; Gender: Female
; 
; Name: es-AR-TomasNeural
; Gender: Male
; 
; Name: es-BO-MarceloNeural
; Gender: Male
; 
; Name: es-BO-SofiaNeural
; Gender: Female
; 
; Name: es-CL-CatalinaNeural
; Gender: Female
; 
; Name: es-CL-LorenzoNeural
; Gender: Male
; 
; Name: es-CO-GonzaloNeural
; Gender: Male
; 
; Name: es-CO-SalomeNeural
; Gender: Female
; 
; Name: es-CR-JuanNeural
; Gender: Male
; 
; Name: es-CR-MariaNeural
; Gender: Female
; 
; Name: es-CU-BelkysNeural
; Gender: Female
; 
; Name: es-CU-ManuelNeural
; Gender: Male
; 
; Name: es-DO-EmilioNeural
; Gender: Male
; 
; Name: es-DO-RamonaNeural
; Gender: Female
; 
; Name: es-EC-AndreaNeural
; Gender: Female
; 
; Name: es-EC-LuisNeural
; Gender: Male
; 
; Name: es-ES-AlvaroNeural
; Gender: Male
; 
; Name: es-ES-ElviraNeural
; Gender: Female
; 
; Name: es-ES-XimenaNeural
; Gender: Female
; 
; Name: es-GQ-JavierNeural
; Gender: Male
; 
; Name: es-GQ-TeresaNeural
; Gender: Female
; 
; Name: es-GT-AndresNeural
; Gender: Male
; 
; Name: es-GT-MartaNeural
; Gender: Female
; 
; Name: es-HN-CarlosNeural
; Gender: Male
; 
; Name: es-HN-KarlaNeural
; Gender: Female
; 
; Name: es-MX-DaliaNeural
; Gender: Female
; 
; Name: es-MX-JorgeNeural
; Gender: Male
; 
; Name: es-NI-FedericoNeural
; Gender: Male
; 
; Name: es-NI-YolandaNeural
; Gender: Female
; 
; Name: es-PA-MargaritaNeural
; Gender: Female
; 
; Name: es-PA-RobertoNeural
; Gender: Male
; 
; Name: es-PE-AlexNeural
; Gender: Male
; 
; Name: es-PE-CamilaNeural
; Gender: Female
; 
; Name: es-PR-KarinaNeural
; Gender: Female
; 
; Name: es-PR-VictorNeural
; Gender: Male
; 
; Name: es-PY-MarioNeural
; Gender: Male
; 
; Name: es-PY-TaniaNeural
; Gender: Female
; 
; Name: es-SV-LorenaNeural
; Gender: Female
; 
; Name: es-SV-RodrigoNeural
; Gender: Male
; 
; Name: es-US-AlonsoNeural
; Gender: Male
; 
; Name: es-US-PalomaNeural
; Gender: Female
; 
; Name: es-UY-MateoNeural
; Gender: Male
; 
; Name: es-UY-ValentinaNeural
; Gender: Female
; 
; Name: es-VE-PaolaNeural
; Gender: Female
; 
; Name: es-VE-SebastianNeural
; Gender: Male
; 
; Name: et-EE-AnuNeural
; Gender: Female
; 
; Name: et-EE-KertNeural
; Gender: Male
; 
; Name: fa-IR-DilaraNeural
; Gender: Female
; 
; Name: fa-IR-FaridNeural
; Gender: Male
; 
; Name: fi-FI-HarriNeural
; Gender: Male
; 
; Name: fi-FI-NooraNeural
; Gender: Female
; 
; Name: fil-PH-AngeloNeural
; Gender: Male
; 
; Name: fil-PH-BlessicaNeural
; Gender: Female
; 
; Name: fr-BE-CharlineNeural
; Gender: Female
; 
; Name: fr-BE-GerardNeural
; Gender: Male
; 
; Name: fr-CA-AntoineNeural
; Gender: Male
; 
; Name: fr-CA-JeanNeural
; Gender: Male
; 
; Name: fr-CA-SylvieNeural
; Gender: Female
; 
; Name: fr-CA-ThierryNeural
; Gender: Male
; 
; Name: fr-CH-ArianeNeural
; Gender: Female
; 
; Name: fr-CH-FabriceNeural
; Gender: Male
; 
; Name: fr-FR-DeniseNeural
; Gender: Female
; 
; Name: fr-FR-EloiseNeural
; Gender: Female
; 
; Name: fr-FR-HenriNeural
; Gender: Male
; 
; Name: fr-FR-RemyMultilingualNeural
; Gender: Male
; 
; Name: fr-FR-VivienneMultilingualNeural
; Gender: Female
; 
; Name: ga-IE-ColmNeural
; Gender: Male
; 
; Name: ga-IE-OrlaNeural
; Gender: Female
; 
; Name: gl-ES-RoiNeural
; Gender: Male
; 
; Name: gl-ES-SabelaNeural
; Gender: Female
; 
; Name: gu-IN-DhwaniNeural
; Gender: Female
; 
; Name: gu-IN-NiranjanNeural
; Gender: Male
; 
; Name: he-IL-AvriNeural
; Gender: Male
; 
; Name: he-IL-HilaNeural
; Gender: Female
; 
; Name: hi-IN-MadhurNeural
; Gender: Male
; 
; Name: hi-IN-SwaraNeural
; Gender: Female
; 
; Name: hr-HR-GabrijelaNeural
; Gender: Female
; 
; Name: hr-HR-SreckoNeural
; Gender: Male
; 
; Name: hu-HU-NoemiNeural
; Gender: Female
; 
; Name: hu-HU-TamasNeural
; Gender: Male
; 
; Name: id-ID-ArdiNeural
; Gender: Male
; 
; Name: id-ID-GadisNeural
; Gender: Female
; 
; Name: is-IS-GudrunNeural
; Gender: Female
; 
; Name: is-IS-GunnarNeural
; Gender: Male
; 
; Name: it-IT-DiegoNeural
; Gender: Male
; 
; Name: it-IT-ElsaNeural
; Gender: Female
; 
; Name: it-IT-GiuseppeNeural
; Gender: Male
; 
; Name: it-IT-IsabellaNeural
; Gender: Female
; 
; Name: ja-JP-KeitaNeural
; Gender: Male
; 
; Name: ja-JP-NanamiNeural
; Gender: Female
; 
; Name: jv-ID-DimasNeural
; Gender: Male
; 
; Name: jv-ID-SitiNeural
; Gender: Female
; 
; Name: ka-GE-EkaNeural
; Gender: Female
; 
; Name: ka-GE-GiorgiNeural
; Gender: Male
; 
; Name: kk-KZ-AigulNeural
; Gender: Female
; 
; Name: kk-KZ-DauletNeural
; Gender: Male
; 
; Name: km-KH-PisethNeural
; Gender: Male
; 
; Name: km-KH-SreymomNeural
; Gender: Female
; 
; Name: kn-IN-GaganNeural
; Gender: Male
; 
; Name: kn-IN-SapnaNeural
; Gender: Female
; 
; Name: ko-KR-HyunsuNeural
; Gender: Male
; 
; Name: ko-KR-InJoonNeural
; Gender: Male
; 
; Name: ko-KR-SunHiNeural
; Gender: Female
; 
; Name: lo-LA-ChanthavongNeural
; Gender: Male
; 
; Name: lo-LA-KeomanyNeural
; Gender: Female
; 
; Name: lt-LT-LeonasNeural
; Gender: Male
; 
; Name: lt-LT-OnaNeural
; Gender: Female
; 
; Name: lv-LV-EveritaNeural
; Gender: Female
; 
; Name: lv-LV-NilsNeural
; Gender: Male
; 
; Name: mk-MK-AleksandarNeural
; Gender: Male
; 
; Name: mk-MK-MarijaNeural
; Gender: Female
; 
; Name: ml-IN-MidhunNeural
; Gender: Male
; 
; Name: ml-IN-SobhanaNeural
; Gender: Female
; 
; Name: mn-MN-BataaNeural
; Gender: Male
; 
; Name: mn-MN-YesuiNeural
; Gender: Female
; 
; Name: mr-IN-AarohiNeural
; Gender: Female
; 
; Name: mr-IN-ManoharNeural
; Gender: Male
; 
; Name: ms-MY-OsmanNeural
; Gender: Male
; 
; Name: ms-MY-YasminNeural
; Gender: Female
; 
; Name: mt-MT-GraceNeural
; Gender: Female
; 
; Name: mt-MT-JosephNeural
; Gender: Male
; 
; Name: my-MM-NilarNeural
; Gender: Female
; 
; Name: my-MM-ThihaNeural
; Gender: Male
; 
; Name: nb-NO-FinnNeural
; Gender: Male
; 
; Name: nb-NO-PernilleNeural
; Gender: Female
; 
; Name: ne-NP-HemkalaNeural
; Gender: Female
; 
; Name: ne-NP-SagarNeural
; Gender: Male
; 
; Name: nl-BE-ArnaudNeural
; Gender: Male
; 
; Name: nl-BE-DenaNeural
; Gender: Female
; 
; Name: nl-NL-ColetteNeural
; Gender: Female
; 
; Name: nl-NL-FennaNeural
; Gender: Female
; 
; Name: nl-NL-MaartenNeural
; Gender: Male
; 
; Name: pl-PL-MarekNeural
; Gender: Male
; 
; Name: pl-PL-ZofiaNeural
; Gender: Female
; 
; Name: ps-AF-GulNawazNeural
; Gender: Male
; 
; Name: ps-AF-LatifaNeural
; Gender: Female
; 
; Name: pt-BR-AntonioNeural
; Gender: Male
; 
; Name: pt-BR-FranciscaNeural
; Gender: Female
; 
; Name: pt-BR-ThalitaNeural
; Gender: Female
; 
; Name: pt-PT-DuarteNeural
; Gender: Male
; 
; Name: pt-PT-RaquelNeural
; Gender: Female
; 
; Name: ro-RO-AlinaNeural
; Gender: Female
; 
; Name: ro-RO-EmilNeural
; Gender: Male
; 
; Name: ru-RU-DmitryNeural
; Gender: Male
; 
; Name: ru-RU-SvetlanaNeural
; Gender: Female
; 
; Name: si-LK-SameeraNeural
; Gender: Male
; 
; Name: si-LK-ThiliniNeural
; Gender: Female
; 
; Name: sk-SK-LukasNeural
; Gender: Male
; 
; Name: sk-SK-ViktoriaNeural
; Gender: Female
; 
; Name: sl-SI-PetraNeural
; Gender: Female
; 
; Name: sl-SI-RokNeural
; Gender: Male
; 
; Name: so-SO-MuuseNeural
; Gender: Male
; 
; Name: so-SO-UbaxNeural
; Gender: Female
; 
; Name: sq-AL-AnilaNeural
; Gender: Female
; 
; Name: sq-AL-IlirNeural
; Gender: Male
; 
; Name: sr-RS-NicholasNeural
; Gender: Male
; 
; Name: sr-RS-SophieNeural
; Gender: Female
; 
; Name: su-ID-JajangNeural
; Gender: Male
; 
; Name: su-ID-TutiNeural
; Gender: Female
; 
; Name: sv-SE-MattiasNeural
; Gender: Male
; 
; Name: sv-SE-SofieNeural
; Gender: Female
; 
; Name: sw-KE-RafikiNeural
; Gender: Male
; 
; Name: sw-KE-ZuriNeural
; Gender: Female
; 
; Name: sw-TZ-DaudiNeural
; Gender: Male
; 
; Name: sw-TZ-RehemaNeural
; Gender: Female
; 
; Name: ta-IN-PallaviNeural
; Gender: Female
; 
; Name: ta-IN-ValluvarNeural
; Gender: Male
; 
; Name: ta-LK-KumarNeural
; Gender: Male
; 
; Name: ta-LK-SaranyaNeural
; Gender: Female
; 
; Name: ta-MY-KaniNeural
; Gender: Female
; 
; Name: ta-MY-SuryaNeural
; Gender: Male
; 
; Name: ta-SG-AnbuNeural
; Gender: Male
; 
; Name: ta-SG-VenbaNeural
; Gender: Female
; 
; Name: te-IN-MohanNeural
; Gender: Male
; 
; Name: te-IN-ShrutiNeural
; Gender: Female
; 
; Name: th-TH-NiwatNeural
; Gender: Male
; 
; Name: th-TH-PremwadeeNeural
; Gender: Female
; 
; Name: tr-TR-AhmetNeural
; Gender: Male
; 
; Name: tr-TR-EmelNeural
; Gender: Female
; 
; Name: uk-UA-OstapNeural
; Gender: Male
; 
; Name: uk-UA-PolinaNeural
; Gender: Female
; 
; Name: ur-IN-GulNeural
; Gender: Female
; 
; Name: ur-IN-SalmanNeural
; Gender: Male
; 
; Name: ur-PK-AsadNeural
; Gender: Male
; 
; Name: ur-PK-UzmaNeural
; Gender: Female
; 
; Name: uz-UZ-MadinaNeural
; Gender: Female
; 
; Name: uz-UZ-SardorNeural
; Gender: Male
; 
; Name: vi-VN-HoaiMyNeural
; Gender: Female
; 
; Name: vi-VN-NamMinhNeural
; Gender: Male
; 
; Name: zh-CN-XiaoxiaoNeural
; Gender: Female
; 
; Name: zh-CN-XiaoyiNeural
; Gender: Female
; 
; Name: zh-CN-YunjianNeural
; Gender: Male
; 
; Name: zh-CN-YunxiNeural
; Gender: Male
; 
; Name: zh-CN-YunxiaNeural
; Gender: Male
; 
; Name: zh-CN-YunyangNeural
; Gender: Male
; 
; Name: zh-CN-liaoning-XiaobeiNeural
; Gender: Female
; 
; Name: zh-CN-shaanxi-XiaoniNeural
; Gender: Female
; 
; Name: zh-HK-HiuGaaiNeural
; Gender: Female
; 
; Name: zh-HK-HiuMaanNeural
; Gender: Female
; 
; Name: zh-HK-WanLungNeural
; Gender: Male
; 
; Name: zh-TW-HsiaoChenNeural
; Gender: Female
; 
; Name: zh-TW-HsiaoYuNeural
; Gender: Female
; 
; Name: zh-TW-YunJheNeural
; Gender: Male
; 
; Name: zu-ZA-ThandoNeural
; Gender: Female
; 
; Name: zu-ZA-ThembaNeural
; Gender: Male""")
        cf.close()
  