#★html情報の取得
from bs4 import BeautifulSoup
import requests
import datetime

#★必要なデータを取り込み用に処理
Remove_list = ["(Mon)","(Tue)","(Wed)","(Thu)","(Fri)","(Sat)","(Sun)","（Mon）","（Tue）","（Wed）","（Thu）","（Fri）","（Sat）","（Sun）"]

def get_edit_sch_info():
    html = requests.get("https://toricago.info/schedule/")
    soup = BeautifulSoup(html.text, "lxml")
    text = soup.get_text()
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

