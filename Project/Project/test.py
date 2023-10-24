#import RPi.GPIO as GPIO
from time import sleep
import time
import threading
import sys
import os

# def open_bar():
#     GPIO.setmode(GPIO.BCM)
#     GPIO.setwarnings(False)
#     motor_pin = 26
#     GPIO.setup(motor_pin,GPIO.OUT)
#     p = GPIO.PWM(motor_pin,50)
#     p.start(0)
#     p.ChangeDutyCycle(7.5)
#     time.sleep(2)
#     p.ChangeDutyCycle(12.5)
#     time.sleep(1)
#     p.stop()
#     GPIO.Cleanup()

#led제어 , 문자열로 들어와서 제어코드 추가, mtemp : 체감온도 "주의, 경고" 데이터 / msun : 자외선 차단 지수 "높음, 매우높음" 데이터
def led_on(mtemp, msun):
    print("LED제어하는 함수입니다. %s는 mtemp,%s는 msun" %(mtemp,msun))

    