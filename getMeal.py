# -*- coding:utf-8 -*-

import datetime
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

    return breakfast + ',' + lunch + ',' + dinner


def getToday():
    today = datetime.date.today()
    return [today.month, today.day]


def getTommorow():
    tommorow = datetime.date.today() + datetime.timedelta(days=1)
    return [tommorow.month, tommorow.day]

def main(date, fs_name) :
    query = str(date[0]) + '월 ' + str(date[1]) + '일 식단입니다.'

    query_txt = open('query_txt.txt', mode='wt', encoding='utf-8')
    query_txt.write(query)

    target_url = find_href_by_date(query)
    meal = get_meal(target_url)
    file_name = fs_name+'.txt'
    meal_txt = open(file_name, mode='wt', encoding='utf-8')
    meal_txt.write(meal)

if __name__ == "__main__":
    todayDate = getToday()
    tommorowDate = getTommorow()

    main(todayDate, 'today')
    main(tommorowDate, 'tommorow')

    # today_date_query = todayDate[0] + '월 ' + todayDate[1] + '일 식단입니다.'
    # tmr_date_query = tommorowDate[0] + '월 ' + tommorowDate[1] + '일 식단입니다.'

    # TODAY_URL = find_href_by_date(today_date_query)
    # TOMMOROW_URL = find_href_by_date(tmr_date_query)

    # today_meal = get_meal(TODAY_URL)
    # tommorow_meal = get_meal(TOMMOROW_URL)

    # today_meal_txt = open('today_meal.txt', mode='wt', encoding='utf-8')
    # today_meal_txt.write(today_meal)

    # tommorow_meal_txt = open('tommorow_meal.txt', mode='wt', encoding='utf-8')
    # tommorow_meal_txt.write(tommorow_meal)

    # date_txt = open('date_query.txt', mode='wt', encoding='utf-8')
    # date_txt.write(date_query)

    # argv_txt = open('argv_txt.txt', mode='wt', encoding='utf-8')
    # argv_txt.write(sys.argv[1])

    # date_query = '5월 2일 식단입니다.'
    # TARGET_URL = find_href_by_date(date_query)
    # get_meal(TARGET_URL)
