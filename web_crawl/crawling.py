import platform
import sys
import os
import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm
from selenium import webdriver
import time

url_load = pd.read_excel('blog_url.xlsx')

dict = {}  # 전체 크롤링 데이터를 담을 그릇
# ★수집할 글 갯수 정하기
number = 30
for i in tqdm(range(0, number)): 
    # 글 띄우기
    url = url_load['url'][i]
    driver = webdriver.Chrome("chromedriver")
    driver.get(url)   # 글 띄우기
    # 크롤링
    try :
        # iframe 접근
        driver.switch_to.frame('mainFrame')
        target_info = {}
        # 제목 크롤링 시작
        overlays = ".se-module.se-module-text.se-title-text"
        tit = driver.find_element_by_css_selector(overlays)          # title
        title = tit.text
        # 글쓴이 크롤링 시작
        overlays = ".nick"
        nick = driver.find_element_by_css_selector(overlays)         # nickname
        nickname = nick.text
        # 날짜 크롤링
        overlays = ".se_publishDate.pcol2"
        date = driver.find_element_by_css_selector(overlays)         # datetime
        datetime = date.text
        # 내용 크롤링
        overlays = ".se-component.se-text.se-l-default"
        contents = driver.find_elements_by_css_selector(overlays)
        content_list = []
        for content in contents:
            content_list.append(content.text)
        content_str = ' '.join(content_list)                         # content_str
        # 글 하나는 target_info라는 딕셔너리에 담기게 되고,
        target_info['title'] = title
        target_info['nickname'] = nickname
        target_info['datetime'] = datetime
        target_info['content'] = content_str
        # 각각의 글은 dict라는 딕셔너리에 담기게 됩니다.
        dict[i] = target_info
        time.sleep(1)
        # 크롤링이 성공하면 글 제목을 출력하게 되고,
        print(i, title)
        # 글 하나 크롤링 후 크롬 창을 닫습니다.
        driver.close()
    # 에러나면 현재 크롬창을 닫고 다음 글(i+1)로 이동합니다.
    except:
        driver.close()
        time.sleep(1)
        continue
    # 중간,중간에 파일로 저장하기
    if i == 30 or 50 or 80:
        # 판다스로 만들기
        result_df = pd.DataFrame.from_dict(dict, 'index')
        # 저장하기
        result_df.to_excel("blog_content.xlsx")
        time.sleep(3)
print('수집한 글 갯수: ', len(dict))
print(dict)