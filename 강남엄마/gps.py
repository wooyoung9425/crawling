import pandas as pd
from urllib.request import Request
from urllib.request import urlopen
from urllib import parse
from urllib.error import HTTPError
import json
import requests
import pandas as pd
from tqdm import tqdm

# input data
gangnam = pd.read_excel('/content/drive/MyDrive/학숲데이터정제/강남엄마/gangNam_4000.xlsx')
gangnam = gangnam.drop(labels='Unnamed: 0', axis=1)
gn_aca = gangnam[['academyIndex','academyName','academyAddr']]
gn_aca = gn_aca.drop_duplicates()

# 지번-> gps


client_id = 'NAVER 오픈 api 아이디'
client_pw = 'NAVER 오픈 api 비밀번호'
api_url = 'https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode?query='

geo = []
for index, addr in zip(gn_aca['academyIndex'], gn_aca['academyAddr']):
    addr_url = parse.quote(addr)
    url = api_url+addr_url
    request = Request(url)
    request.add_header('X-NCP-APIGW-API-KEY-ID', client_id)
    request.add_header('X-NCP-APIGW-API-KEY', client_pw)

    try:
        response = urlopen(request)
    except HTTPError as e:
        print('HTTP Error!')
        latitude = None
        longitude = None
    else:
        rescode = response.getcode()
        if rescode == 200:
            response_body = response.read().decode('utf-8')
            response_body = json.loads(response_body)   # json
            if response_body['addresses'] == []:
                print(addr, "'result' not exist!")
                latitude = None
                longitude = None
            else:
                latitude = response_body['addresses'][0]['y']
                longitude = response_body['addresses'][0]['x']
                # print("Success!")
        else:
            print('Response error code : %d' % rescode)
            latitude = None
            longitude = None
    print(index, latitude, longitude)
    geo.append([index, latitude, longitude])

df_geo = pd.DataFrame(geo, columns = ['academyIndex','lat','lng'])
df_geo = df_geo.dropna()

# 기존 data와 gps데이터 합치기
merge = pd.merge(gn_aca, df_geo, how='outer', on='academyIndex')
merge.to_excel('저장할 위치/저장 파일명.xlsx')

# gps-> 지번
addr2 = []
none_list = []
academyCsv=pd.read_csv('적용할 파일')

for index, aca in tqdm(academyCsv.iterrows()):
    latitude = aca['lat']
    longitude = aca['lng']

    coords = f"{longitude},{latitude}"
    output = "json"
    orders = 'addr'
    sourcecrs = "epsg:4326"
    endpoint = "https://naveropenapi.apigw.ntruss.com/map-reversegeocode/v2/gc"
    url = f"{endpoint}?request=coordsToaddr&coords={coords}&sourcecrs={sourcecrs}&output={output}&orders={orders}"
    headers = {
        "X-NCP-APIGW-API-KEY-ID": client_id,
        "X-NCP-APIGW-API-KEY": client_pw,
    }
    res = requests.get(url, headers=headers)
    result = res.json()

    if result.get('status').get('code') == 0:
        area1 = result.get('results')[0].get('region').get('area1').get('name')
        area2 = result.get('results')[0].get('region').get('area2').get('name')
        area3 = result.get('results')[0].get('region').get('area3').get('name')
        area4 = result.get('results')[0].get('region').get('area4').get('name')
        num1 = result.get('results')[0].get('land').get('number1')
        num2 = result.get('results')[0].get('land').get('number2')

        if area4 == '':
            if num2 == '':
                addr2.append({'addr2': area1 +
                              ' '+area2+' '+area3+' '+num1})
            else:
                addr2.append({'addr2': area1 +
                              ' '+area2+' '+area3+' '+num1+'-'+num2})
        else:
            if num2 == '':
                addr2.append({'addr2': area1 +
                              ' '+area2+' '+area3+' '+area4+' '+num1})
            else:
                addr2.append({'addr2': area1 +
                              ' '+area2+' '+area3+' '+area4+' '+num1+'-'+num2})
    else:
        print(result)
        addr2.append({'addr2': ''})

df_addr2 = pd.DataFrame(addr2, columns=['addr2'])
academy = pd.concat([academyCsv, df_addr2], axis=1)
academy.to_excel('저장 위치/저장 파일명.xlsx', index=False)