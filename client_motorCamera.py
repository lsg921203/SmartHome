import client_connect
import threading
import queue
import tkinter as tk
import time
import RPi.GPIO as GPIO
import re
import serial
import picamera
import video_connect

##########################
checkQcheck =False
HOST = "192.168.22.127"
PORT = 9999
VIDEOPORT2 = 8888
connect = client_connect.client_connect(HOST, PORT, "MortorCamera")

ser = serial.Serial('/dev/ttyACM0', 9600, timeout = None)#시리얼 포트 설정
GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT) #서보모터

camera_on_check =False
#########################################
class Application(tk.Frame):


    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.geometry('600x600+100+100')  # 윈도우창 크기 조절
        self.create_widgets()
        self.p = GPIO.PWM(12, 50)
        self.p.start(0)
        self.servo = 7
        self.beforeAngle = 7




    def create_widgets(self):# 여기에서 위젯 변경

        self.command1 = tk.Button(self.master, font=60, text='command1', command=self.Button_command1)
        self.command1.place( x=245 , y=610)

        self.Exit = tk.Button(self.master, font=60, text='Exit', command=self.Exit)# 이건 지우지 말기
        self.Exit.place(x=280, y=555)
        #self.up_web = tk.Button(self, width=10, font=60, text='web upload')
        #self.up_web.pack()

    def Button_command1(self):
        global connect
        connect.sendMessage("yo")

    def control_servo(self,num):
        self.beforeAngle = 7

        print(num)
        if int(num) == 1:
            self.servo -= 1
        elif int(num) == 2:
            self.servo += 1

        if self.servo <= 2:
            self.servo = 3
        elif self.servo >= 12:
            self.servo = 11

        if 2 < self.servo and self.servo < 12:
            if (self.servo != self.beforeAngle):
                self.p.ChangeDutyCycle(self.servo)
                self.beforeAngle = self.servo



    def Exit(self):# 이건 지우지 말기
        global checkQcheck
        global connect
        connect.sendMessage("Disconnect")
        checkQcheck = False
        self.p.stop()
        self.master.destroy()
####################################################
#여기에서 function 추가 수정
def func1():#
    print("hello")

def func2():
    print("I'm fine and you")

def camera_on(ld_coc):
    v_connect = video_connect.video_connect(HOST, VIDEOPORT2, 1)
    c = picamera.PiCamera()
    c.resolution = (320, 240)
    path = "refs/tmp.png"
    print(ld_coc())
    while(ld_coc()):
        c.capture(path)
        v_connect.sendImage(path)
        time.sleep(0.3)
    v_connect.closeSoc()
    c.close()

def checkQueue(checkQcheck,commandQ):
    global connect
    global camera_on_check
    global A
    while checkQcheck:
        if(commandQ.qsize()>0):
            message = commandQ.get(0)
            if message == "hi": # 해당 커맨드에 따라서
                func1()         # 특정 함수 호출
            elif message == "how are you":
                func2()
            elif message == "start camera":
                camera_on_check =True
                th = threading.Thread(target=camera_on,args=(lambda :camera_on_check,))
                th.start()
            elif message == "end camera":
                camera_on_check = False
            elif message == "1" or "2":
                A.control_servo(message)
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

root = tk.Tk()
A = Application(root)
main(root)
