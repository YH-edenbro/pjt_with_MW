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

def crawl_tossinvest_opinions(search_keyword: str):

    # 크롬 드라이버 세팅
    options = Options()
    options.add_argument("--start-maximized")
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
    actions.send_keys("삼성전자")
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
    duration = 5  # 5초 동안만 스크롤

    while time.time() - start_time < duration:
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
        time.sleep(0.5)  # 너무 빠르게 하지 않도록 약간의 딜레이


    # 3초 대기 (변화 확인용)
    time.sleep(3)

    # 페이지 로딩 대기
    time.sleep(5)

    # # 페이지의 HTML 소스 가져오기
    # html = driver.page_source

    # # BeautifulSoup 객체 생성(파서: html.paresr)
    # soup = BeautifulSoup(html, "html.parser")

    # results = soup.select("div.notranslate")
    # company =  []


    driver.quit()

crawl_tossinvest_opinions("삼성전자")
