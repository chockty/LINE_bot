import httplib2, os
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import random
import auth_photo_api as auth

service = auth.photo_get_service()
album_id = ()
nextPageToken = ""

def get_photo_url(event):
    get_album_list = service.albums().list(pageSize=10, pageToken=nextPageToken).execute()
    for num in range(0, len(get_album_list)):
        if event == get_album_list["albums"][num]["title"]:
            album_id = get_album_list["albums"][num]["id"]
    format_search = {
        'albumId' : album_id,
        'pageSize' : 10,
        'pageToken' : nextPageToken,
    }
    get_photos = service.mediaItems().search(body=format_search).execute()
    get_photo_info = random.choice(get_photos["mediaItems"])
    show_img_url = get_photo_info["baseUrl"] + "=w{width}-h{height}".format(width=get_photo_info["mediaMetadata"]["width"],height=get_photo_info["mediaMetadata"]["height"])
    return show_img_url
