from bs4 import BeautifulSoup
import requests
import datetime

#全角→半角のテーブル
henkan_table = str.maketrans({"１":"1","２":"2","３":"3","４":"4","５":"5","６":"6","７":"7","８":"8","９":"9","０":"0"})

def get_schedules():
    event_list = []
    html = requests.get("https://toricago.info/schedule/")
    soup = BeautifulSoup(html.text, "lxml")
    get_schedule = soup.find_all("ul",{"class":"sideRecList1"})

    for event in get_schedule:
        for a in event.select("a"):
            href = a.attrs["href"]
            event_list.append(a.getText())
            event_list.append(href)
    event_info = "\n".join(event_list)
    return event_info

def get_a_schedule():
    event_list = []
    html = requests.get("https://toricago.info/schedule/")
    soup = BeautifulSoup(html.text, "lxml")
    get_schedule = soup.find_all("ul",{"class":"sideRecList1"})

    for event in get_schedule:
        for a in event.select("a"):
            href = a.attrs["href"]
            event_set = a.getText(),href
            event_list.append(event_set)
#    event_list = dict(event_list)
    return event_list
    
def choice_a_day(keyword,event_info):
    keyword = keyword.translate(henkan_table)
    today = datetime.date.today()
    event_info = dict(event_info)
    selected_day = ()
    key = "エラー発生"
    if "月" in keyword and "日" in keyword:
        try:
            keyword = keyword.replace("月","/") 
            keyword = keyword.replace("日","") 
            selected_day = str(today.year) + "/" + keyword
        except KeyError as key:
            return key
    elif "/" in keyword:
        try:
            selected_day = str(today.year) + "/" + keyword
        except KeyError as key:
            return key
    else:
        try:
            keyword = keyword.replace("0","/") 
            keyword = keyword.replace("0","") 
            selected_day = str(today.year) + keyword
        except KeyError as key:
            return key
            
    for a_day in event_info.keys():
        if selected_day in a_day:
            a_day_info = ()
            edit_one = event_info[a_day].replace("\n", "")
            a_day = a_day.replace("\n", "")
            a_day_info = a_day + "\n" + edit_one
            return a_day_info
            break
        else:
            continue

def get_a_earlist_schedule(events_list):
    a_earlist_one = events_list[0][0].replace("\n", "") + "\n" +events_list[0][1]
    return a_earlist_one

def get_today_event(events_list):
    today = datetime.date.today()
    today = str(today.year) + "/" + str(today.month) + "/" + str(today.day)
    events_list = dict(events_list)
    a_day_info = []
    count = 0
    
    for a_day in events_list.keys():
        if today in a_day:
            a_info = ()
            edit_one = events_list[a_day].replace("\n", "")
            a_day = a_day.replace("\n", "")
            a_info = a_day + "\n" + edit_one
            a_day_info.append(a_info)
            count += 1
            if count == len(events_list.keys()):
                break
            else:
                continue
        elif today not in a_day:
            count += 1
            if count == len(events_list.keys()):
                break
            else:
                continue
        else:
            return Exception
    if len(a_day_info) == 1:
        return a_day_info
    else:
        a_day_info = "\n\n".join(a_day_info)
        return a_day_info




