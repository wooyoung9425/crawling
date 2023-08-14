from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import warnings
import time

#드라이버
warnings.filterwarnings('ignore')
options = webdriver.ChromeOptions()
# headless 옵션 설정
options.add_argument('headless')
options.add_argument("no-sandbox")
# 브라우저 윈도우 사이즈
options.add_argument('window-size=1920x1080')
# 사람처럼 보이게 하는 옵션들
options.add_argument("disable-gpu")   # 가속 사용 x
options.add_argument("lang=ko_KR")    # 가짜 플러그인 탑재
options.add_argument(
    'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36')  # user-agent 이름 설정
# 드라이버 위치 경로 입력
driver = webdriver.Chrome('chromedriver', chrome_options=options)
# 서울권 1763
url = 'https://academy.prompie.com/academies/search/?age=2%2C3%2C4&sort=review&province=1&page='
# 경기권 2227 / 543(7번째)
# url = 'https://academy.prompie.com/academies/search/?age=2%2C3%2C4&sort=review&province=9&page='
academy_list=[]
review_list=[]
review_count=1

no_detail_page=[]
good_list=[]
         
# nurak_list = list(range(972, 1201))
nurak_list = list(range(1,1608))

def craw(i):
    page_url = url+str(i)
    driver.get(page_url)
    time.sleep(2)
    soup = bs(driver.page_source, 'html.parser')
    list_li = soup.select('#academyList > li')
    
    for j in range(1, len(list_li)+1):
    # for j in range(1,len(list_li)+1):
        academy_dict={}
        # 리뷰와 맞추기 위한 학원 index값 1~끝까지
        academy_dict['academyIdx']=9*(i-1)+j
        xpath='//*[@id="academyList"]/li['+str(j)+']/div'
        try:
            academy_button = driver.find_element(By.XPATH,xpath)
            driver.execute_script("arguments[0].click();", academy_button)
            time.sleep(3)
        except:
            no_detail_page.append(f'{i}page의 {j}번째')
            continue
        soup = bs(driver.page_source, 'html.parser')

        # 학원이름
        try:
            academy_dict['academyName']=soup.select('#content > div.container.bg-white.border.mt-5.mb-5 > div.w-85.mx-lg-auto > div > div.d-flex.align-items-center > div.col-9.p-0 > div > div > h1 > span')[0].text
        except:
            continue
        # 학원도로명주소
        try:
            academy_dict['addr1']=soup.select('#content > div.container.bg-white.border.mt-5.mb-5 > div.w-85.mx-lg-auto > div > div.d-flex.align-items-center > div.col-9.p-0 > div > div > div:nth-child(2) > span.d-inline-block.mb-2.align-middle')[0].text
        except:
            academy_dict['addr1']=''
        # 학원지번주소
        try:
            academy_dict['addr2']=soup.select_one('#info > div > div.m-5.align-items-center > div.d-flex > div > span.d-block.mb-2').text.replace('  ','')[1:-1]
        except:
            academy_dict['addr2']=''
        # 학원전화번호
        try:
            academy_dict['phone']=soup.select_one('#content > div.container.bg-white.border.mt-5.mb-5 > div.w-85.mx-lg-auto > div > div.d-flex.align-items-center > div.col-9.p-0 > div > div > div:nth-child(3) > a > span').text
        except:
            academy_dict['phone']=''
        # 수강인원
        try:
            academy_dict['num_of_student']='/'.join(soup.select_one('#hakwon-info > div.pt-5 > div:nth-child(2) > div:nth-child(1) > div.col-8.pr-0 > span').text.replace('\n','').replace('  ','').split(','))
        except:
            academy_dict['num_of_student']=''
        # 수강연령
        try:
            academy_dict['grade']='/'.join(soup.select_one('#hakwon-info > div.pt-5 > div:nth-child(2) > div:nth-child(2) > div.col-8.pr-0 > span').text.replace('\n','').replace('  ','').split(','))
        except:
            academy_dict['grade']=''
        # 수강기간
        try:
            academy_dict['period']='/'.join(soup.select_one('#hakwon-info > div.pt-5 > div:nth-child(2) > div:nth-child(3) > div.col-8.pr-0 > span').text.replace('\n','').replace('  ','').split(','))
        except:
            academy_dict['period']=''
        # 수강과목
        try:
            academy_dict['subject']='/'.join(soup.select_one('#hakwon-info > div.pt-5 > div:nth-child(2) > div:nth-child(4) > div.col-8.pr-0.d-flex > span').text.replace('  ','').replace('\n','').split(','))
        except:
            academy_dict['subject'] = ''
        # 수강목적
        try:
            academy_dict['reson']=soup.select('#hakwon-info > div.pt-5 > div:nth-child(2) > div:nth-child(5) > div.col-8.pr-0.d-flex > span')[0].text.replace('\n','').replace('  ','')
        except:
            academy_dict['reson']=''
        # 편의시설
        try:
            facility=soup.select('#hakwon-info > div.pt-5 > div:nth-child(5) > div:nth-child(2) > div > div> h6')
            tmp=[]
            for content in facility:
                tmp.append(content.text.replace('  ','').replace('\n',''))
            academy_dict['facility']='/'.join(tmp)
        except:
            academy_dict['facility']=''
        # 학원 수업 정보       
        try:   
            info_list=soup.select('#hakwon-info > div.pt-5 > div:nth-child(8) > div:nth-child(2) > div > div > h6')
            tmp=[]
            for info in info_list:
                tmp.append(info.text.replace('  ','').replace('\n',''))
            academy_dict['info']='/'.join(tmp)
        except:
            academy_dict['info'] = ''
        academy_list.append(academy_dict)
        review_none = soup.select_one('#review-container > div.text-center.my-10')
        if  review_none==None:
            # 학원 리뷰 있으면 가져오기
            review_num=int(soup.select_one('#review-container > h5 > span').text)
            review_button = driver.find_element(By.XPATH, '//*[@id="content"]/div/ul/li[3]/a')
            driver.execute_script("arguments[0].click();", review_button)
            # 5로나눳을때 나눠떨어지면 나머지 아니면 +1
            if review_num%5==0: review_page=review_num//5 
            else: review_page= review_num//5+1
            print('review 개수 : ', review_num)
            print('review 페이지 개수 : ', review_page)
            check=0
            for p in range(1, review_page+1):
                if p==review_page:
                    sub_review_num=int(review_num%5)
                else:
                    sub_review_num = 5
                
                if p != 1: 
                    if p%5==0:
                        if check==0:
                            next_page_xpath=6
                        else:
                            next_page_xpath=7
                    else: 
                        next_page_xpath = p%5+1
                    
                    if check ==0:
                        if next_page_xpath!=2:
                            review_button = driver.find_element(By.XPATH, '//*[@id="reviewListContainer"]/nav/ul/li['+str(next_page_xpath)+']/a')  
                        else:
                            check=1
                            review_button = driver.find_element(By.XPATH, '//*[@id="reviewListContainer"]/nav/ul/li[7]/a')
                            time.sleep(1)
                            driver.execute_script("arguments[0].click();", review_button)
                            time.sleep(2)
                            review_button=driver.find_element(By.XPATH, '//*[@id="reviewListContainer"]/nav/ul/li[2]/a')
                    else:
                        if next_page_xpath!=3:
                            review_button = driver.find_element(By.XPATH, '//*[@id="reviewListContainer"]/nav/ul/li['+str(next_page_xpath)+']/a')
                        else:
                            review_button = driver.find_element(By.XPATH, '//*[@id="reviewListContainer"]/nav/ul/li[8]/a')
                            time.sleep(1)
                            driver.execute_script("arguments[0].click();", review_button)
                            time.sleep(2)
                            review_button=driver.find_element(By.XPATH, '//*[@id="reviewListContainer"]/nav/ul/li[3]/a')
                        
                    time.sleep(1)
                    driver.execute_script("arguments[0].click();", review_button)
                    time.sleep(2)
                    print(p, f'-> [{next_page_xpath}]')

                    soup = bs(driver.page_source, 'html.parser')
                print('마지막 페이지에서 확인:', sub_review_num)
                for k in range(1,sub_review_num+1):
                    review_dict={}
                    review_dict['reviewIdx']=review_count
                    review_dict['academyIdx']=9*(i-1)+j
                    review_dict['year']=soup.select_one('#reviewListContainer > div:nth-child('+str(k)+') > div.mb-3 > div > div:nth-child(2) > ul > li:nth-child(5) > span').text
                    review_dict['grade']=soup.select_one('#reviewListContainer > div:nth-child('+str(k)+') > div.mb-3 > div > div.rounded-circle.u-m-direct-avatar.border.font-footnote.text-primary.p-2.mr-3.text-center > span').text
                    review_dict['summary']=soup.select_one('#reviewListContainer > div:nth-child('+str(k)+') > div.d-flex.justify-content-start.align-items-start > div.ml-7 > h5').text
                    review_dict['advantage']=soup.select('#goodText')[k-1].text
                    review_dict['disadvantage']=soup.select('#badText')[k-1].text
                    review_dict['review'] = review_dict['summary']+'/'+review_dict['advantage']+'/'+review_dict['disadvantage']
                    # print(review_dict)
                    review_list.append(review_dict)
                    review_count += 1
        # else:
        #     # 학원 리뷰 없으므로 학원 정보만 가져온다.   
        #     continue
        print(f'{i}페이지 {j}번째 학원')
        time.sleep(2)
        driver.get(page_url)
        time.sleep(1)
count=0
# for i in search_list: 
for i in nurak_list: 
    if count !=16:
        count+=1     
    else:
        count=0
        time.sleep(600)
    try:
        craw(i)
    except:
        good_list.append(str(i))
        continue
    
print('----------------------------------------------------')
print(no_detail_page)
print('----------------------------------------------------')
print(good_list)
print('----------------------------------------------------')
academy = pd.DataFrame(academy_list, columns=['academyIdx','academyName','addr1','addr2','phone','num_of_student','grade','period','subject','reson','facility','info'])
academy.to_excel('./academy/academy.xlsx', index=False) 
review = pd.DataFrame(review_list, columns=['reviewIdx', 'academyIdx','year','grade','summary','advantage','disadvantage','review'])
review.to_excel('./review/review.xlsx', index=False)
print(review)
print(len(academy))