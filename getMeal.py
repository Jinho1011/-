# -*- coding:utf-8 -*-

import sys
import requests
from bs4 import BeautifulSoup


def splitStr(str):
    return str.split(':')[1]


def find_href_by_date(date_query):
    TARGET_URL = 'https://www.dimigo.hs.kr/index.php?mid=school_cafeteria'

    req = requests.get(TARGET_URL)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    titles = soup.find_all("a", "fl")

    for i in titles:
        if (i.text == date_query):
            return i['href']


def get_meal(URL):
    rawStr = ''
    req = requests.get(URL)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    content = soup.find_all("div", "scConDoc")
    for i in content:
        rawStr += i.text

    rawStr = rawStr.split("중식")
    temp = rawStr[1].split("석식")

    breakfast = rawStr[0]
    lunch = temp[0]
    dinner = temp[1]

    breakfast = breakfast.split("조식")
    breakfast = breakfast[1]

    breakfast = splitStr(breakfast).rstrip('\n')
    lunch = splitStr(lunch).rstrip('\n')
    dinner = splitStr(dinner).rstrip('\n')
    result = breakfast + ',' + lunch + ',' + dinner

    print(result)


if __name__ == "__main__":
    date_query = sys.argv[2] + '월 ' + sys.argv[1] + '일 식단입니다.'

    # date_txt = open('date_query.txt', mode='wt', encoding='utf-8')
    # date_txt.write(date_query)

    # argv_txt = open('argv_txt.txt', mode='wt', encoding='utf-8')
    # argv_txt.write(sys.argv[2])

    # date_query = '5월 2일 식단입니다.'
    TARGET_URL = find_href_by_date(date_query)
    get_meal(TARGET_URL)
