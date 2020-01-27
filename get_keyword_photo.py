#Google photo API 認証
import httplib2, os
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import argparse
import random
import requests
import json


SCOPES = "https://www.googleapis.com/auth/photoslibrary"

CLIENT_SECRET_FILE_PATH = "client_id(3)_Pht.json"

USER_SECRET_FILE_PATH = os.environ["CREDIT"]

flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()

def photo_user_auth():
    CREDS = client.Credentials.new_from_json(USER_SECRET_FILE_PATH)
    http = CREDS.authorize(httplib2.Http())
    service = discovery.build("photoslibrary", "v1", http=http)
    return service

service = photo_user_auth()

nextPageToken = ""
get_album_list = service.albums().list(pageSize=10, pageToken=nextPageToken).execute()
album_id = ()

def get_photo_url(keyword):
    for num in range(0, len(get_album_list["albums"])):
        if keyword == get_album_list["albums"][num]["title"]:
            album_id = get_album_list["albums"][num]["id"]
        format_search ={ 
            "albumId" : album_id,
            "pageSize" : 30,
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