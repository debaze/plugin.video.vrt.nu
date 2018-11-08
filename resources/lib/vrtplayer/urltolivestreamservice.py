import requests
<<<<<<< HEAD
from resources.lib.helperobjects import helperobjects
from resources.lib.vrtplayer import streamservice

class UrlToLivestreamService(streamservice.StreamService):
=======
import urlparse

from resources.lib.helperobjects import helperobjects
from resources.lib.kodiwrappers import kodiwrapper

class UrlToLivestreamService:
    
	_TOKEN_URL = "https://media-services-public.vrt.be/vualto-video-aggregator-web/rest/external/v1/tokens"
	
	def get_stream_from_url(self, url, kodi_wrapper):
            self._kodi_wrapper = kodi_wrapper
            self._vrt_base = 'https://www.vrt.be'
            self._API_KEY = '3_qhEcPa5JGFROVwu5SWKqJ4mVOIkwlFNMSKwzPDAh8QZOtHqu6L4nD5Q7lk0eXOOG'
            session = requests.session()
            cred = helperobjects.Credentials(self._kodi_wrapper)
            if not cred.are_filled_in():
                self._kodi_wrapper.open_settings()
                cred.reload()
            url = urlparse.urljoin(self._vrt_base, url)
            r = session.post('https://accounts.vrt.be/accounts.login',
                                   {'loginID': cred.username, 'password': cred.password, 'APIKey': self._API_KEY,
                                    'sessionExpiration': '-1',
                                    'targetEnv': 'jssdk',
                                    'include': 'profile,data,emails,subscriptions,preferences,',
                                    'includeUserInfo': 'true',
                                    'loginMode': 'standard',
                                    'lang': 'nl-inf',
                                    'source': 'showScreenSet',
                                    'sdk': 'js_latest',
                                    'authMode': 'cookie',
                                    'format': 'json'})

            session.get('https://token.vrt.be/vrtnuinitlogin?provider=site&destination=https://www.vrt.be/vrtnu/')

            logon_json = r.json()

            if logon_json['errorCode'] == 0:
                uid = logon_json['UID']
                sig = logon_json['UIDSignature']
                ts = logon_json['signatureTimestamp']

                data = {'UID': uid, 
                       'UIDSignature': sig,
                       'signatureTimestamp': ts ,
                       'client_id': 'vrtnu-site', 
                       'submit': 'submit'
                       } 

                response = session.post('https://login.vrt.be/perform_login', data=data)

                vrt_player_token_url = session.post(self._TOKEN_URL, headers={'Content-Type': 'application/json'})

                token = vrt_player_token_url.json()['vrtPlayerToken']
                print("###################################################")
                print("##############################o#####################")
                print("##############################ppp#####################")
                print("got token", token)
		# token_response = requests.post(self._TOKEN_URL)
		# token = token_response.json()['vrtPlayerToken']
		stream_response = requests.get(url, {'vrtPlayerToken': token, 'client':'vrtvideo' }).json()
                print(stream_response)
		target_urls = stream_response['targetUrls']
		found_url = False
		index = 0
		while not found_url and index < len(target_urls):
			item = target_urls[index]
			found_url = item['type'] == 'hls_aes'
			stream = item['url']
			index +=1
		return stream
>>>>>>> 99c480873a24e217e4d528ae42e6bdb61c6e0723

    def __init__(self, kodi_wrapper):
        super(UrlToLivestreamService, self).__init__(kodi_wrapper)

    _TOKEN_URL = "https://media-services-public.vrt.be/vualto-video-aggregator-web/rest/external/v1/tokens"

    def get_stream_from_url(self, url):
        (session, token) = super(UrlToLivestreamService, self)._get_session_and_token_from_()

        stream_response = requests.get(url, {'vrtPlayerToken': token, 'client':'vrtvideo' }).json()
        target_urls = stream_response['targetUrls']
        found_url = False
        index = 0
        while not found_url and index < len(target_urls):
          item = target_urls[index]
          found_url = item['type'] == 'hls_aes'
          stream = item['url']
          index +=1
        return stream