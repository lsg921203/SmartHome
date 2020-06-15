import RPi.GPIO as GPIO  
from time import sleep
import re
import serial

ser = serial.Serial('/dev/ttyACM0', 9600, timeout = None)#시리얼 포트 설정

GPIO.setmode(GPIO.BOARD) 

GPIO.setup(12, GPIO.OUT) #서보모터 

p = GPIO.PWM(12, 50) 

p.start(0)            
servo = 7#서보모터 초기값 

while 1:
    joy=str(ser.readline())#아두이노에서 들어온 시리얼값 저장 
    num = re.findall("\d+", joy)#시리얼값에서 필요한 부분만 저장 
    print(num)
    if int(num[0])==1 and 2<servo :
        servo -= 1
    elif int(num[0])==2 and servo<12:
        servo += 1
    if 2<servo and servo<12:
        p.ChangeDutyCycle(servo)
    del(num)#원래 들어있던 조이스틱 값 삭제 

p.stop()                

GPIO.cleanup() 