import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

SW=7
pins=[11,13,15]

password = 1234
passcnt = 0
for i in pins:
    GPIO.setup(i,GPIO.OUT, initial=GPIO.LOW)

GPIO.setup(SW, GPIO.IN)

try:
    while 1:
        inputpass = int(input("password : "))
        if password == inputpass:
            for i in range(0,5):
                GPIO.output(pins[1], GPIO.HIGH)
                time.sleep(0.2)
                GPIO.output(pins[1], GPIO.LOW)
                time.sleep(0.2)
        elif passcnt > 4:
            for i in range(0,5):
                GPIO.output(pins[0], GPIO.HIGH)
                time.sleep(0.2)
                GPIO.output(pins[0], GPIO.LOW)
                time.sleep(0.2)
        else:
            passcnt+=1
            print('try again passcnt : ',passcnt)
except  KeyboardInterrupt:
    pass

GPIO.cleanup()
