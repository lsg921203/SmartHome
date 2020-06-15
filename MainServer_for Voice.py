import tkinter as tk
from tkinter import messagebox
import socket, os
import threading
import queue
import sys
import time

messageQueue = queue.Queue()
commandQueue = queue.Queue()
client_socket_list = []
Parts_list = ["Voice","Bell"]
#Voice controls추가함
Voice_controls=["0","0","0"]#LED012, AC01, TV01
room_img_dir=" "

wait_c_check = False
wait_m_check = False
send_c_check = False
activity_check = False

#HOST = '192.168.22.127'#'192.168.103.61'  #server ip
HOST="192.168.22.157"    #NYK
PORT = 9999         #server port

#server socket open. socket.AF_INET:주소체계(IPV4), socket.SOCK_STREAM:tcp
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

class Application(tk.Frame):
    global commandQueue
    global wait_c_check
    global wait_m_check
    global send_c_check
    global activity_check

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.geometry('600x600+100+100')  # 윈도우창 크기 1600*900, 위치:100,100
        #self.master.resizable(True, True)
        #self.pack()
        self.effect = ['negative', 'sketch', 'pastel', 'watercolor']
        self.create_widgets()

    def create_widgets(self):

        self.img = tk.PhotoImage(file="refs/mic_img.png")
        self.img_viewer = tk.Label(self.master, image=self.img)
        self.img_viewer.place(x=35,y=10)

        #room 추가됨
        self.img_room = tk.PhotoImage(file="refs/room/IOT000.png")
        self.img_viewer_room = tk.Label(self.master, image=self.img_room)
        self.img_viewer_room.place(x=60, y=10)



        #self.fname = tk.Label(self.master, text='')
        #self.fname.pack()

        self.command1 = tk.Button(self.master, font=60, text='LED on brightly', command=self.Button_command1)
        self.command1.place( x=245 , y=610)
        self.command2 = tk.Button(self.master, font=60, text='LED on not brightly', command=self.Button_command2)
        self.command2.place(x=345, y=610)
        self.command3 = tk.Button(self.master, font=60, text='LED off', command=self.Button_command3)
        self.command3.place(x=445, y=610)
        self.command4 = tk.Button(self.master, font=60, text='AC on', command=self.Button_command4)
        self.command4.place(x=245, y=660)
        self.command5 = tk.Button(self.master, font=60, text='AC off', command=self.Button_command5)
        self.command5.place(x=345, y=660)
        self.command6 = tk.Button(self.master, font=60, text='TV on', command=self.Button_command6)
        self.command6.place(x=245, y=710)
        self.command7 = tk.Button(self.master, font=60, text='TV off', command=self.Button_command7)
        self.command7.place(x=345, y=710)


        self.Exit = tk.Button(self.master, font=60, text='Exit', command=self.Exit)
        self.Exit.place(x=280, y=555)
        #self.up_web = tk.Button(self, width=10, font=60, text='web upload')
        #self.up_web.pack()

    def Button_command1(self):
        global commandQueue
        Voice_Command("LED on brightly", commandQueue)

    def Button_command2(self):
        global commandQueue
        Voice_Command("LED on not brightly", commandQueue)

    def Button_command3(self):
        global commandQueue
        Voice_Command("LED off None", commandQueue)

    def Button_command4(self):
        global commandQueue
        Voice_Command("AC on", commandQueue)

    def Button_command5(self):
        global commandQueue
        Voice_Command("AC off", commandQueue)

    def Button_command6(self):
        global commandQueue
        Voice_Command("TV on", commandQueue)

    def Button_command7(self):
        global commandQueue
        Voice_Command("TV off", commandQueue)




        #print("TEST Voice,hi")


    def Exit(self):
        global wait_c_check
        global wait_m_check
        global send_c_check
        global activity_check

        wait_c_check = False
        wait_m_check = False
        send_c_check = False
        activity_check = False


        self.master.destroy()



def mk_dir():
    if not os.path.isdir('refs'):
        print('refs 디렉토리 생성')
        os.mkdir('refs')

def dir_list():
    return os.listdir('refs')

def wait_client(ld_wcc, wait_m_check, server_socket, messageQueue,client_socket_list):


    while ld_wcc():
        print("클라이언트 연결 대기중")
        client_socket, addr = server_socket.accept()
        client_socket_list.append(client_socket)
        th_wait_message = threading.Thread(target=wait_message,
                                           args=(lambda:wait_m_check,
                                                 client_socket,
                                                 messageQueue,
                                                 client_socket_list))
        th_wait_message.start()
    server_socket.close()
