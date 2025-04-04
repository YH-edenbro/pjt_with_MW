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

def crawl_tossinvest_opinions(search_keyword: str, count: int = 15, output_csv: str = "comments.csv"):
    """TossInvest 커뮤니티에서 특정 종목 의견 텍스트를 크롤링해서 CSV로 저장하는 함수"""

    # 크롬 드라이버 세팅
    options = Options()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    wait = WebDriverWait(driver, 10)

    try:
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


        while len(comments) < count and scroll_count < 20:
            time.sleep(2)

            posts = driver.find_elements(By.CSS_SELECTOR, "div[class*='PostPreview_container']")

            for post in posts:
                try:
                    # 텍스트만 있는지 확인
                    text_blocks = post.find_elements(By.CSS_SELECTOR, "p")
                    if text_blocks and post.find_elements(By.CSS_SELECTOR, "img") == []:
                        full_text = "\n".join([p.text.strip() for p in text_blocks if p.text.strip()])
                        if full_text:
                            comments.add(full_text)
                            if len(comments) >= count:
                                break
                except:
                    continue

            # 스크롤 다운
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            scroll_count += 1

        # 결과 저장
        with open(output_csv, "w", encoding="utf-8-sig", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Opinion"])
            for comment in list(comments)[:count]:
                writer.writerow([comment])

        print(f"✅ '{search_keyword}'의 텍스트 기반 의견 {len(comments)}개를 '{output_csv}'에 저장 완료!")

    finally:
        driver.quit()

crawl_tossinvest_opinions("삼성전자", count=15, output_csv="삼성전자_comments.csv")
