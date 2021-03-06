'''
Created on 17.04.2016

@author: h0d3nt3uf3l
'''
__author__ = 'h0d3nt3uf3l'

from . import yt_login
from random import randint
#import resources.lib.youtube.client.provider
import xbmcaddon
import re

addon = xbmcaddon.Addon()
api_enable = addon.getSetting('youtube.api.enable')
api_key = addon.getSetting('youtube.api.lastused.key')
api_id = addon.getSetting('youtube.api.lastused.id')
api_secret = addon.getSetting('youtube.api.lastused.secret')
aktivated_logins = 5; # Change this value to get the logins above in the rotation 0 - 5 = 6!!

class Change_API():
    CONFIGS = {
        'last_used': {
            'key': api_key,
            'id': api_id,
            'secret': api_secret,
        },
        'login0': { #Bromix youtube-for-kodi-12
            'id': '947596709414-08nrn314d8j3k91cl4f51srcu6m19hvu',
            'key': 'AIzaSyCDn_9EybTJiymHipNS3jk5ZpCTXdCotQ0',
            'secret': 'HsLT2ZCexIV-VFxWeYVZ2TUc'
        },
       'login1': { #Youtube Plugin for Kodi #1
            'id': '294899064488-a8kc1k1jd00kamqre0vd2nftuiifrf6a',
            'key': 'AIzaSyCZwQuosFJbQznqnqpqpYlaJWVMn16wBvs',
            'secret': 'KTkBKINN5vf4Owj1NYyXLzbe',
        },
        'login2': { #Bromix youtube-for-kodi-13
            'id': '448940676713-min9u5frfujprbnb8f3dri3cv9jr32rn',
            'key': 'AIzaSyAmrf3BneEQPDiUEuQlzy0_rbFGDBg-bi0',
            'secret': '79vMsJsNC9jypSfryUMu00jW'
        },
        'login3': { #Bromix youtube-for-kodi-14
            'id': '107500767506-9mvbaacuscf8cge2n3kkvj50a6dnrk8g',
            'key': 'AIzaSyCCnZImC7gTniNfgwqGwixIdBVGxiCOKlU',
            'secret': '2ceVfognBCtn8uh20HmlJN4X'
        },
        'login4': { #Bromix youtube-for-kodi-15
            'id': '610696918705-bkt6v536k7gn2dtcv8vdngm4b0vt5sev',
            'key': 'AIzaSyATqDim-56y8HcN1NAzQdVZgdMoc6d9Eys',
            'secret': 'kV7ReP1f_Lg9i2hWR2liHnO6'
        },
        'login5': { #Bromix youtube-for-kodi-16
            'id': '879761788105-sduf0ht335dvg923ane7cg1jnt1d5l4k',
            'key': 'AIzaSyBS3rNymJtzPYbJX5lSGdNCBS6ajh4VDDY',
            'secret': 'vBVDa-kNdCHDTkpD8b8HO718'
        },
        'login6': { #Deaktivated / template
            'id': '',
            'key': '',
            'secret': '',
        }
    }
    
    def get_api_key(self, error, last_login, new_logon=False):
        
        if api_enable == 'true':
            return addon.getSetting('youtube.api.key')
        elif error == 'true' or new_logon:
            api_key = self.get_api('key', error, last_login)
        else:
            api_key = addon.getSetting('youtube.api.lastused.key')
        
        return api_key

    def get_api_id(self, error, last_login, new_logon=False):
        
        if api_enable == 'true':
            return addon.getSetting('youtube.api.id')
        elif error == 'true'or new_logon:
            api_id = self.get_api('id', error, last_login)
        else:
            api_id = addon.getSetting('youtube.api.lastused.id')
            
        return api_id

    def get_api_secret(self, error, last_login, new_logon=False):
                
        if api_enable == 'true':
            return addon.getSetting('youtube.api.secret')
        elif error =='true' or new_logon:
            api_secret = self.get_api('secret', error, last_login)
        else:
            api_secret = addon.getSetting('youtube.api.lastused.secret')
        
        return api_secret

    def get_api(self, part, error, last_login):
        
        #last_login = addon.getSetting('youtube.api.lastused.last_login')
        new_login = addon.getSetting('youtube.api.lastused.new_login')
        #error = addon.getSetting('youtube.api.lastused.error')
        if error == 'true':
            if new_login == last_login or new_login == '':
                while new_login == last_login or new_login == '':
                    new_login = login = 'login%i' % randint(0,aktivated_logins)
                addon.setSetting(id='youtube.api.lastused.last_login', value= login)
                addon.setSetting(id='youtube.api.lastused.new_login', value= new_login)
                addon.setSetting(id='youtube.api.lastused.error', value='false')
            else:
                login = new_login
        elif last_login:
            login = last_login
        else:
            login = 'login%i' % randint(0,aktivated_logins)
                    
        addon.setSetting(id='youtube.api.lastused.last_login', value= login)
        
        part_value = self.CONFIGS[login][part]
        
        tempstring = 'youtube.api.lastused.%s' % part
        
        addon.setSetting(id=tempstring, value=part_value)
        
        return part_value
    
    def new_login(self):
        addon.setSetting(id='kodion.access_token', value = '')
        addon.setSetting(id='kodion.refresh_token', value = '')
        addon.setSetting(id='kodion.access_token.expires', value = '')
        addon.setSetting(id='youtube.api.lastused.error', value='false')
        api_error = addon.getSetting('youtube.api.lastused.error')
        addon.setSetting(id='youtube.api.lastused.last_login', value = 'login0')
        api_last_login = addon.getSetting('youtube.api.lastused.last_login')
        
        addon.setSetting(id='youtube.api.lastused.key', value = self.get_api_key(api_error,api_last_login, True))
        addon.setSetting(id='youtube.api.lastused.id', value = self.get_api_id(api_error,api_last_login, True))
        addon.setSetting(id='youtube.api.lastused.secret', value = self.get_api_secret(api_error,api_last_login, True))
        pass