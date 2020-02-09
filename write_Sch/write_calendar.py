#Google Calendar API 取得
import httplib2, os
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import argparse
import random
import requests
import json

SCOPES = "https://www.googleapis.com/auth/calendar"

USER_SECRET_FILE_PATH = os.environ["Ca_CREDIT"]

flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()

def calendar_user_auth():
    CREDS = client.Credentials.new_from_json(USER_SECRET_FILE_PATH)
    http = CREDS.authorize(httplib2.Http())
    service = discovery.build("calendar", "v3", http=http)
    return service

service = calendar_user_auth()

#Googleカレンダーに入力してあるイベントを取得する
def get_calendar_events(service):
    event = service.events().list(calendarId='primary').execute()
    searched_lists = []
    DICT = {}
    searched_lists = []
    
    for get_data in event["items"]:
        date = get_data.get("start").get("date") 
        searched_tuples = get_data.get("id"), get_data.get("summary")
        searched_data = date,list(searched_tuples)
        searched_lists.append(searched_data)
    DICT = dict(searched_lists)
    return DICT

#カレンダーのイベントを参照してスケジュールを入力するかどうかを条件分岐させる
def hantei_wtite(DICT,edited_Sch_list):
    Num = 0
    #判定用のファイルをkey取得でループ処理
    #まずはDICTにデータが入っているか確認。入って無い場合は書き込み。
    for DATE in edited_Sch_list.keys():
        if not DICT:
            event = {
                "summary": "鶯籠(未)"+ edited_Sch_list[DATE],
                "description": edited_Sch_list[DATE],
                "start": {
                    "date": DATE,
                    "timezone": "Asia/Tokyo",
                    },
                    "end":{
                        "date": DATE,
                        "timezone": "Asia/Tokyo",
                        },
                        }
            event = service.events().insert(calendarId='primary', body=event).execute()
            Num += 1
            if Num == len(edited_Sch_list):
                break
    #もしDATE（日付）がDICTのkeyの中にあれば、次の分岐へ。
        elif DATE in DICT.keys():
        #鶯籠+場所名（もしくはイベント名）がDICTのDATEのvalueとしてあるか判断。あれば書き込み不要。なければ書き込み
            if "鶯籠" in DICT[DATE][1]:
                Num += 1
                if Num == len(edited_Sch_list):
                    break
            else:
                event = {
                    "summary": "鶯籠(未)"+ edited_Sch_list[DATE],
                    "description": edited_Sch_list[DATE],
                    "start": {
                        "date": DATE,
                        "timezone": "Asia/Tokyo",
                        },
                        "end":{
                            "date": DATE,
                            "timezone": "Asia/Tokyo",
                            },
                            }
                event = service.events().insert(calendarId='primary', body=event).execute()
                Num += 1
                if Num == len(edited_Sch_list):
                    break
#もしDATE（日付）がDICTのkeyの中になければ、書き込み処理を行う。
        else:
            event = {
                "summary": "鶯籠(未)"+edited_Sch_list[DATE],
                "description": edited_Sch_list[DATE],
                "start": {
                    "date": DATE,
                    "timezone": "Asia/Tokyo",
                    },
                    "end":{
                        "date": DATE,
                        "timezone": "Asia/Tokyo",
                        },
                    }
            event = service.events().insert(calendarId='primary', body=event).execute()
            Num += 1
            if Num == len(edited_Sch_list):
                break

