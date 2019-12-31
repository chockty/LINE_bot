#Google photo API 認証
import httplib2, os
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import argparse
import random
from io import BytesIO
from PIL import Image, ImageOps
import requests

CLIENT_INFO ={
    "installed":{
        "client_id":"902572033754-mk5cvvgjs8ld0t4bbhuho072aolvrsik.apps.googleusercontent.com",
        "project_id":"modern-triumph-254209",
        "auth_uri":"https://accounts.google.com/o/oauth2/auth",
        "token_uri":"https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs",
        "client_secret":"SPErn7SRfLjoGmpUiSjOfqb9",
        "redirect_uris":["urn:ietf:wg:oauth:2.0:oob","http://localhost"]
        }
    }

CREDENTIAL_INFO ={
    "access_token": "ya29.ImC2B0YLJJrH4Y8Lrr4Dxkad5b8_Uwx9wxbsgaoRN5CXZhvhbzk_ZyqiAYSXXrT69oLrkdTGqsi0CWJsRQN0DEz718cRt4ccE7hCS_XEfe_UKq1eiNdNBTv7fUt-nCeTSZY", 
    "client_id": "902572033754-mk5cvvgjs8ld0t4bbhuho072aolvrsik.apps.googleusercontent.com", 
    "client_secret": "SPErn7SRfLjoGmpUiSjOfqb9", 
    "refresh_token": "1//0e4x02R0e0QBpCgYIARAAGA4SNwF-L9Ir6p0a8H4v_FWz4aeA4e40dlGk9LBHHZG9VrIKPHM2wn_UIZWn9mzRd1N86zcDV_6xsaQ", 
    "token_expiry": "2019-12-21T06:59:49Z", 
    "token_uri": "https://oauth2.googleapis.com/token", 
    "user_agent": "photolibrary", 
    "revoke_uri": "https://oauth2.googleapis.com/revoke", 
    "id_token": None, 
    "id_token_jwt": None, 
    "token_response": {
        "access_token": "ya29.ImC2B0YLJJrH4Y8Lrr4Dxkad5b8_Uwx9wxbsgaoRN5CXZhvhbzk_ZyqiAYSXXrT69oLrkdTGqsi0CWJsRQN0DEz718cRt4ccE7hCS_XEfe_UKq1eiNdNBTv7fUt-nCeTSZY", 
        "expires_in": 3600, 
        "scope": "https://www.googleapis.com/auth/photoslibrary", 
        "token_type": "Bearer"}, 
    "scopes": ["https://www.googleapis.com/auth/photoslibrary"], 
    "token_info_uri": "https://oauth2.googleapis.com/tokeninfo", 
    "invalid": False, 
    "_class": "OAuth2Credentials", 
    "_module": "oauth2client.client"
    }


SCOPES = "https://www.googleapis.com/auth/photoslibrary"

CLIENT_SECRET_FILE_PATH = CLIENT_INFO

USER_SECRET_FILE_PATH = CREDENTIAL_INFO

flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()

def photo_user_auth():
    store = Storage(USER_SECRET_FILE_PATH)
    creditials = store.get()

    if not creditials or creditials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE_PATH, SCOPES)
        flow.user_agent = "photolibrary"
        creditials = tools.run_flow(flow, store, flags)
        print("認証結果を保存しました:" + USER_SECRET_FILE_PATH)
    return creditials

def photo_get_service():
    creditials = photo_user_auth()
    http = creditials.authorize(httplib2.Http())
    service = discovery.build("photoslibrary", "v1", http=http)
    return service

service = photo_get_service()

nextPageToken = ""
get_album_list = service.albums().list(pageSize=10, pageToken=nextPageToken).execute()
album_id = ()

def get_photo_url(key_word):
    for num in range(0, len(get_album_list["albums"])):
        if key_word == get_album_list["albums"][num]["title"]:
            album_id = get_album_list["albums"][num]["id"]
    format_search ={ 
        "albumId" : album_id,
        "pageSize" : 10,
        "pageToken" : nextPageToken,
        }
    get_photos = service.mediaItems().search(body=format_search).execute()
    get_photo_info = random.choice(get_photos["mediaItems"])
    show_img_url = get_photo_info["baseUrl"] + "=w{width}-h{height}".format(width=get_photo_info["mediaMetadata"]["width"],height=get_photo_info["mediaMetadata"]["height"])
    return show_img_url

#response = requests.get(show_img_url)
#response
#img = Image.open(BytesIO(response.content))
#img.show()