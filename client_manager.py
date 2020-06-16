import client_connect
import threading
import queue
import tkinter as tk
import time
##########################
checkQcheck =False
HOST = "192.168.22.127"
PORT = 9999
connect = client_connect.client_connect(HOST, PORT, "Manager")
Voice_controls=["0","0","0"]#LED(0,1,2),AC(0,1),TV(0,1)
#########################################
class Application(tk.Frame):


    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.geometry('730x620+100+100')  # 윈도우창 크기 조절
        self.create_widgets()

    def create_widgets(self):# 여기에서 위젯 변경

        self.img_viewer_room = tk.Canvas(height=570, width=720)
        self.img_viewer_room.place( x=10, y=10)

        self.Exit = tk.Button(self.master, font=60, text='Exit', command=self.Exit)# 이건 지우지 말기
        self.Exit.place(x=280, y=580)
        #self.up_web = tk.Button(self, width=10, font=60, text='web upload')
        #self.up_web.pack()

    def Room_change(self):
        global Voice_controls
        global room_img_dir
        print(Voice_controls)
        room_img_dir = "refs/room/IOT" + Voice_controls[0] + Voice_controls[1] + Voice_controls[2] + ".png"
        self.img_room = tk.PhotoImage(file=room_img_dir)
        self.img_viewer_room["image"] = self.img_room


    def Exit(self):# 이건 지우지 말기
        global checkQcheck
        global connect
        connect.sendMessage("Disconnect")
        checkQcheck = False

        self.master.destroy()
####################################################
#여기에서 function 추가 수정
def LED_on():#
    num = int(Voice_controls[0])
    num+=1
    if(num>2):
        num=2
    Voice_controls[0] = str(num)
def LED_off():
    num = int(Voice_controls[0])
    num -= 1
    if (num < 0):
        num = 0
    Voice_controls[0] = str(num)
def AC_on():
    num = int(Voice_controls[1])
    num += 1
    if (num > 1):
        num = 2
    Voice_controls[0] = str(num)
def AC_off():
    num = int(Voice_controls[1])
    num -= 1
    if (num < 0):
        num = 0
def TV_on():
    num = int(Voice_controls[2])
    num += 1
    if (num > 1):
        num = 2
    Voice_controls[0] = str(num)

def TV_off():
    num = int(Voice_controls[2])
    num -= 1
    if (num < 0):
        num = 0
    Voice_controls[0] = str(num)
def checkQueue(checkQcheck,commandQ):
    global  connect
    while checkQcheck:
        if(commandQ.qsize()>0):
            message = commandQ.get(0)
            if message == "LED on": # 해당 커맨드에 따라서
                LED_on()
            elif message == "LED off":
                LED_off()
            elif message == "AC on":
                AC_on()
            elif message == "AC off":
                AC_off()
            elif message == "TV on":
                TV_on()
            elif message == "TV off":
                TV_off()
    connect.closeSoc()
#################################################################
def getCommand():
    global checkQcheck
    global  connect

    checkQcheck = True

    t1 = threading.Thread(target=checkQueue, args=(lambda:checkQcheck,connect.getCommandQueue()))
    t1.start()

def main():
    root = tk.Tk()
    A = Application(root)
    getCommand()
    root.mainloop()

main()
