# -*- coding:utf-8 -*-

import datetime
import requests
from bs4 import BeautifulSoup
from operator import eq


def splitStr(str):
    return str.split(':')[1]


def find_href_by_date(date_query):
    TARGET_URL = 'https://www.dimigo.hs.kr/index.php?mid=school_cafeteria'

    req = requests.get(TARGET_URL)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    titles = soup.find_all("a", "fl")


    for i in titles:
        if date_query in i.text :
            return i['href']


def get_meal(URL):
    mealList = []
    req = requests.get(URL)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')

    content = soup.select('div.scConDoc p')

    for i in content:
        if(i.text):
            mealList.append(i.text)

    b_res = [False]
    l_res = [False]
    d_res = [False]

    for i in mealList:
        if u"조식" in i:
            b_res[0] = True
            b_res.append(i)
        if u"중식" in i:
            l_res[0] = True
            l_res.append(i)
        if u"석식" in i:
            d_res[0] = True
            d_res.append(i)

    if b_res[0]:
        meal_b = b_res[1]
    else:
        meal_b = u'급식 정보를 찾을 수 없습니다'
    if l_res[0]:
        meal_l = l_res[1]
    else:
        meal_l = u'급식 정보를 찾을 수 없습니다'
    if d_res[0]:
        meal_d = d_res[1]
    else:
        meal_d = u'급식 정보를 찾을 수 없습니다'

    meal_res = splitStr(meal_b) + '|' + splitStr(meal_l) + \
        '|' + splitStr(meal_d)
    return meal_res


def getToday():
    today = datetime.date.today()
    return [today.month, today.day]


def getTommorow():
    tommorow = datetime.date.today() + datetime.timedelta(days=1)
    return [tommorow.month, tommorow.day]


if __name__ == "__main__":
    todayDate = getToday()
    tommorowDate = getTommorow()

    today_date_query = str(todayDate[0]) + u'월 ' + str(todayDate[1]) + u'일 식단입니다.'
    tmr_date_query = str(tommorowDate[0]) + u'월 ' + str(tommorowDate[1]) + u'일 식단입니다.'

    TODAY_URL = find_href_by_date(today_date_query)
    TOMMOROW_URL = find_href_by_date(tmr_date_query)

    today_meal = get_meal(TODAY_URL)
    tommorow_meal = get_meal(TOMMOROW_URL)

    today_txt = open('today_meal.txt', 'wt')
    today_txt.write(today_meal)
    today_txt.close()

    tommorow_txt = open('tommorow_meal.txt', 'wt')
    tommorow_txt.write(tommorow_meal)
    tommorow_txt.close()
