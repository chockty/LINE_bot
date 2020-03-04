from bs4 import BeautifulSoup
import requests

def scriping():
    html = requests.get("https://toricago.info/schedule/")
    soup = BeautifulSoup(html.text, "lxml")
    return soup
#    get_schedule = soup.find_all("ul",{"class":"sideRecList1"})
#    return get_schedule

def get_schedules(get_schedule):
    event_list = []
    get_schedule = get_schedule.find_all("ul",{"class":"sideRecList1"})
    for event in get_schedule:
        for a in event.select("a"):
            href = a.attrs["href"]
            event_list.append(a.getText())
            event_list.append(href)
    event_info = "\n".join(event_list)
    return event_info
