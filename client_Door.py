import client_connect
import queue
import RPi.GPIO as GPIO
import time, os, threading
import tkinter as tk
from tkinter import *
from tkinter import ttk
import picamera
import video_connect
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

camera_on_check =False

##########################
checkQcheck =False
HOST = "192.168.22.127"
PORT = 9999
VIDEOPORT1 = 8888
connect = client_connect.client_connect(HOST, PORT, "Door")



####


#########################################
class Application(tk.Frame):


    def __init__(self, root=None):
        super().__init__(root)
        self.root = root
        self.root.title("Pass")
        self.root.geometry("1500x1500")  # 윈도우창 크기 조절
        self.root.resizable(True, True)
        self.entry_value = StringVar(root, value='')
        self.create_widgets()
        self.state = "0"
        self.bell_Botton_Check = True
        th = threading.Thread(target=self.BellBtn)
        th.start()
    def create_widgets(self):# 여기에서 위젯 변경
        self.num_entry = ttk.Entry(self.root, textvariable=self.entry_value, width=20)
        self.num_entry.place(x=10, y=0)
        # button 9개 추가
        self.button7 = ttk.Button(self.root, text="7", command=lambda: self.button_pressed('7'))
        self.button7.place(x=0, y=30, width=60)
        self.button8 = ttk.Button(self.root, text="8", command=lambda: self.button_pressed('8'))
        self.button8.place(x=60, y=30, width=60)
        self.button9 = ttk.Button(self.root, text="9", command=lambda: self.button_pressed('9'))
        self.button9.place(x=120, y=30, width=60)

        self.button4 = ttk.Button(self.root, text="4", command=lambda: self.button_pressed('4'))
        self.button4.place(x=0, y=60, width=60)
        self.button5 = ttk.Button(self.root, text="5", command=lambda: self.button_pressed('5'))
        self.button5.place(x=60, y=60, width=60)
        self.button6 = ttk.Button(self.root, text="6", command=lambda: self.button_pressed('6'))
        self.button6.place(x=120, y=60, width=60)

        self.button1 = ttk.Button(self.root, text="1", command=lambda: self.button_pressed('1'))
        self.button1.place(x=0, y=90, width=60)
        self.button2 = ttk.Button(self.root, text="2", command=lambda: self.button_pressed('2'))
        self.button2.place(x=60, y=90, width=60)
        self.button3 = ttk.Button(self.root, text="3", command=lambda: self.button_pressed('3'))
        self.button3.place(x=120, y=90, width=60)

        self.button0 = ttk.Button(self.root, text="0", command=lambda: self.button_pressed('0'))
        self.button0.place(x=60, y=120, width=60)

        self.btnetr = ttk.Button(self.root, text="↑", command=lambda: self.enter(self.num_entry.get()))#
        self.btnetr.place(x=120, y=120, width=60)

        self.btnclr = ttk.Button(self.root, text="c", command=lambda: self.clear())#
        self.btnclr.place(x=0, y=120, width=60)

        self.label = tk.Label(self.root, text="")
        self.label.place(x=10, y=150)

        self.canvas = Canvas(self.root, width=1500, height=1500)
        self.canvas.place(x=200, y=0)

        self.testImage1 = PhotoImage(file="door.png")
        self.testImage2 = PhotoImage(file="door2.png")
        self.canvas.create_image(420, 100, anchor=NW, image=self.testImage2)
        self.canvas.create_image(150, 100, anchor=NW, image=self.testImage1)

        self.Exit = tk.Button(self.root, font=60, text='Exit', command=self.Exit)# 이건 지우지 말기
        self.Exit.place(x=280, y=555)
        #self.up_web = tk.Button(self, width=10, font=60, text='web upload')
        #self.up_web.pack()

    def Button_command1(self):
        global connect
        connect.sendMessage("yo")

    def clear(self):  # 틀린횟수 초기화
        global passcnt
        passcnt = 0
        self.num_entry.delete(0)

    def enter(self,value):  # 키패드에 입력된 값 수신 ########################################
        global passcnt
        global password
        self.num_entry.delete(0, 'end')  # 키패드 entry 초기화
        inputpass = value
        print(inputpass)
        print(type(inputpass))
        passcnt += 1

        if password == inputpass:  # 비밀번호 맞는지 틀리는지 확인
            print('door open')
            passcnt = 0
            self.openTh()
        elif passcnt > 3:  # 일정횟수 이상 틀리면 경고동작 실행
            print('warning')
            self.warTh()
        else:
            self.label.config(text="비밀번호 틀림!!!")  # 비밀번호 틀렸을때
            print('비밀번호 틀림!!!\ntry again passcnt : ', passcnt)
    def doorOpen(self):  # 도어 열림 애니메이션
        self.root.update()  # canvas 활성화
        time.sleep(0.5)
        for x in range(0, 30):
            self.canvas.move(1, 5, 0)  # x축으로 5만큼 이동

            self.root.update()  # x축 이동한 이미지 활성화

            time.sleep(0.05)

        time.sleep(4)

        for x in range(0, 30):
            self.canvas.move(1, -5, 0)

            self.root.update()

            time.sleep(0.05)


    def bellSPK(self):  # 초인종 소리, 초인종 눌렀을때 실행함수
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


    def BellBtn(self):  # 버튼 입력 대기상태 만들기
        global connect
        while self.bell_Botton_Check:
            GPIO.wait_for_edge(SW,GPIO.RISING,300)
            connect.sendMessage("bell")
            print('bell')
            self.bellSPK()
            time.sleep(0.3)
        


    def openSPK(self):  # 도어오픈 스피커
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


    def warSPK(self):  # 경고음
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
        self.state("1")


    def openLed(self):  # 도어오픈 led
        GPIO.output(pins[1], GPIO.HIGH)
        time.sleep(3)
        GPIO.output(pins[1], GPIO.LOW)


    def warLed(self):  # 경고 led
        for i in range(0, 5):
            GPIO.output(pins[0], GPIO.HIGH)
            time.sleep(0.2)
            GPIO.output(pins[0], GPIO.LOW)
            time.sleep(0.2)


    def openTh(self):  # 오픈동작
        threading.Thread(target=self.openLed).start()
        threading.Thread(target=self.openSPK).start()
        threading.Thread(target=self.doorOpen).start()


    def warTh(self):  # 비밀번호4번틀릴때동작
        threading.Thread(target=self.warLed).start()
        threading.Thread(target=self.warSPK).start()



    def button_pressed(self,value):  # 숫자버튼 커멘드 #################################################
        self.label.config(text="")  # 비밀번호가 틀렸습니다 라벨 초기화
        if len(self.num_entry.get()) > 3:  # 키패드 entry에 4개초과로 입력됐을때 자동전송하고 entry초기화
            self.enter(self.num_entry.get())
            self.num_entry.delete(0, 'end')
        print(value, "pressed")
        self.num_entry.insert("end", value)  # 들어온 value값을 entry에 추가

    def Exit(self):# 이건 지우지 말기
        global checkQcheck
        global connect
        connect.sendMessage("Disconnect")
        checkQcheck = False
        #GPIO.remove_event_detect(SW)######
        self.bell_Botton_Check = False
        GPIO.cleanup()
        self.master.destroy()

