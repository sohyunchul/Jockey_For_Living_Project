from flask import Flask, render_template, request # flask모듈에서 Flask클래스 import
import requests  # pip install requests
from urllib.parse import urlencode, unquote # 딕셔너리를 URL파라미터 형식으로 변환(웹 요청 시 데이터를 URL에 함께 전달해야 할 때 유용)
import json # 서버와 클라이언트 간 데이터를 교환하거나 저장할 때 사용
import csv # CSV 형식의 파일 읽기 및 사용
from dotenv import load_dotenv #"env'파일에 정의된 환경 변수들을 현재 스크립트의 환경 변수로 로드
import os # 운영 체제와 상호 작용하고 다양한 운영 체제 관련 작업을 수행하는 방법을 제공
from datetime import datetime # 현재 날짜와 시간을 반환
import test as ts 

load_dotenv()
WeatherDailyLife = os.environ.get("WEATHER_FORECAST_KEY") # 공공데이터포털에서 받은 인증키
app = Flask(__name__) 

# 현재시간 표기(년, 월, 일, 시) ex)2023090112 (API에서 date값 양식)
def current_TimeNow():
    current_time = datetime.now() 
    formatted_time = current_time.strftime("%Y%m%d%H")
    return formatted_time

# 현재시간 ~ 00시까지 계산 ex) 12시~00시까지 개수 12개
def disPlayTimeCount(datet):
    splitdatet = datet[-2::] # ex)2023090109에서 9,10번째 값
    timeCount = 24 - int(splitdatet) + 1 # 24는 00시 기준, 날짜데이터에서 시간만 가져옴, 현재시간 포함 +1
    return timeCount

#체감온도
# 발표 시간 기준으로 00시까지 1시간 단위로 온도 출력
# ex) 현재시간 09시 10시 ~ 00시까지 1시간 단위 온도출력
def getWindChill(city_id):

#현재시간 출력
    
    print("1. url함수 : " + str(current_TimeNow()))
    url = "http://apis.data.go.kr/1360000/LivingWthrIdxServiceV4/getSenTaIdxV4"
    queryString = "?" + urlencode(
        {
            "serviceKey": unquote(WeatherDailyLife),
            "numOfRows": "10",
            "pageNo": "1",
            "dataType": "JSON",
            "areaNo" : city_id, # 지역번호
            "time" : current_TimeNow(), # 현재시간
            "requestCode" : "A41", # 요청코드(서비스대상) A41, 노인 A42, 어린이 A44, 농촌 A45, 비닐하우스 A46, 취약거주환경 A47, 도로 A48, 건설현장 A49, 조선소
        }
    )
    response = requests.get(url + queryString)
    print("2." + response.text)  
    r_dict = json.loads(response.text)
    r_response = r_dict.get("response")
    r_body = r_response.get("body")
    r_item = r_body.get("items")
    item_list = r_item.get("item")
    
    templist = {} # 체감온도 딕셔너리
    # 아이템리스트안에 있는 아이템으로 for문으로 실행
    for item in item_list:
        datet = item.get("date") # API에서 제공해주는 DATE값
        print("3." + datet)
        
        timecount = disPlayTimeCount(datet) # 현재시간 ~ 24시까지 개수
        print(timecount)
        
        splitdatet = datet[-2::] # API에서 제공해주는 DATE값에서 뒤에 2개(시간)
        for i in range(1, timecount + 1): # 시간에 해당하는 데이터
            itemname = "h" + str(i) # 미리보기 h + 숫자(문자열)
            templist[str(int(splitdatet) + i - 1)] = item.get(itemname) # key : value, 발표시간 : 온도 (발표시간 ~ 24시까지, 1부터 시작해서 -1)
        print(templist)
        break
    return templist

