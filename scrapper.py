from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
import requests
from bs4 import BeautifulSoup
import time
# from urllib.parse import urlparse, quote
# import json

# usb 가져오지 못한다는 에러 자꾸 떠서 추가함
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
browser = webdriver.Chrome(options=options)

# 각 병원정보 클릭
# information = browser.find_element_by_xpath('//*[@id="_list_scroll_container"]/div/div/div[2]/ul/li[1]/div[2]/a[1]')
# information.click()

def extract_hospital(html):
    # 거리
    distance = html.find("em").get_text()
    # 이름
    title = html.find("span", class_="QLp9G").get_text()
    # 영업시간
    when = html.find("div", class_="_1D4xp")
    if when is None:
        final_when = "정보가 없어요"
    else:
        final_when = when.get_text()    
# 주의) 정보가 없는 게 중간에 존재하면 오류뜨고 거기서 멈출 수 있음!! none일 때 해결법 고려해야 함
# 계속 get_text()가 NoneType에 쓰여서 문제가 됐으니 그걸 막기 위해 get_text는 나중에 쓰기로!!
       
    # 링크
    last_link = html.select_one("a")["href"].replace("photo" , "home")
    return {'distance': distance, "title": title, "when": final_when, "link": f"https://m.place.naver.com{last_link}"}

def final_location(location, word):
   url = f"https://dapi.kakao.com/v2/local/search/address.json?query={location}"
   kakao_key = "본인 키 쓰세요" # 보안주의~
   result = requests.get(url, headers={"Authorization":f"KakaoAK {kakao_key}"})
   json_obj = result.json()
   # print(json_obj)
   x = json_obj['documents'][0]['x']
   y = json_obj['documents'][0]['y']
   final_url = f"https://m.place.naver.com/hospital/list?x={x}&y={y}&query={word}"
   return final_url

def scrap_hospital(location, word): # homepage에서 받을 정보(치과, 내과, 한의원 등)
    URL = final_location(location, word)
    browser.get(URL)
    time.sleep(3)

    # 목록보기 클릭
    button = browser.find_element_by_class_name("_31ySW ")
    button.click()
    time.sleep(3)

    # 정확도순 클릭
    filter = browser.find_element_by_xpath('//*[@id="_list_scroll_container"]/div/div/div[1]/div/div/div/div/div/span[1]/a')
    filter.click()
    
    # 거리순으로 변경
    short_way = browser.find_element_by_xpath('//*[@id="_list_scroll_container"]/div/div/div[1]/div/div/div[2]/div/ul/li[2]/a')
    short_way.click()
    time.sleep(5)
    # 와 기다리지 않아서 이랬던거야? 너무해..;;;;

    inf = []
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    hospitals = soup.find_all("li", class_="_2JXhh")
    # print(len(hospitals)) # 50개니까 완전 충분함
    for hospital in hospitals:
        information = extract_hospital(hospital)
        inf.append(information)
    return inf   

# final_function = scrap_hospital()
# print(final_function)
