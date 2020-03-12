from bs4 import BeautifulSoup
import requests

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
    event_list = dict(event_list)
    return event_list
    
