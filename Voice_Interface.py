import client_connect
import threading
import queue
import tkinter as tk
import time
import voice_machine
import serial
import re

##########################
checkQcheck = False
# HOST = "192.168.22.127"#LSG(SungGyeol)

ser = serial.Serial('/dev/ttyACM0', 9600, timeout = None)#시리얼 포트 설정

HOST = "192.168.22.127"  # NYK
PORT = 9999
connect = client_connect.client_connect(HOST, PORT, "Voice")
targetParts = [["Door", "open"], ["LED", "on"], ["Window", "open"], ["AC", "on"], ["TV", "on"], ["None", "None"]]


#########################################
class Application(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.geometry('600x600+100+100')  # 윈도우창 크기 조절
        self.create_widgets()
        self.state = "0"
        self.input_joystick_check = True
        th = threading.Thread(target= self.input_joystick)
        th.start()

    def create_widgets(self):  # 여기에서 위젯 변경

        self.command1 = tk.Button(self.master, font=60, text='voice command', command=self.Button_command1)
        self.command1.place(x=245, y=610)

        self.Exit = tk.Button(self.master, font=60, text='Exit', command=self.Exit)  # 이건 지우지 말기
        self.Exit.place(x=280, y=555)
        # self.up_web = tk.Button(self, width=10, font=60, text='web upload')
        # self.up_web.pack()
    def input_joystick(self):
        while self.input_joystick_check:

            joy=str(ser.readline())#아두이노에서 들어온 시리얼값 저장
            num = re.findall("\d+", joy)#시리얼값에서 필요한 부분만 저장
            if(num[0] != "0"):
                connect.sendMessage(num[0])
            del(num)
    def Button_command1(self):
        global connect
        global targetParts
        vcm = voice_machine.voice_machine(targetParts)
        aa = vcm.mode("hear2Act")
        print(aa)
        Msg = aa[0] + " " + aa[1]
        print(Msg)
        connect.sendMessage(Msg)

    def Exit(self):  # 이건 지우지 말기
        global checkQcheck
        global connect
        connect.sendMessage("Disconnect")
        checkQcheck = False
        input_joystick_check = False
        self.master.destroy()


####################################################
# 여기에서 function 추가 수정
def func1():  #
    print("hello")


def func2():
    print("I'm fine and you")


def checkQueue(checkQcheck, commandQ):
    global connect
    while checkQcheck:
        if (commandQ.qsize() > 0):
            message = commandQ.get(0)
            if message == "hi":  # 해당 커맨드에 따라서
                func1()  # 특정 함수 호출
            elif message == "how are you":
                func2()
    connect.closeSoc()


#################################################################
def getCommand():
    global checkQcheck
    global connect

    checkQcheck = True

    t1 = threading.Thread(target=checkQueue, args=(lambda: checkQcheck, connect.getCommandQueue()))
    t1.start()


def main():
    root = tk.Tk()
    A = Application(root)
    getCommand()
    root.mainloop()


main()