def wait_message(ld_wmc, client_socket, messageQueue, client_socket_list):

    while ld_wmc():
        
        data = client_socket.recv(1024)
        message = data.decode()
        if message.split(",")[1] == "Disconnect":
            print("Disconnect")
            print(len(client_socket_list))
            for idx, soc in enumerate(client_socket_list):
                if(soc == client_socket):
                    del client_socket_list[idx]
                    break
            print(len(client_socket_list))
            client_socket.close()
            break
        else:
            messageQueue.put(message)

def send_command(ld_scc, commandQueue, client_socket_list):
    while ld_scc():
        if commandQueue.qsize()>0:
            command = commandQueue.get(0)
            for soc in client_socket_list:
                soc.sendall(command.encode())

def activity(ld_ac,messageQueue,commandQueue):

    while ld_ac():
        if messageQueue.qsize()>0:
            message = messageQueue.get(0)
            messagelist = message.split(",")
            if messagelist[0]=="Voice":
                print("Voice")
                Voice_Command(messagelist[1],commandQueue)
                #Voice_Command("AC on", commandQueue)
            elif messagelist[0]=="Bell":
                print("Bell")
            elif messagelist[0]=="TEST":
                print("TEST")
            ##여기에 파츠 추가

def Room_change():
    global Voice_controls
    global room_img_dir
    print(Voice_controls)
    room_img_dir="refs/room/IOT"+Voice_controls[0]+Voice_controls[1]+Voice_controls[2]+".png"
    app.img_room = tk.PhotoImage(file=room_img_dir)
    app.img_viewer_room["image"] = app.img_room

def Voice_Command(message,commandQueue):
    global Voice_controls
    print("waiting voice command")
    print(message)
    print(Voice_controls)

    if(message=="door opened"):
        commandQueue.put("Door,door open")
        print(commandQueue)
    elif (message == "window opened"):
        commandQueue.put("Manager,window open")
        print(commandQueue)
    elif (message == "window closed"):
        commandQueue.put("Manager,window close")
        print(commandQueue)


    elif (message == "LED on not brightly"):
        if Voice_controls[0]!="1":
            Voice_controls[0] = "1"
            Room_change()
            print("changed")
        else:
            print("Already LED on, and not bright")
    elif (message == "LED on brightly"):
        if Voice_controls[0]!="2":
            Voice_controls[0] = "2"
            Room_change()
            print("changed")
        else:
            print("Already LED on, and bright")
    elif (message == "LED off None"):
        if Voice_controls[0]!="0":
            Voice_controls[0] = "0"
            Room_change()
            print("changed")
        else:
            print("Already LED off")
    elif (message == "AC on"):
        if Voice_controls[1]!="1":
            Voice_controls[1] = "1"
            Room_change()
            print("changed")
        else:
            print("Already AC on")
    elif (message == "AC off"):
        if Voice_controls[1]!="0":
            Voice_controls[1] = "0"
            Room_change()
            print("changed")
        else:
            print("Already AC off")
    elif (message == "TV on"):
        if Voice_controls[2] != "1":
            Voice_controls[2] = "1"
            Room_change()
            print("changed")
        else:
            print("Already TV on")
    elif (message == "TV off"):
        if Voice_controls[2] != "0":
            Voice_controls[2] = "0"
            Room_change()
            print("changed")
        else:
            print("Already TV off")


def main(app):
    global wait_c_check
    global wait_m_check
    global send_c_check
    global activity_check
    global messageQueue
    global client_socket_list
    global commandQueue
    global server_socket
    mk_dir()


    #포트 여러번 바인드하면 발생하는 에러 방지
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    #바인드:오픈한 소켓에 IP와 PORT 할당
    server_socket.bind((HOST, PORT))

    #이제 accept할 수 있음을 알림
    server_socket.listen()

    wait_c_check = True
    wait_m_check = True
    th_wait_client = threading.Thread(target= wait_client,
                                      args=(lambda:wait_c_check,
                                            wait_m_check,
                                            server_socket,
                                            messageQueue,
                                            client_socket_list))
    th_wait_client.start()

    send_c_check = True
    th_send_command = threading.Thread(target= send_command,
                                       args=(lambda:send_c_check,
                                             commandQueue,
                                             client_socket_list))
    th_send_command.start()
    activity_check = True
    th_activity = threading.Thread(target= activity,
                                   args=(lambda:activity_check,
                                         messageQueue,
                                         commandQueue))
    th_activity.start()

root = tk.Tk()
app = Application(master=root)
main(app)
app.mainloop()