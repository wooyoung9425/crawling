from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import warnings
import random
import time
warnings.filterwarnings('ignore')
options = webdriver.ChromeOptions()
# headless 옵션 설정
options.add_argument('headless')
options.add_argument("no-sandbox")
# 브라우저 윈도우 사이즈
options.add_argument('window-size=1920x1080')
# 사람처럼 보이게 하는 옵션들
options.add_argument("disable-gpu")   # 가속 사용 x
options.add_argument("--lang=ko_KR")    # 가짜 플러그인 탑재
options.add_argument(
    'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36')  # user-agent 이름 설정
# 드라이버 위치 경로 입력
driver = webdriver.Chrome('chromedriver', chrome_options=options)
start = 11
end = start + 1011
result = []
for i in range(start, end):
    url = 'https://www.allaca.net/academy/view?academyNo='+str(i)
    driver.get(url)
    time.sleep(3)
    soup = bs(driver.page_source, 'html.parser')
    if i == start:
        time.sleep(1)
        driver.find_element(
            By.XPATH, '//*[@id="app"]/div[1]/div[2]/div[2]/div/div/div/div[3]/button[3]').click()
        time.sleep(1)
    academy_check = soup.select_one(
        '#scroll_top > div > div > div > div.flex_col > div.flex_col_con > div > div > div.name_all > p')
    if academy_check != None:
        try:
            academyName = soup.select_one(
                '#scroll_top > div > div > div > div.flex_col > div.flex_col_con > div > div > div.name_all > p').text
            subject = soup.select_one(
                '#scroll_top > div > div > div > div.flex_col > div.flex_col_con > div > div > div:nth-child(3) > p').text
            grade = soup.select_one(
                '#scroll_top > div > div > div > div.flex_col > div.flex_col_con > div > div > div:nth-child(4) > p').text
            addr = soup.select_one(
                '#scroll_top > div > div > div > div.flex_col > div.flex_col_con > div > div > div.address > p:nth-child(2)').text

            homepage_check = soup.select_one(
                '#scroll_top > div > div > div > div.flex_col > div.flex_col_con > div > div > div.small > div.url > a > p')
            if homepage_check == None:
                homepage = ''
            else:
                homepage = homepage_check.text

            blob_check = soup.select_one(
                '#scroll_top > div > div > div > div.flex_col > div.flex_col_con > div > div > div.small > div:nth-child(2) > a > p')
            if blob_check == None:
                blog = ''
            else:
                blog = blob_check.text
            print(blog)

            phone = soup.select_one(
                '#scroll_top > div > div > div > div.flex_col > div.flex_col_con > div > div > div.small > div.phone > p').text

            intro_list = soup.select(
                '#scroll_top > div > div > div > div.flex_col > div.flex_col_con > div > div > div.small > div.academy_intro.editor > div > p')

            intro = ''
            if intro_list == []:
                intro = ''
            else:
                for i in range(len(intro_list)):
                    intro = intro + intro_list[i].text+'\n'
            time.sleep(1)
            driver.find_element(
                By.XPATH, '//*[@id="scroll_top"]/div/div/div/div[1]/div[2]/div/ul/li[6]/button').click()
            time.sleep(1)
            driver.execute_script(
                "window.scrollTo(0,document.body.scrollHeight)")
            time.sleep(5)
            soup = bs(driver.page_source, 'html.parser')
            review_list = soup.select(
                '#scroll_top > div > div > div > div.flex_col > div.flex_col_con > div > div > div.contents.tab05 > div > ul > li')
            for i in range(len(review_list)):
                name = review_list[i].find('span').text
                review = review_list[i].find('p').text
                result.append({
                    'academyName': academyName,
                    'subject': subject,
                    'grade': grade,
                    'addr': addr,
                    'homepage': homepage,
                    'blog': blog,
                    'phone': phone,
                    'intro': intro,
                    'name': name,
                    'review': review
                })

        except:
            continue
    else:
        continue
    rand_value = random.randint(1, 30)
    time.sleep(rand_value)

df = pd.DataFrame(
    result, columns=['academyName', 'subject', 'grade', 'addr', 'homepage', 'blog', 'phone', 'intro', 'name', 'review'])
print(df)

df.to_excel('저장위치/저장파일명.xlsx')
