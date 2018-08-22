import sys
import xbmcgui
import xbmcplugin
import xbmcaddon
import xbmcvfs
import urllib
import urlparse
import json
import hyperion_client
from contextlib import closing

base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])
xbmcplugin.setContent(addon_handle, 'files')

ADDON = xbmcaddon.Addon()
ADDONNAME = ADDON.getAddonInfo('id')

def build_url(query):
    return base_url + '?' + urllib.urlencode(query)

def launching(foldersplit):
    if len(foldersplit) == 2:
        name = foldersplit[1]
    else:
        name1 = ''
        for i in range(1,len(foldersplit)):
            name1 += foldersplit[i] + divider
        name = name1[:-1]
    return name


def cmd_display_current_location(*args):
    window = xbmcgui.WindowXMLDialog('custom-sliders.xml',xbmcaddon.Addon().getAddonInfo('path').decode('utf-8'), 'default', '720p')
    win =xbmcgui.Window(10001)
    win.setProperty( 'VPN.ExitNode' ,  'Brisbane, Australia')
    #Property can be accessed in the XML using:
    #<label fallback="416">$INFO[Window(10001).Property(VPN.ExitNode)]</label>
    window.doModal()
    del window


mode = args.get('mode', None)

#colornames = {'red':(255,0,0), 'green':(0,255,0), 'blue':(0,0,255),'yellow':(255,255,0),'orange':(255,100,0),'purple':(255,0,255),'magenta':(255,50,100),'cyan':(10,100,250),'white':(255,255,255)}
#color_path = 'C:\Users\GianlucaSPS\AppData\Roaming\Kodi\\addons\plugin.program.hyperion-controller\colors.json'
color_path = xbmc.translatePath('special://home/addons/plugin.program.hyperion-controller/colors.json')

divider = '-'
ip = str(ADDON.getSetting('ip'))
port = ADDON.getSetting('port')
apriority = ADDON.getSetting('priority') 
h=hyperion_client.hyperion_client(ip, port)

if mode is None:
    url = build_url({'mode': 'folder', 'foldername': 'Clear All'})
    li = xbmcgui.ListItem('Clear all effects/color', iconImage='http://www.weareclear.co.uk/wp-content/uploads/2017/12/logo.png')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=False)
    
    url = build_url({'mode': 'folder', 'foldername': 'Color'})
    li = xbmcgui.ListItem('Color')
    image='https://teetribe.eu/wp-content/uploads/2018/05/RGB-Red-Green-Blue.png'
    li.setArt({'thumb': image,
                'icon': image,
              'fanart': image})
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)
    
    url = build_url({'mode': 'folder', 'foldername': 'Effects'})
    li = xbmcgui.ListItem('Effects')
    image='https://png.icons8.com/color/1600/color-wheel-2.png'
    li.setArt({'thumb': image,
                'icon': image,
              'fanart': image})
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)
    sliders = 'RGB Sliders'
    url = build_url({'mode': 'folder', 'foldername': sliders})
    li = xbmcgui.ListItem(sliders, iconImage='https://sites.google.com/site/makecolorsimages/sliders-RGB_512x512.png')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
    
    Settings = 'Settings'
    url = build_url({'mode': 'folder', 'foldername': Settings})
    li = xbmcgui.ListItem(Settings, iconImage='https://cdn4.iconfinder.com/data/icons/meBaze-Freebies/512/setting.png')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=False)

    
    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0] == 'folder':
    foldername = args['foldername'][0]

    if foldername == 'Clear All':
        h.clear_all()
        xbmcgui.Dialog().notification(foldername, 'clearing...')
        h.close_connection()
    
    foldersplit = foldername.split(divider)
    if foldersplit[0] == 'Effects':
        if foldername == 'Effects':
            effectnames =  h.effects_names()#['Snake', 'Rainbow swirl fast']
            for e in effectnames:
                #url = 'http://www.vidsplay.com/wp-content/uploads/2017/04/alligator.mp4'
                url = build_url({'mode': 'folder', 'foldername': foldername + divider + e })
                li = xbmcgui.ListItem(e)
                xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

        elif len(foldersplit) > 1:
            nome = launching(foldersplit)
            h.set_effect(effectName=nome, priority=apriority)
            line1 = foldersplit[0]
            line2 = "launching " + nome + " on Hyperion " + ip
            xbmcgui.Dialog().notification(line1, line2)
            h.close_connection()

    elif foldersplit[0] == 'Color':
        with open(color_path) as f:
        #with closing(xbmcvfs.File('colors.json')) as f:
            colornames = json.load(f)
        
        if foldername == 'Color':            
            for c in colornames:
                url = build_url({'mode': 'folder', 'foldername': foldername + divider + c})
                hexColor = '%02x%02x%02x' % tuple(colornames[c])
                img = 'https://dummyimage.com/100x100/' + hexColor + '/' + hexColor + '.jpg'
                li = xbmcgui.ListItem(c, iconImage=img)
                xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=False)

        elif len(foldersplit) > 1:
            nome = launching(foldersplit)
            h.set_RGBcolor(red=colornames[nome][0],green=colornames[nome][1],blue=colornames[nome][2], priority=apriority)
            line1 = foldersplit[0]
            line2 = "launching " + nome + " on Hyperion " + ip
            xbmcgui.Dialog().notification(line1, line2) 
            h.close_connection()
            

    elif foldername == 'RGB Sliders':
        xbmcgui.Dialog().ok(foldername, 'apre un control panel con 3 sliders')
        # xbmc.executebuiltin("ActivateWindow(1100,'plugin://plugin.video.demo1/resources/sliders.xml',return)")
        # text = xbmcgui.Window(10000).getProperty('GEN-DOWNLOADED')
        # xbmcgui.Window(10000).setProperty('GEN-DOWNLOADED', text)
    elif foldername == 'Settings':
        ADDON.openSettings()
        
    xbmcplugin.endOfDirectory(addon_handle)



    
    
    

