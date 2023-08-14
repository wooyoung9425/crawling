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
url = 'https://www.allaca.net/teacher/view?teacherNo='
start = 6
review_list = []
for i in range(start, 11548):
    teacher_url = url+str(i)
    driver.get(teacher_url)
    if i == start:
        # 다시보지 않기 클릭
        time.sleep(1)
        driver.find_element(
            By.XPATH, '//*[@id="app"]/div[1]/div[2]/div[2]/div/div/div/div[3]/button[3]').click()
        time.sleep(1)

    time.sleep(1)
    soup = bs(driver.page_source, 'html.parser')
    time.sleep(1)
    check = soup.select_one(
        '#scroll_top > div.tchr_page.h > div > div > div.board.detail > ul > li > div > div.col.txt.clearfix > div.flex_box > div > p')
    print(i, check)

    if check == None:
        print(i, '학원이 없어')
        continue
    else:
        if check.text == '':
            print(i, '선생은 있지만 학원이 없어')
            continue
        else:
            teacher_name = soup.select(
                '#scroll_top > div.tchr_page.h > div > div > div.board.detail > ul > li > div > div.col.txt.clearfix > div.line.first > p')[0].getText()
            text = teacher_name.split(' ')
            grade = text[-2]
            subject = text[-1]
            if '본원' in teacher_name:
                teacher = '본원 선생님'
            else:
                teacher = teacher_name[:3]
            academyName = check.text
            print(academyName, ' ', teacher, grade, subject)
            time.sleep(1)
            driver.find_element(
                By.XPATH, '//*[@id="scroll_top"]/div[1]/div/div/div[2]/div/ul/li[2]/button').click()
            time.sleep(1)
            soup = bs(driver.page_source, 'html.parser')
            # 추천글 있는지 확인 필요
            check2 = soup.select(
                '#scroll_top > div.tchr_page.h > div > div > div.sbj_list > ul > div > div > div.contents.tab05 > div > ul > li')
            if check2 == []:
                review_list.append({
                    'teacherNo': i,
                    'academyName': academyName,
                    'teacher': teacher,
                    'grade': grade,
                    'subject': subject,
                    'nickName': '',
                    'review': ''
                })

                continue
            else:
                for li in check2:
                    nickName = li.find('span').text
                    review = li.find('p').text
                    print(nickName, review)
                    review_list.append({
                        'teacherNo': i,
                        'academyName': academyName,
                        'teacher': teacher,
                        'grade': grade,
                        'subject': subject,
                        'nickName': nickName,
                        'review': review
                    })

df_review = pd.DataFrame(review_list, columns=['teacherNo',
                         'academyName', 'teacher', 'grade', 'subject', 'nickName', 'review'])
print(df_review)
df_review.to_excel('저장위치/저장파일명.xlsx', index=False)
