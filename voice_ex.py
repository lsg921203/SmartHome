import time, serial
import RPi.GPIO as GPIO

port="/dev/ttyAMA0"
rate=9600
ser=serial.Serial(port,rate)
ser.parity=serial.PARITY_NONE
ser.bytesize=serial.EIGHTBITS

GPIO.setmode(GPIO.BOARD)

try:
    if ser.isOpen():
        ser.close()
    ser.open()
    print("serial open")
    ser.flushInput()
    ser.flushOutput()
    time.sleep(0.1)
    ser.write(serial.to_bytes([0xAA]))
    ser.write(serial.to_bytes([0x22]))
    time.sleep(0.1)
    res = ser.readline()
    time.sleep(0.1)
    print(res)
    print('testing start')

        
    while True:
        time.sleep(0.3)
        res = ser.readline()
        print(res)
        if res==b'Result:11\r\n':
                print("1")
        elif res==b'Result:12\r\n':
                print("2")
        elif res==b'Result:13\r\n':
                print("3")
        elif res==b'Result:14\r\n':
                print("4")
        elif res==b'Result:15\r\n':
                print("5")
    print('input end')
except:
    pass
finally:
    ser.close()

