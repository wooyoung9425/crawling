import openai
import argparse
import pandas as pd
import time
import math

from openai.api_resources import model

def call_chatgpt_api(messages):
  try:
    response = openai.ChatCompletion.create(
        model=model,
        messages = messages
    )
    return response['choices'][0]['message']['content']
  except openai.error.RateLimitError as e:
    return ""
def review_washing(answer):
  try:
    if '"' in answer:
      answer_list = answer.split('"')
      answer = answer_list[len(answer_list)-2]
    if ':' in answer:
      answer = answer.split[':'][1]
    if '\n' in answer:
      answer = answer.split('\n')[1]
  except:
    answer = answer
  return answer

if __name__=='__main__':
    # chatgpt api 키 설정
    API_KEY = 'chatgpt api 키'
    openai.api_key = API_KEY
    # 모델 선택
    model="gpt-3.5-turbo"


    # csv 읽어오기
    input_csv='input data 위치'
    data = pd.read_excel(input_csv)
    col = ['reviewId','academyIndex','academyName','academySubject','academyAddr','nickName','date','grade','review','academyid']

    # 리뷰 아이디 넣기
    review_id =list(range(0,len(data)))
    df_review_id = pd.DataFrame(review_id, columns=['reviewId'])
    data = pd.concat([df_review_id, data], axis=1)
    review=data[['reviewId','review']]
    review
    new_review = []
    query = 'review column의 전체 글들을 의미는 같지만 한가지의 학원 평가문장으로 바꿔주세요.'

    new_review=[]
    for num, row in review.iterrows():
        if row.reviewId > 12166:
            review_text = row.review
            messages = [
                {"role" : "system", "content":"You are a helpful assistant."},
                {"role" : "user", "content":query+review_text}
            ]
            answer = call_chatgpt_api(messages)
            if answer == "":
                continue
            else:
                answer = review_washing(answer)
                print(row['reviewId'], answer)
                new_review.append({'reviewId':row['reviewId'], 'newReview':answer})
        else:
            continue

    df_new_review = pd.DataFrame(new_review, columns =['reviewId','newReview'])
    merge_result = pd.merge(data, df_new_review, how='inner', on='reviewId')
    merge_result.to_excel('저장위치/저장파일 이름')