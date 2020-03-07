import requests
import datetime
from bs4 import BeautifulSoup

sessions = requests.Session()
request = sessions.get('http://www.xn--80aybw.xn--p1ai/studentam/zamena-raspisaniya-doc', headers={'accept': '*/*', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'})
soup = BeautifulSoup(request.content, 'html.parser')

def getChange():
    f = open("change.json", "w")
    f.write('')
    f.close()
    tr = soup.findAll("tr")
    for line in tr:
        line = line.text
        line = line.split()
        if line[0] == "18-4":
            line[0] = "Группа: " + line[0] + "\n"
            if line[1] == "С":
                line[1] = "Пара: " + line[1] + " " + line[2] + " " + line[3] + " " + line[4] + "\n"
                line[2] = ""
                line[3] = ""
                line[4] = ""
                line[5] = "Кто заменяет: " + line[5] + " " + line[6] + "\n"
                line[6] = ""
                line[7] = "Кого заменяет: " + line[7] + " " + line[8] + "\n"
                line[8] = ""
                line[9] = "Кабинет: " + line[9] + "\n----------------------------------\n"
            else:
                 line[1] = "Пара: " + line[1] + "\n"
                 line[2] = "Кто заменяет: " + line[2] + " " + line[3] + "\n"
                 line[3] = ""
                 line[4] = "Кого заменяет: " + line[4] + " " + line[5] + "\n"
                 line[5] = ""
                 line[6] = "Кабинет: " + line[6] + "\n----------------------------------\n"
            f = open("change.json", "a")
            f.write(''.join(map(str, line)))
            f.close()
            work = 1
    try:
        if work == 1:
            return withOutChange()
    except:
        return f"Замен на завтра нету.\nВажно: Замены с физкультурой не пишется!"

def getChangeDate():
    todayData = datetime.datetime.today() + datetime.timedelta(days=1)
    todayData = todayData.strftime('%d.%m.%Yг')
    span = soup.findAll('span')
    for data in span:
        data = data.text
        line = data.find(todayData)
        if line != -1:
            work = 1
    try:
        if work == 1:
            getChange()
    except:
        return 1

def withOutChange():
    f = open("change.json", "r")
    withOut = f.read()
    f.close()
    return withOut

def start():
    if getChangeDate() == 1:
        return f"Замен нет на сайте!"
    else:
        getChange()
        return withOutChange()
