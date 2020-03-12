#★html情報の取得
from bs4 import BeautifulSoup
import requests
import datetime

#★必要なデータを取り込み用に処理
Remove_list = ["(Mon)","(Tue)","(Wed)","(Thu)","(Fri)","(Sat)","(Sun)","（Mon）","（Tue）","（Wed）","（Thu）","（Fri）","（Sat）","（Sun）"]

#全角→半角のテーブル
henkan_table = str.maketrans({"１":"1","２":"2","３":"3","４":"4","５":"5","６":"6","７":"7","８":"8","９":"9","０":"0"})

def edit_sch_info(i):
    text = i.get_text()
    text = text.split("FUTURE")
    i = text[1].split("ACT")
    for num in range(0,len(i)):
        i[num] = i[num].replace("\n", "")
        i[num] = i[num].replace("\t", "")
        i[num] = i[num].replace("鶯籠", "")
        i[num] = i[num].replace("ツイート", "")
        i[num] = i[num].replace("\xa0/\xa0", "")
        i[num] = i[num].replace("鶯谷わんこ学園（ゲスト）", "")
        i[num] = i[num].replace("救急舎（ゲスト）", "")
        i[num] = i[num].replace("KADOKA（ネパール）and more ", "")
        i[num] = i[num].replace("12>&raquo","")
        for Removal in Remove_list:
            if Removal in i[num]:
                i[num]=i[num].split(Removal)
                
    del i[-2:]
    for num in range(0,len(i)):
        i[num][1] = i[num][1].split("INFO")
        
    for num in range(0,len(i)):
        i[num][0] = i[num][0].replace(".", "-")
        i[num][0] = str(datetime.datetime.strptime(i[num][0], '%Y-%m-%d'))
        i[num][0] = i[num][0].replace(" 00:00:00", "")
        
    edited_info = dict(i)
    return edited_info

def choice_a_day(keyword,event_info):
    keyword = keyword.translate(henkan_table)
    today = datetime.date.today()
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
            selected_day = datetime.datetime.strptime(selected_day,"%Y/%m/%d")
            selected_day = selected_day.strftime("%Y-%m-%d")
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
            a_day_info = []
            a_day_info.append(a_day)
            a_day_info.append(event_info[a_day])
            return a_day_info
            break
        else:
            continue