def camera_on(ld_coc):
    v_connect = video_connect.video_connect(HOST, VIDEOPORT1, 0)
    c = picamera.PiCamera()
    c.resolution = (150, 100)
    path = "refs/tmp.png"
    print(ld_coc())
    while(ld_coc()):
        c.capture(path)
        v_connect.sendImage(path)
        time.sleep(0.3)
    v_connect.closeSoc()
    c.close()
###############################################
root = tk.Tk()
A = Application(root)
#GPIO.add_event_detect(SW,GPIO.RISING,A.BellBtn,500)########

####################################################
#여기에서 function 추가 수정


def checkQueue(checkQcheck,commandQ):
    global  connect
    global camera_on_check
    while checkQcheck:
        if(commandQ.qsize()>0):
            message = commandQ.get(0)
            if message == "door open": # 해당 커맨드에 따라서
                A.openTh()         # 특정 함수 호출
            elif message == "warning":
                A.warTh()
            elif message == "get state":
                connect.sendMessage(A.state)
            elif message == "start camera":
                camera_on_check =True
                th = threading.Thread(target=camera_on,args=(lambda :camera_on_check,))
                th.start()
            elif message == "end camera":
                camera_on_check = False
    connect.closeSoc()
#################################################################
def getCommand():
    global checkQcheck
    global  connect

    checkQcheck = True

    t1 = threading.Thread(target=checkQueue, args=(lambda:checkQcheck,connect.getCommandQueue()))
    t1.start()

def main(root):
    
    getCommand()
    root.mainloop()

main(root)