# 자외선 차단지수
def UvIndex(city_id):
    current_TimeNow()
    url = "http://apis.data.go.kr/1360000/LivingWthrIdxServiceV4/getUVIdxV4"
    queryString = "?" + urlencode(
        {
            "serviceKey": unquote(WeatherDailyLife),
            "numOfRows": "10",
            "pageNo": "1",
            "dataType": "JSON",
            "areaNo" : city_id, # 지역번호
            "time" : current_TimeNow(), # 현재시간
        }
    )
    response = requests.get(url + queryString)
    print("6." + response.text) 
    r_dict = json.loads(response.text)
    r_response = r_dict.get("response")
    r_body = r_response.get("body")
    r_item = r_body.get("items")
    item_list = r_item.get("item")

    uvCount = 8 - (int(current_TimeNow()[-2::])//3)
    #현재시간~ 초기값(발표초기값)
    stime = (int(current_TimeNow()[-2::])//3) *3 
    suntemplist = {} # 자외선 차단 지수 딕셔너리

    # 아이템리스트안에 있는 아이템으로 for문으로 실행
    for item in item_list:
        datet = item.get("date") # API에서 제공해주는 DATE값, 발표시간 기준
        print("7." + datet)
        timecount = disPlayTimeCount(datet) # 현재시간 ~ 24시까지 개수
        print(timecount)
        splitdatet = datet[-2::] # API에서 제공해주는 DATE값에서 뒤에 2개(시간)
        for i in range(1, uvCount + 1): # 시간에 해당하는 데이터
            print(str(stime) + "~" + str(stime+3))
            stime = stime+3
            itemname = "h" + str((i - 1) * 3) # 미리보기 h + 숫자(문자열), 3시간마다 정보받아오기 때문
            suntemplist[str(int(splitdatet) + (i - 1)*3)] = item.get(itemname) # key : value, 발표시간 : 온도 (발표시간 ~ 24시까지, 1부터 시작해서 -1)            
        break    
    return suntemplist

# 딕셔너리 생성
city_dict = {}
with open(
    "city.csv", # csv파일안에 있는 시티명에서 출력
    mode="r", 
    encoding="UTF8",
) as inp:    
    
    reader = csv.reader(inp)
    city_dict = {rows[0]: rows[1] for rows in reader} # 반복문을 통해 csv파일안에 있는 시티명에서 지역정보를 출력한다.
print(city_dict)

@app.route("/", methods=["GET", "POST"]) # GET모드와 POST모드 지원
def index():
    if request.method == "POST": # POST모드일 경우 진행
        city_name = request.form["name"] # 지역명
        print(city_name)
        city_id = city_dict.get(city_name) # 지역번호
        print(city_id)
        # 현재 시간 계산
        current_time = datetime.now()
        current_hour = current_time.hour # 0 ~ 23시

        # 시간별 자외선 차단 지수 데이터 생성
        time_count = disPlayTimeCount(current_TimeNow())
        
        if city_id == None: 
            return render_template("index.html") # 지역명이 없을 경우
        # post모드일 경우 78번째 코드에 이어서 진행
        templist = getWindChill(city_id) # 체감온도 출력
        suntemplist = UvIndex(city_id) # 자외선 차단지수       
        
        mtemp = max(list(templist.values()))
        msun = max(list(suntemplist.values()))

        # 체감온도별 "주의, 경고" 표시
        if int(mtemp) >=29:
            mtemp = "경고"
        elif int(mtemp) >= 28:
            mtemp = "주의" 
        else:
            mtemp = "날씨 좋음"

        # 자외선 차단 지수 "주의, 경고" 표시
        if int(msun) >= 8:
            msun = "매우높음" 
        elif int(msun) >= 6 and int(msun) < 8:
            msun = "높음"
        else:
            msun = "보통"
        data = {"tempstr" : mtemp,"sunstr":msun} # 체감온도, 자외선 차단지수
        ts.led_on(mtemp,msun)
        
        return render_template(
            "index.html",
            temp = templist,  #체감온도
            suntemplist = suntemplist, # 자외선 차단 지수
            city_name = city_name, #도시이름
            current_time = current_TimeNow()[-2::], # HTML 검색시간 전달 
            #data = data, # 체감온도, 자외선차단지수 
            tempstr = mtemp,
            sunstr = msun,
            data = data
        )
    else: # GET모드일 경우 html반환
        return render_template("main.html")
    
if __name__ == "__main__":
    app.run(debug=True)