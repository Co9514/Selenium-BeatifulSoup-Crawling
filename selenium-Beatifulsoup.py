from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import pandas as pd

## 셀레니움 웹 드라이버 호출
driver = webdriver.Chrome("C:/Users/PC01/Desktop/CloudPlatformReport1/chromedriver_win32/chromedriver.exe")

## 해당 url 열기
driver.get("http://section.cgv.co.kr/theater/popup/r_TimeTable.aspx?")

## 페이지 소스 받아와 html 파싱
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

key_list = {}
cgv_list = {}
# 지역 00~13 [서울,경기,인천,부산,울산,대구,대전,광주,강원,경남,경북,전라,충청,제주]
# 지역별 CGV 고유 키값 가져오기
for i in range(14):
    num = ""
    if(i < 10):
        num = "0"+str(i)
    else :
        num = str(i)
    element = driver.find_element_by_id("rptRegion_ctl"+num+"_lbtnRegion").click()
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    theater_list = soup.select("#divWrap a")
    theater_list2 = []
    theater_name = []
    for c in range(len(theater_list)):
        theater_name.append(theater_list[c].string.strip())
        theater_list2.append(theater_list[c]["href"])
    val_list = []
    for l in theater_list2:
        val_list.append(l[37:])
    key_list[i] = val_list
    cgv_list[i] = theater_name

# 상영시간표
driver.get('http://www.cgv.co.kr/common/showtimes/iframeTheater.aspx?')

default_cgv = 'http://www.cgv.co.kr/common/showtimes/iframeTheater.aspx?'
cgv_name = "http://section.cgv.co.kr/theater/popup/r_TimeTable.aspx?"
cgv_html = requests.get(cgv_name).text
cgv_location_number=BeautifulSoup(cgv_html,'html.parser')

mv_list = {}
city = ["서울","경기","인천","부산","울산","대구","대전","광주","강원","경남","경북","전라","충청","제주"]

cnt = 0
mv_list = {"서울":{},
          "경기":{},
          "인천":{},
          "부산":{},
          "울산":{},
          "대구":{},
          "대전":{},
          "광주":{},
          "강원":{},
          "경남":{},
          "경북":{},
          "전라":{},
          "충청":{},
          "제주":{}}

for val in key_list.values():
    cnt2 = 0
    for i in val:
        theater = 'theatercode='+i+'&'
        date = 'date=20201017'
        cgvTime_html = requests.get(default_cgv + theater + date).text
        cgvSoup=BeautifulSoup(cgvTime_html,'html.parser')
        cgv=cgvSoup.select('div.sect-showtimes>ul>li')
        mv_list[city[cnt]][cgv_list[cnt][cnt2]] = {}
        cnt2 = cnt2 + 1
        for selector in cgv:
            movie_name=selector.select('strong')
            movie_times=selector.select('.info-timetable li a')
            mv_name = movie_name[0].string.strip()
            mv_list[city[cnt]][cgv_list[cnt][(cnt2-1)]][mv_name] = {}
            for movie in movie_times:
                try:
                    mv_list[city[cnt]][cgv_list[cnt][(cnt2-1)]][mv_name][movie['data-playstarttime'][:2]+":"+movie['data-playstarttime'][2:]] = movie['data-seatremaincnt']
                except:
                    print(movie)
    cnt = cnt + 1

print(mv_list)
df = pd.DataFrame(mv_list)
df.to_csv('output.csv')
