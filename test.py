import requests
from bs4 import BeautifulSoup

def animelist(username):
    session = requests.Session()
    request = session.get('https://jut.su/user/'+str(username)+'/anime')
    if request.status_code == 200:
        soup = BeautifulSoup(request.content, 'html.parser')
        divs = soup.findAll("div", class_="all_anime")
        Str = ""
        for div in divs:
            title = div.find('div', class_='aaname').text
            Str += "\n" + title
        return Str
    else:
        print('error')