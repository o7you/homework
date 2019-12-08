import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta                      # 'dbsparta'라는 이름의 db를 만듭니다.

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://www.genie.co.kr/chart/top200?ditc=D&rtm=N&ymd=20191208',headers=headers)
#ctrl+alt+i->파이썬 정렬
#순위 / 곡 제목 / 가수 (네이버영화 실습과 동일하게 저장)
soup = BeautifulSoup(data.text, 'html.parser')
genie = soup.select('#body-content > div.newest-list > div > table > tbody > tr')
#body-content > div.newest-list > div > table > tbody > tr:nth-child(1) > td.info > a.artist.ellipsis
rank = 1
for g in genie:
    g_title = g.select_one('td.info > a.title.ellipsis')
    g_singer = g.select_one('td.info > a.artist.ellipsis')
#for g in genie:
    #rank = g.select_one('td.number').text.split(' ')[0].strip()
    #g_title = g.select_one('td.info > a.title.ellipsis').text.strip()
    #g_singer = g.select_one('td.info > a.artist.ellipsis').text
    #doc = {
            #'rank': rank,
            #'title': title,
            #'singer': singer
        #}
        #db.ggenie.insert_one(doc)

    if g_title is not None:
        title = g_title.text.strip()
        singer = g_singer.text

        doc = {
            'rank': rank,
            'title': title,
            'singer': singer
        }
        db.ggenie.insert_one(doc)
        rank += 1