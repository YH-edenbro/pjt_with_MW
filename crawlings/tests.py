import os
import sys
import time
import django

# ✅ 현재 파일 위치 기준으로 프로젝트 루트 경로 설정
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))          # crawlings/
BASE_DIR = os.path.dirname(CURRENT_DIR)                           # yhmw/ ← settings.py 있는 경로
sys.path.append(BASE_DIR)                                         # yhmw 상위 경로 추가

# ✅ Django 환경 설정
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "yhmw.settings")  # settings.py 있는 프로젝트 이름
django.setup()

from crawlings.models import Jusik  # 너의 모델

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from urllib.parse import urlparse


def crawl_tossinvest_opinions(search_keyword: str):
    options = Options()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    driver.get("https://tossinvest.com/")
    actions = ActionChains(driver)
    actions.send_keys("/").perform()
    time.sleep(1)

    actions = ActionChains(driver)
    actions.send_keys(search_keyword)
    actions.send_keys(Keys.ENTER)
    actions.perform()
    time.sleep(2)

    current_url = driver.current_url
    parsed_url = urlparse(current_url)
    path_parts = parsed_url.path.strip('/').split('/')
    stock_name = path_parts[0] if len(path_parts) >= 2 else "UNKNOWN"
    stock_code = path_parts[1] if len(path_parts) >= 2 else "UNKNOWN"

    if current_url.endswith("/order"):
        community_url = current_url.replace("/order", "/community")
    else:
        community_url = current_url.rstrip("/") + "/community"

    driver.get(community_url)
    time.sleep(3)

    start_time = time.time()
    duration = 10  # 스크롤 시간 (초)

    while time.time() - start_time < duration:
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
        time.sleep(2)
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        comment_blocks = soup.select("div.xdogm45")
        for block in comment_blocks:
            content = block.select_one("span._60z0ev0")
            timestamp = block.select_one("time")

            if content:
                content_text = content.get_text().strip()
                timestamp_text = timestamp.get_text().strip() if timestamp else "시간 정보 없음"

                if not Jusik.objects.filter(
                    company=stock_name,
                    company_code=stock_code,
                    comment=content_text
                ).exists():
                    Jusik.objects.create(
                        company=stock_name,
                        company_code=stock_code,
                        comment=content_text,
                        created_at=timestamp_text
                    )

    driver.quit()
    print("✅ 크롤링 및 DB 저장 완료")


# 테스트 실행
if __name__ == "__main__":
    crawl_tossinvest_opinions("삼성전자")
