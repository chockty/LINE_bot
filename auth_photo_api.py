#Google photo API 認証
import httplib2, os
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import argparse

SCOPES = "https://www.googleapis.com/auth/photoslibrary"

CLIENT_SECRET_FILE_PATH = "client_id(3)_Pht.json"

USER_SECRET_FILE_PATH = 'credentials-photoslibrary.json'

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

#service = photo_get_service()