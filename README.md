big thanks to https://github.com/aenemapy/aenemapyrepo

# Introduction
modify the skipintro to suite my own needs  
compared to origin version, changes:
- default to disable the addon
- remove update and disable button, only a clean skip button
- button can hide itself after into

# Usage
When you play a TV show episode, a new entry will be created in skipintro.json in your kodi profile addon folder.
e.g. if you are using Shield TV, location will be: \internal\Android\data\org.xbmc.kodi\files\.kodi\userdata\addon_data\script.tvskipintro\skipintro.json
```
[
  {
    "title": "default",
    "service": false,
    "skip": "45",
    "start": 0
  }
  {
    "title": "Rick and Morty",
    "service": false,
    "skip": "45",
    "start": 0
  }
]
```
update the "service" key to true
update the "start" key to intro length in seconds

Then you are good to go.
Click Skip button will skip to the start position of your setting
If you do not do anything, on (start - 5) the skip button will disappear

# todo
- [ ] edl file support, so it can auto skip or promote skip according to edl file content, tvshow or movie
- [ ] integrate with jellyfin for kodi plugin. Initial plan is modify https://github.com/xiakeng/jellyfin-kodi so I can get actual file path from event
- [ ] use jellyfin api to get actual path info, so this addon can be more independent
- [ ] modify button layout so it can be used on my favorate kodi skins.