from bs4 import BeautifulSoup
import requests

def scriping():
    html = requests.get("https://toricago.info/schedule/")
    soup = BeautifulSoup(html.text, "lxml")
    get_schedule = soup.find_all("ul",{"class":"sideRecList1"})
    return get_schedule

def get_schedules(get_schedule):
    event_list = []
    for event in get_schedule:
        for a in event.select("a"):
            href = a.attrs["href"]
            detail = a.getText()
            SCH = print(href,detail)
            event_list.append(SCH)
    return event_list
