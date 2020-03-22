#判定用のファイルをkey取得でループ処理
#まずはDICTにデータが入っているか確認。入って無い場合は書き込み。
from write_Sch import write_calendar as wc

def write_calendar_details(DICT,edited_info,service):
    Num = 0
    for DATE in edited_info.keys():
        if not DICT:
            event = {
                "summary": "鶯籠"+ edited_info[DATE][0],
                "description": edited_info[DATE][1],
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
            if Num == len(edited_info):
                break
    #もしDATE（日付）がDICTのkeyの中にあれば、次の分岐へ。
        elif DATE in DICT.keys():
        #鶯籠+場所名（もしくはイベント名）がDICTのDATEのvalueとしてあるか判断。あれば書き込み不要。なければ書き込み
            if "鶯籠" in DICT[DATE][1] or "鶯籠(未)" in DICT[DATE][1]:
                event = service.events().get(calendarId='primary', eventId=DICT[DATE][0]).execute()
                event["summary"] = "鶯籠"+edited_info[DATE][0]
                event["description"] = edited_info[DATE][1]
                updated_event = service.events().update(calendarId='primary', eventId=DICT[DATE][0], body=event).execute()
                Num += 1
                if Num == len(edited_info):
                    break
            else:
                event = {
                    "summary": "鶯籠"+ edited_info[DATE][0],
                    "description": edited_info[DATE][1],
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
                if Num == len(edited_info):
                    break
#もしDATE（日付）がDICTのkeyの中になければ、書き込み処理を行う。
        else:
            event = {
                "summary": "鶯籠"+ edited_info[DATE][0],
                "description": edited_info[DATE][1],
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
            if Num == len(edited_info):
                break

