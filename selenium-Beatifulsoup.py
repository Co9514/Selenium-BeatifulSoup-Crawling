from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import re
import json
import os

# Driver를 이용해 크롤링하려는 사이트에 접근
driver = webdriver.Chrome("C:/Users/khj95/Downloads/chromedriver_win32/chromedriver.exe")

driver.implicitly_wait(3)
driver.get('http://www.cgv.co.kr/common/showtimes/iframeTheater.aspx?')

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

# 상영시간표  
default_cgv = 'http://www.cgv.co.kr/common/showtimes/iframeTheater.aspx?' 
cgv_name = "http://section.cgv.co.kr/theater/popup/r_TimeTable.aspx?"
cgv_html = requests.get(cgv_name).text
cgv_location_number=BeautifulSoup(cgv_html,'html.parser')
city_list=['01','02','202','12','11','05','204','206']
area = 'areacode='+city_list[?]+'&'
for i in range(30):
    cgv_location = cgv_location_number.select('#divWrap>a')[i]['href']
    print(cgv_location[37:])
    theater = 'theatercode='+cgv_location[37:0]+'&'
    date = 'date=20190530'
    cgvTime_html = requests.get(default_cgv + area + theater + date).text
    cgvSoup=BeautifulSoup(cgvTime_html,'html.parser')
    cgv=cgvSoup.select('div.sect-showtimes>ul>li')
    for selector in cgv:
        movie_name=selector.select('strong')
        movie_times=selector.select('.info-timetable li a')
        print(movie_name[0].string)
        for movie in movie_times:
            movie_time = movie['data-playstarttime']
            print("상영시간:",movie['data-playstarttime'])
            print("상영관:", movie['data-screenkorname'])
            print("잔여좌석:",movie['data-seatremaincnt'])
            print("====================================")

matched = re.search(r'var theaterJsonData = (.*?);', html, re.S) 
# .: 모든, *: 문자열 ?: 0회이상, 1회 이하 // 즉 .*? : 0번째 모든문자열

driver = webdriver.Chrome("C:/Users/khj95/Downloads/chromedriver_win32/chromedriver.exe")

driver.implicitly_wait(3)
driver.get("http://section.cgv.co.kr/theater/popup/r_TimeTable.aspx?")
element = driver.find_element_by_id("rptRegion_ctl13_lbtnRegion")
element.click()
html = driver.page_source
cgvSoup=BeautifulSoup(html,'lxml')

for i in range(30):
    conn = pymysql.connect(host='localhost', user='root', password='admin1234',
                       db='cgv', charset='utf8')
    curs = conn.cursor()
    cgv = cgvSoup.select('#divWrap>a')[i]['href']
    num = cgv[37:]
    cgv_lo = cgvSoup.select('#divWrap>a>span')[i]
    screen=cgv_lo.string
    sql = """insert into location(city,location_name,num)values (%s, %s, %s)"""
    curs.execute(sql,('제주',screen,num))
    conn.commit()
    conn.close()
os.path.dirname(os.path.abspath('__file__'))

theater = 'theatercode=0012&'
date = 'date=20190531'
cgvTime_html = requests.get(default_cgv + theater + date).text  
cgvTime_soup = BeautifulSoup(cgvTime_html, 'html.parser')
movie_info = cgvTime_soup.select(".sect-showtimes .info-movie")
movie_title = cgvTime_soup.select(".sect-showtimes .info-movie strong")
     # 영화 제목
for title in movie_title:
    print(title.text)  
    movie_time = cgvTime_soup.select(".sect-showtimes .info-timetable li a")
    for time in movie_time:  
     # print(time)  
        print("상영시간:",time['data-playstarttime'])  
        print("상영관:", time['data-screenkorname'])  
        print("잔여좌석:", time['data-seatremaincnt'])  
        print("====================================")


//DB에 저장
import pymysql

cgv_name = "http://section.cgv.co.kr/theater/popup/r_TimeTable.aspx?"
cgvTime_html = requests.get(cgv_name).text
cgvSoup=BeautifulSoup(cgvTime_html,'html.parser')

rows = curs.fetchall()
print(rows)
#for i in range(30):
#    cgv = cgvSoup.select('#divWrap>a')[i]['href']
#    cgv_lo = cgvSoup.select('#divWrap>a>span')[i]
#    num = cgv[37:]
#    print(num,cgv_lo.string)
for i in range(30):
    conn = pymysql.connect(host='localhost', user='root', password='password',
                       db='cgv', charset='utf8')
    curs = conn.cursor()
    cgv = cgvSoup.select('#divWrap>a')[i]['href']
    num = cgv[37:]
    cgv_lo = cgvSoup.select('#divWrap>a>span')[i]
    screen=cgv_lo.string
    sql = """insert into location(city,location_name,num)values (%s, %s, %s)"""
    curs.execute(sql,('경기',screen,num))
    conn.commit()
    conn.close()

import pymysql
conn = pymysql.connect(host='localhost', user='root', password='admin1234',
                       db='cgv', charset='utf8')
curs = conn.cursor()
sql = """create table location(city varchar(10),location_name varchar(30),num varchar(10),primary key(num))default character set utf8 collate utf8_general_ci;"""
curs.execute(sql)
conn.commit()
conn.close()