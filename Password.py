import RPi.GPIO as GPIO
import time, os, threading
import tkinter as tk
from tkinter import *
from tkinter import ttk

GPIO.setmode(GPIO.BOARD)

SW = 7
pins = [11, 13, 15]
pin = 37
data = [260, 290, 330, 340, 380, 430, 490, 510]

password = "1234"  # 비밀번호 설정
passcnt = 0

for i in pins:
    GPIO.setup(i, GPIO.OUT, initial=GPIO.LOW)  # led

GPIO.setup(pin, GPIO.OUT)  # speaker
buz = GPIO.PWM(pin, 100)

GPIO.setup(SW, GPIO.IN)  # switch


def openSPK():
    buz.start(100)
    buz.ChangeDutyCycle(90)
    buz.ChangeFrequency(data[0])
    time.sleep(0.3)
    buz.ChangeFrequency(1)
    time.sleep(0.03)
    buz.ChangeDutyCycle(90)
    buz.ChangeFrequency(data[2])
    time.sleep(0.3)
    buz.ChangeFrequency(1)
    time.sleep(0.03)
    buz.ChangeDutyCycle(90)
    buz.ChangeFrequency(data[4])
    time.sleep(0.3)
    buz.ChangeFrequency(1)
    time.sleep(0.03)
    buz.ChangeDutyCycle(90)
    buz.ChangeFrequency(data[7])
    time.sleep(0.3)
    buz.ChangeFrequency(1)
    time.sleep(0.03)
    buz.stop()


def warSPK():
    buz.start(100)
    for i in range(0, 3):
        buz.ChangeDutyCycle(90)
        buz.ChangeFrequency(data[0])
        time.sleep(0.3)
        buz.ChangeFrequency(1)
        time.sleep(0.03)
        buz.ChangeDutyCycle(90)
        buz.ChangeFrequency(data[6])
        time.sleep(0.3)
        buz.ChangeFrequency(1)
        time.sleep(0.03)
    buz.stop()


def openLed():
    GPIO.output(pins[1], GPIO.HIGH)
    time.sleep(1.5)
    GPIO.output(pins[1], GPIO.LOW)


def warLed():
    for i in range(0, 5):
        GPIO.output(pins[0], GPIO.HIGH)
        time.sleep(0.2)
        GPIO.output(pins[0], GPIO.LOW)
        time.sleep(0.2)


def openTh():
    threading.Thread(target=openLed).start()
    threading.Thread(target=openSPK).start()


def warTh():
    threading.Thread(target=warLed).start()
    threading.Thread(target=warSPK).start()


def clear():  # 틀린횟수 초기화
    global passcnt
    passcnt = 0
    num_entry.delete(0)


def enter(value):  # 비밀번호 맞는지 틀리는지 확인
    global passcnt
    num_entry.delete(0, 'end')
    inputpass = value
    print(inputpass)
    print(type(inputpass))
    passcnt += 1
    if password == inputpass:
        print('door open')
        passcnt = 0
        openTh()

    elif passcnt > 3:
        print('warning')
        warTh()

    else:
        print('비밀번호 틀림!!!\ntry again passcnt : ', passcnt)


def button_pressed(value):  # 숫자버튼 커멘드
    if len(num_entry.get()) > 3:
        enter(num_entry.get())
        num_entry.delete(0, 'end')
    print(value, "pressed")
    num_entry.insert("end", value)


root = Tk()
root.title("Pass")
root.geometry("500x200")  # 버튼폭에 맞춰서 확장.

entry_value = StringVar(root, value='')

num_entry = ttk.Entry(root, textvariable=entry_value, width=20)
num_entry.grid(row=0, columnspan=3)  # columnspan 은 여러칸에 걸쳐서 표시함.

# button 9개 추가
button7 = ttk.Button(root, text="7", command=lambda: button_pressed('7'))
button7.grid(row=1, column=0)
button8 = ttk.Button(root, text="8", command=lambda: button_pressed('8'))
button8.grid(row=1, column=1)
button9 = ttk.Button(root, text="9", command=lambda: button_pressed('9'))
button9.grid(row=1, column=2)

button4 = ttk.Button(root, text="4", command=lambda: button_pressed('4'))
button4.grid(row=2, column=0)
button5 = ttk.Button(root, text="5", command=lambda: button_pressed('5'))
button5.grid(row=2, column=1)
button6 = ttk.Button(root, text="6", command=lambda: button_pressed('6'))
button6.grid(row=2, column=2)

button1 = ttk.Button(root, text="1", command=lambda: button_pressed('1'))
button1.grid(row=3, column=0)
button2 = ttk.Button(root, text="2", command=lambda: button_pressed('2'))
button2.grid(row=3, column=1)
button3 = ttk.Button(root, text="3", command=lambda: button_pressed('3'))
button3.grid(row=3, column=2)

button0 = ttk.Button(root, text="0", command=lambda: button_pressed('0'))
button0.grid(row=4, column=1)

btnetr = ttk.Button(root, text="↑", command=lambda: enter(num_entry.get()))
btnetr.grid(row=4, column=2)

btnclr = ttk.Button(root, text="c", command=lambda: clear())
btnclr.grid(row=4, column=0)

label = tk.Label(root, text='', relief='groove', borderwidth=1, padx=400, pady=150)

root.mainloop()

main()
GPIO.cleanup()
