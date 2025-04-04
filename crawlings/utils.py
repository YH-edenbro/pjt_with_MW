import time
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from .models import Jusik

def crawl_tossinvest_opinions(search_keyword: str):

    # 크롬 드라이버 세팅
    options = Options()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    wait = WebDriverWait(driver, 10)

    # Toss Invest 접속
    driver.get("https://tossinvest.com/")

    # 검색창 열기
    actions = ActionChains(driver)
    actions.send_keys("/").perform() 
    
    time.sleep(1)
    
    # 검색어 입력
    actions = ActionChains(driver)
    actions.send_keys(search_keyword)
    actions.send_keys(Keys.ENTER)  # 엔터도 같이 누르기
    actions.perform()

    time.sleep(2)

    current_url = driver.current_url

    # '/order'를 제거하고 '/community'로 대체
    if current_url.endswith("/order"):
        community_url = current_url.replace("/order", "/community")
    else:
        # 예외 상황 고려: 다른 경로일 경우 그냥 커뮤니티 붙이기
        community_url = current_url.rstrip("/") + "/community"

    # 이동
    driver.get(community_url)

    # 스크롤 시작 시간 기록
    start_time = time.time()
    duration = 10  # 5초 동안만 스크롤
    titles = []  # 결과 제목을 저장할 리스트
    cnt = 0
    

    # 처음 주식 코드 추출
    time.sleep(1)

    html = driver.page_source

    # 6) BeautifulSoup 객체 생성(파서: html.parser)
    soup = BeautifulSoup(html, "html.parser")

    # 7) 검색 결과에서 제목 추출
    results = soup.select("div._1sivumi0")
    cnt = 0
    for result in results:
        # if result:
            # print(result)
        # print(result)
        cnt += 1
        title = result.select("span.tw-1r5dc8g0")
        # company_title = result.select_one("span.")

    
        
        if title is not None:
            stock_name = title[0].get_text().strip()
            stock_code = title[1].get_text().strip()


    while time.time() - start_time < duration:
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
        time.sleep(2)  # 너무 빠르게 하지 않도록 약간의 딜레이
        html = driver.page_source

    # 6) BeautifulSoup 객체 생성(파서: html.parser)
        soup = BeautifulSoup(html, "html.parser")

        # 7) 검색 결과에서 제목 추출
        results = soup.select("div.xdogm45")
        cnt = 0
        for result in results:
            # print(result)
            cnt += 1
            title = result.select_one("span._60z0ev0")
            post_time = result.select("span.tw-1r5dc8g0")
            
            if title is not None:
                title_text = title.get_text().strip()
                real_post_time = post_time[1].get_text().strip()
        if not Jusik.objects.filter(
            company=stock_name,
            company_code=stock_code,
            comment=title_text
            ).exists():
                Jusik.objects.create(
                    company=stock_name,
                    company_code=stock_code,
                    comment=title_text,
                    created_at=real_post_time
                )

    driver.quit()