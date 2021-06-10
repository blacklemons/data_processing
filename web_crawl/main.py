import platform
import sys
import os
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
import time

def scroll_down(driver):
    driver.execute_script("window.scrollTo(0,999999999)")
    time.sleep(1)


# query_text = input("크롤링 할 맛집은 ? (형식 : 00맛집): ")
query_text = "강남맛집"
# 크롤링을 위해 chrome.exe 를 가져온다.
path="chromedriver.exe"

driver = webdriver.Chrome()

driver.get("https://www.naver.com/")
time.sleep(2)

element = driver.find_element_by_id("query")
# print(element)
element.send_keys(query_text)
element.submit()
time.sleep(2)

# 강남맛집 검색 - view - 필터 - 블로그 - 기간
# driber.find_element_by_xpath(//*[@id="lnb"]/div[1]/div/ul/li[2]/a)
driver.find_element_by_link_text("VIEW").click()
time.sleep(2)
driver.find_element_by_link_text("블로그").click()
time.sleep(2)
driver.find_element_by_link_text("옵션").click()
time.sleep(2)
driver.find_element_by_link_text("1개월").click()
time.sleep(2)

for i in range(10):
    scroll_down(driver)
# URL 크롤링
class_articles=".api_txt_lines.total_tit"
url_link = driver.find_elements_by_css_selector(class_articles)
# print(url_link)

url_list = []
title_list = []
for article in url_link:
    url = article.get_attribute('href')
    url_list.append(url)
# print("=========")
# print(url_list)
# print("=========")

for article in url_link:
    title = article.text
    title_list.append(title)
# print("=========")
# print(title_list)
# print("=========")
print(f'url갯수 : {len(url_list)}')
print(f'title갯수 : {len(title_list)}')

# 데이터프레임으로 변환
df = pd.DataFrame({'url':url_list, 'title':title_list})

# 엑셀로 저장
df.to_excel('blog_url.xlsx')
print('Fin Save')