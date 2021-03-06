import re
import requests
import bs4
import convertapi
import os


def startSecondNameParse():
    request = requests.get('http://xn--80aybw.xn--p1ai/svedeniya-ob-obrazovatelnoj-organizatsii/rukovodstvo-i-pedagogicheskij-sostav')
    soup = bs4.BeautifulSoup(request.content, 'html.parser')
    url = soup.select('body > section.content > div > div > div > div.col-lg-9 > div > div.content-page > div.content-page__body > ul > li:nth-child(2) > span > strong > a')[0]['href']
    url = "http://намт.рф" + url
    file = requests.get(url)
    with open('assets/secondName.pdf', "wb") as f:
        f.write(file.content)
        f.close()

    convertapi.api_secret = 'sDh1snxkw8dKPWxk'
    convertapi.convert('txt', {
        'File': 'assets/secondName.pdf'
    }, from_format='pdf').save_files('assets')

    os.remove('assets/secondName.pdf')


def findFullName(arg):
    if arg != "":
        with open('assets/secondName.txt', "r", encoding="utf8") as txt:
            for line in txt:
                if re.search(arg.title(), line):
                    line = line.split(" ")
                    try:
                        if line[3] == "":
                            return f"{line[0]} {line[1]} {line[2]}"
                        else:
                            return "Фамилия не найдена"
                    except IndexError:
                        return f"{line[0]} {line[1]} {line[2]}"

            txt.close()
    else:
        return "Фамилия не найдена"
