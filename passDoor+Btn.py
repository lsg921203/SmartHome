import RPi.GPIO as GPIO
import time, os, threading
import tkinter as tk
from tkinter import *
from tkinter import ttk

GPIO.setmode(GPIO.BOARD)

SW = 7  # 버튼
pins = [11, 13, 15]  # led
pin = 37  # 스피커
data = [260, 290, 330, 340, 380, 430, 490, 510]

password = "1234"  # 비밀번호 설정
passcnt = 0  # 비밀번호 틀린 횟수

for i in pins:
    GPIO.setup(i, GPIO.OUT, initial=GPIO.LOW)  # led

GPIO.setup(pin, GPIO.OUT)  # speaker
buz = GPIO.PWM(pin, 100)

GPIO.setup(SW, GPIO.IN)  # switch


def doorOpen():  # 도어 열림 애니메이션
    root.update()  # canvas 활성화
    time.sleep(0.5)
    for x in range(0, 30):
        canvas.move(1, 5, 0)  # x축으로 5만큼 이동

        root.update()  # x축 이동한 이미지 활성화

        time.sleep(0.05)

    time.sleep(4)

    for x in range(0, 30):
        canvas.move(1, -5, 0)

        root.update()

        time.sleep(0.05)


def bellSPK():  # 초인종 소리, 초인종 눌렀을때 실행함수
    buz.start(100)
    buz.ChangeDutyCycle(90)
    buz.ChangeFrequency(data[3])
    time.sleep(1)
    buz.ChangeFrequency(1)
    time.sleep(0.03)
    buz.ChangeDutyCycle(90)
    buz.ChangeFrequency(data[3])
    time.sleep(1)
    buz.ChangeFrequency(1)
    time.sleep(0.03)
    buz.stop()


def BellBtn():  # 버튼 입력 대기상태 만들기
    while 1:
        GPIO.wait_for_edge(SW, GPIO.RISING, 300)
        print('pushed')
        bellSPK()
        print('ready')


def openSPK():  # 도어오픈 스피커
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


def warSPK():  # 경고음
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


def openLed():  # 도어오픈 led
    GPIO.output(pins[1], GPIO.HIGH)
    time.sleep(3)
    GPIO.output(pins[1], GPIO.LOW)


def warLed():  # 경고 led
    for i in range(0, 5):
        GPIO.output(pins[0], GPIO.HIGH)
        time.sleep(0.2)
        GPIO.output(pins[0], GPIO.LOW)
        time.sleep(0.2)


def openTh():  # 오픈동작
    threading.Thread(target=openLed).start()
    threading.Thread(target=openSPK).start()
    threading.Thread(target=doorOpen).start()


def warTh():  # 비밀번호4번틀릴때동작
    threading.Thread(target=warLed).start()
    threading.Thread(target=warSPK).start()


def clear():  # 틀린횟수 초기화
    global passcnt
    passcnt = 0
    num_entry.delete(0)


def enter(value):  # 키패드에 입력된 값 수신
    global passcnt
    num_entry.delete(0, 'end')  # 키패드 entry 초기화
    inputpass = value
    print(inputpass)
    print(type(inputpass))
    passcnt += 1

    if password == inputpass:  # 비밀번호 맞는지 틀리는지 확인
        print('door open')
        passcnt = 0
        openTh()
    elif passcnt > 3:  # 일정횟수 이상 틀리면 경고동작 실행
        print('warning')
        warTh()
    else:
        label.config(text="비밀번호 틀림!!!")  # 비밀번호 틀렸을때
        print('비밀번호 틀림!!!\ntry again passcnt : ', passcnt)


def button_pressed(value):  # 숫자버튼 커멘드
    label.config(text="")  # 비밀번호가 틀렸습니다 라벨 초기화
    if len(num_entry.get()) > 3:  # 키패드 entry에 4개초과로 입력됐을때 자동전송하고 entry초기화
        enter(num_entry.get())
        num_entry.delete(0, 'end')
    print(value, "pressed")
    num_entry.insert("end", value)  # 들어온 value값을 entry에 추가


root = Tk()
root.title("Pass")
root.geometry("1500x1500")  # 버튼폭에 맞춰서 확장.
root.resizable(True, True)

entry_value = StringVar(root, value='')  # entry값 저장할 변수

num_entry = ttk.Entry(root, textvariable=entry_value, width=20)
num_entry.place(x=10, y=0)
# button 9개 추가
button7 = ttk.Button(root, text="7", command=lambda: button_pressed('7'))
button7.place(x=0, y=30, width=60)
button8 = ttk.Button(root, text="8", command=lambda: button_pressed('8'))
button8.place(x=60, y=30, width=60)
button9 = ttk.Button(root, text="9", command=lambda: button_pressed('9'))
button9.place(x=120, y=30, width=60)

button4 = ttk.Button(root, text="4", command=lambda: button_pressed('4'))
button4.place(x=0, y=60, width=60)
button5 = ttk.Button(root, text="5", command=lambda: button_pressed('5'))
button5.place(x=60, y=60, width=60)
button6 = ttk.Button(root, text="6", command=lambda: button_pressed('6'))
button6.place(x=120, y=60, width=60)

button1 = ttk.Button(root, text="1", command=lambda: button_pressed('1'))
button1.place(x=0, y=90, width=60)
button2 = ttk.Button(root, text="2", command=lambda: button_pressed('2'))
button2.place(x=60, y=90, width=60)
button3 = ttk.Button(root, text="3", command=lambda: button_pressed('3'))
button3.place(x=120, y=90, width=60)

button0 = ttk.Button(root, text="0", command=lambda: button_pressed('0'))
button0.place(x=60, y=120, width=60)

btnetr = ttk.Button(root, text="↑", command=lambda: enter(num_entry.get()))
btnetr.place(x=120, y=120, width=60)

btnclr = ttk.Button(root, text="c", command=lambda: clear())
btnclr.place(x=0, y=120, width=60)

label = tk.Label(root, text="")
label.place(x=10, y=150)

canvas = Canvas(root, width=1500, height=1500)
canvas.place(x=200, y=0)

testImage1 = PhotoImage(file="door.png")
testImage2 = PhotoImage(file="door2.png")
canvas.create_image(420, 100, anchor=NW, image=testImage2)
canvas.create_image(150, 100, anchor=NW, image=testImage1)

threading.Thread(target=BellBtn).start()  # gui랑 버튼 입력동시동작 &mainloop앞에 있어야함&
root.mainloop()

main()
GPIO.cleanup()





