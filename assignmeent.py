from urllib import parse
from bs4 import BeautifulSoup
from matplotlib import pyplot as plt
import requests
import time
import random
import pandas as pd
import numpy as np


base_url = 'https://movie.naver.com/movie/point/af/list.nhn?&page={}'

comment_list = []
for page in range(1, 100):
    url = base_url.format(page)
    res = requests.get(url)
    if res.status_code == 200:
        soup = BeautifulSoup(res.text, 'lxml')
        tds = soup.select('table.list_netizen > tbody > tr > td.title')
        for td in tds:
            movie_title = td.select_one('a.movie').text.strip()
            link = td.select_one('a.movie').get('href')
            link = parse.urljoin(base_url, link)
            score = td.select_one('div.list_netizen_score > em').text.strip()
            comment = td.select_one('br').next_sibling.strip()
            # 리스트에 저장
            comment_list.append((movie_title, link, score, comment))
        interval = round(random.uniform(0.2, 1.2), 2)
        time.sleep(interval)
df = pd.DataFrame(comment_list, columns=['Title', 'Link', 'Score', 'Comment'])
state = df.groupby('Title')['Score'].describe()
df.head()
choice = input()
if choice == 'find':
    a = input()
    find_a = df['Title'] == a
    find = df[find_a]
    print(a, '의 검색 결과입니다.')
    print(find)
elif choice == 'all':
    print(df)
elif choice == 'state':
    print(state)
elif choice == 'gragph':
    x = df['Title']
    y = df['Score']
    plt.bar(x, y, align = 'center', alpha = 0.7, color = 'red')
    plt.xticks('Title')
    plt.ylabel('Score')
    plt.title('평점')
    plt.show()



