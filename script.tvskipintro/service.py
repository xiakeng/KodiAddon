# -*- coding: utf-8 -*-

'''
    TvSkipIntro Add-on
    Copyright (C) 2018 aenema

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see .
'''

import xbmcvfs,xbmc,xbmcaddon,json,os,xbmcgui, time, re,threading

KODI_VERSION = int(xbmc.getInfoLabel("System.BuildVersion").split(".")[0])
addonInfo = xbmcaddon.Addon().getAddonInfo
settings = xbmcaddon.Addon().getSetting
profilePath = xbmcvfs.translatePath(addonInfo('profile'))
addonPath = xbmcvfs.translatePath(addonInfo('path'))
skipFile = os.path.join(profilePath, 'skipintro.json')
defaultSkip = settings('default.skip')
if not os.path.exists(profilePath): xbmcvfs.mkdir(profilePath)

def cleantitle(title):
    if title == None: return
    title = title.lower()
    title = re.sub('&#(\d+);', '', title)
    title = re.sub('(&#[0-9]+)([^;^0-9]+)', '\\1;\\2', title)
    title = title.replace('&quot;', '\"').replace('&amp;', '&')
    title = re.sub(r'\]*\>','', title)
    title = re.sub('\n|([[].+?[]])|([(].+?[)])|\s(vs|v[.])\s|(:|;|-|"|,|\'|\_|\.|\?)|\(|\)|\[|\]|\{|\}|\s', '', title).lower()
    return title.lower()
    
def updateSkip(title, seconds=defaultSkip, start=0, service=True):
    with open(skipFile, 'r') as file:
         json_data = json.load(file)
         for item in json_data:
               if cleantitle(item['title']) == cleantitle(title):
                  item['service'] = service
                  item['skip'] = seconds
                  item['start'] = start
    with open(skipFile, 'w') as file:
        json.dump(json_data, file, indent=2)
        
def newskip(title, seconds, start=0):
    if seconds == '' or seconds == None: seconds = defaultSkip
    newIntro = {'title': title, 'service': False, 'skip': seconds, 'start': start}
    try:
        with open(skipFile) as f:
            data = json.load(f)
    except:
        data = []
    for item in data:
        if cleantitle(title) in cleantitle(item['title']):
            updateSkip(title, seconds=seconds, start=start, service=True)
            return
    data.append(newIntro)
    with open(skipFile, 'w') as f:
        json.dump(data, f, indent=2)

def getSkip(title):
    try:
        with open(skipFile) as f:
            data = json.load(f)
        skip = [i for i in data if i['service'] != False]
        skip = [i['skip'] for i in skip if cleantitle(i['title']) == cleantitle(title)][0]
    except: 
        skip = defaultSkip
        newskip(title, skip)
    return  skip
    
def checkService(title):
    try:
        with open(skipFile) as f: data = json.load(f)
        skip = [i['service'] for i in data if cleantitle(i['title']) == cleantitle(title)][0]
    except: skip = True
    return  skip

def checkStartTime(title):
    try:
        with open(skipFile) as f: data = json.load(f)
        start = [i['start'] for i in data if cleantitle(i['title']) == cleantitle(title)][0]
    except: start = 0
    return  start
    
if not os.path.exists(skipFile): newskip('default', defaultSkip)


class Service():

    WINDOW = xbmcgui.Window(10000)

    def __init__(self, *args):
        addonName = 'Skip Player'
        self.dialogDisplayed = False



    def ServiceEntryPoint(self):
        monitor = xbmc.Monitor()

        while not monitor.abortRequested():
            # check every 5 sec
            if monitor.waitForAbort(1):
                # Abort was requested while waiting. We should exit
                break
            if xbmc.Player().isPlaying():
                try:
                    playTime = xbmc.Player().getTime()

                    self.currentShow = xbmc.getInfoLabel("VideoPlayer.TVShowTitle")
                    if self.currentShow: 
                        status = checkService(self.currentShow)

                        if status == True:
                            skipValue = int(getSkip(self.currentShow))
                            if playTime >= skipValue - 5: 
                                self.dialogDisplayed = False
                            if self.dialogDisplayed == False and playTime < skipValue - 5: 
                                self.SkipIntro(self.currentShow)
                except:pass
            else: 
                self.dialogDisplayed = False
                
    def SkipIntro(self, tvshow):
        try:

            if not xbmc.Player().isPlayingVideo(): 
                raise Exception() 
            
            time.sleep(1)
            timeNow = xbmc.Player().getTime()

            startTime = checkStartTime(tvshow)
            
            if int(startTime) >= int(timeNow): 
                raise Exception()
            
            self.dialogDisplayed = True
            Dialog = CustomDialog('script-dialog.xml', addonPath, show=tvshow)
            Dialog.doModal()
            del Dialog
            
        except Exception as err:
            pass

OK_BUTTON = 201
NEW_BUTTON = 202
ACTION_PREVIOUS_MENU = 10
ACTION_BACK = 92
CENTER_Y = 6
CENTER_X = 2

class CustomDialog(xbmcgui.WindowXMLDialog):

    def __init__(self, xmlFile, resourcePath, show):
        self.tvshow = show

    def onInit(self):
        self.skipValue = int(getSkip(self.tvshow))

        skipLabel = 'SKIP INTRO'
        skipButton = self.getControl(OK_BUTTON)
        skipButton.setLabel(skipLabel)

        threading.Timer(self.skipValue - 5, self.closeDialog).start()

    def closeDialog(self):
        self.close()
        
    def onAction(self, action):
        if action == ACTION_PREVIOUS_MENU or action == ACTION_BACK:
            self.close()

    def onControl(self, control):
        pass

    def onFocus(self, control):
        pass

    def onClick(self, control):
        print(('onClick: %s' % (control)))

        if control == OK_BUTTON:
            timeNow = xbmc.Player().getTime()
            skipTotal = int(self.skipValue)
            xbmc.Player().seekTime(int(skipTotal))          

        if control == NEW_BUTTON:
            dialog = xbmcgui.Dialog()
            d = dialog.input('Skip Value (seconds)', type=xbmcgui.INPUT_NUMERIC)
            d2 = 0
            d2 = dialog.input('Prompt At (seconds)', type=xbmcgui.INPUT_NUMERIC)
            if d2 == '' or d2 == None: d2 = 0
            if str(d) != '' and str(d) != '0': newskip(self.tvshow , d , start=d2)

        if control in [OK_BUTTON, NEW_BUTTON]:
            self.close()
            
Service().ServiceEntryPoint()
