from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import warnings
import time
warnings.filterwarnings('ignore')
options = webdriver.ChromeOptions()
# headless 옵션 설정
# options.add_argument('headless')
options.add_argument("no-sandbox")
# 브라우저 윈도우 사이즈
options.add_argument('window-size=1920x1080')
# 사람처럼 보이게 하는 옵션들
options.add_argument("disable-gpu")   # 가속 사용 x
options.add_argument("--lang=ko_KR")    # 가짜 플러그인 탑재
options.add_argument(
    'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36')  # user-agent 이름 설정
options.add_argument("--remote-allow-origins=*")
# 드라이버 위치 경로 입력
driver = webdriver.Chrome('chromedriver', chrome_options=options)

# login_url = 'https://www.gangmom.kr/sign-in'
# driver.get(login_url)
# driver.implicitly_wait(10)

# 광고 닫기 클릭
# content = driver.find_element(
#     By.CLASS_NAME, 'buttr-animation-lukeurowwz-gvkoiyyukiwd')
# driver.switch_to.frame(content)
# backdrop_element = driver.find_element('xpath',
#                                        "/html/body/div[1]/div/div[2]/div[1]")
# driver.execute_script("arguments[0].click();", backdrop_element)
# driver.implicitly_wait(10)

# 로그인
# login = driver.find_element(
#     By.XPATH, '//*[@id="__layout"]/div/div/div[1]/div/div/button')
# login.click()
# driver.find_element('name', 'loginKey').send_keys('wooyoung9425@nate.com')
# driver.find_element('name', 'password').send_keys('dndld4756?')
# time.sleep(3)
# checkbox = driver.find_element(By.XPATH, '//*[@id="staySignedIn--3"]')
# print(checkbox)
# driver.execute_script("arguments[0].click();", checkbox)
# time.sleep(3)
# driver.find_element(
#     By.XPATH, '//*[@id="mainContent"]/div/div/form/div[4]/button[1]').click()
# time.sleep(3)

result = []
# 리뷰
for acaId in range(168, 5001):
    url = 'https://www.gangmom.kr/institute/'+str(acaId)+'?from=review'
    driver.get(url)
    time.sleep(5)
    # wait2 = WebDriverWait(driver, 30)
    # wait2.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.navigation')))
    soup = bs(driver.page_source, 'html.parser')
    print(url)
    # 결과
    # 해당 학원의 리뷰개수 확인
    review_num_check = soup.select_one(
        '#review > div > div > div.flex-space-bet.align-center > a:nth-child(1) > h2 > span')
    # '#__layout > div > div > div:nth-child(2) > div > div.navigation > div > a:nth-child(2) > span')
    print("!!!!!!!!!!!!!!!!!!!!!!!!!", review_num_check)

    if review_num_check == None:
        continue
    else:
        review_num = review_num_check.text.replace(
            ' ', '').replace('\n', '').split('총')[1][:-1]
    print(review_num)
    page_num = int(review_num)//20+1
    academyName = soup.select(
        '#__layout > div > div > div:nth-child(2) > div > section.header__wrapper > div > div > div > div.header__heading > h1')[0].text.replace(' ', '').replace('\n', '')
    academyAddr = soup.select(
        '#__layout > div > div > div:nth-child(2) > div > section.header__wrapper > div > div > div > h2')[0].text.replace('\n', '')
    academySubject_list = soup.select(
        '#info > div > div > div.info__subjects.info-box > div.info-box-content.--wd-200 > p > span.info__subjects__list__label')
    academySubject = ''
    for k in range(len(academySubject_list)):
        if k == 0:
            academySubject = academySubject_list[k].text
        else:
            academySubject = academySubject + ',' + academySubject_list[k].text
    print(academySubject)
    print('@@@@@@', page_num, academyName, academyAddr, academySubject)
    time.sleep(3)
    for i in range(1, page_num+1):
        url = 'https://www.gangmom.kr/institute/' + \
            str(acaId)+'/review?sort&page='+str(i)
        driver.get(url)
        time.sleep(3)
        soup = bs(driver.page_source, 'html.parser')
        print(url)
        nickName_list = soup.select(
            '#__layout > div > div > div > div:nth-child(2) > div > div > div.review-list > div > div > div:nth-child(1) > div > div.flex-row.review__row.mb-12 > div.review__auth__author')
        date_list = soup.select(
            '#__layout > div > div > div > div:nth-child(2) > div > div > div.review-list > div > div > div:nth-child(1) > div > div.flex-row.review__row.mb-12 > div.review__auth__created-at')
        grade_list = soup.select(
            '#__layout > div > div > div > div:nth-child(2) > div > div > div.review-list > div > div > div.review__student.review__row.mb-40 > div.flex-row.review__student-info > span.review__age-label')
        review1_list = soup.select(
            '#__layout > div > div > div > div:nth-child(2) > div > div > div.review-list > div > div > div.review__title.mb-40 > text-highlight')
        review2_list = soup.select(
            '#__layout > div > div > div > div:nth-child(2) > div > div > div.review-list > div > div > div.flex-space-bet.review__content.mb-40-pc > div.review__content__pros > text-highlight')
        review3_list = soup.select(
            '#__layout > div > div > div > div:nth-child(2) > div > div > div.review-list > div > div > div.flex-space-bet.review__content.mb-40-pc > div.review__content__cons > text-highlight')
        for j in range(len(nickName_list)):
            nickName = nickName_list[j].text
            date = date_list[j].text.replace('  ', '').replace('\n', '')
            grade = grade_list[j].text.replace(' ', '').split(':')[1]
            review1_text = review1_list[j].text.replace(
                '  ', '').replace('\n', '')
            review2_text = review2_list[j].text.replace(
                '  ', '').replace('\n', '')
            review3_text = review3_list[j].text.replace(
                '  ', '').replace('\n', '')
            review = review1_text+'\n'+review2_text+'\n'+review3_text
            # 펼치기 클릭
            # button1 = driver.find_elements(By.XPATH,
            #                                '//*[@id = "__layout"]/div/div/div/div[2]/div/div/div[3]/div['+str(j+1)+']/div/div[6]')
            # driver.execute_script("arguments[0].click();", button1[0])
            # time.sleep(5)
            # subject = soup.select(
            #     '#__layout > div > div > div > div:nth-child(2) > div > div > div.review-list > div > div > div:nth-child(6) > div.review__extra-info > div:nth-child(2) > div.review__extra-info__value > span')

            print(nickName, date, grade, '\n', review)
            result.append({
                'academyIndex': acaId,
                'academyName': academyName,
                'academySubject': academySubject,
                'academyAddr': academyAddr,
                'nickName': nickName,
                'date': date,
                'grade': grade,
                'review': review,
            })

print(result)
df = pd.DataFrame(result, columns=['academyIndex', 'academyName',
                  'academySubject', 'academyAddr', 'nickName', 'date', 'grade', 'review'])
# df.to_csv('./haksoop/gangName_18.csv', encoding='utf-8')
df.to_excel('./haksoop/gangName_18.xlsx')
