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
wait_c_check = False
wait_m_check = False
send_c_check = False
activity_check = False

HOST = '192.168.22.127'#'192.168.103.61'  #server ip
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

        #self.fname = tk.Label(self.master, text='')
        #self.fname.pack()

        self.command1 = tk.Button(self.master, font=60, text='command1', command=self.Button_command1)
        self.command1.place( x=245 , y=610)

        self.Exit = tk.Button(self.master, font=60, text='Exit', command=self.Exit)
        self.Exit.place(x=280, y=555)
        #self.up_web = tk.Button(self, width=10, font=60, text='web upload')
        #self.up_web.pack()

    def Button_command1(self):
        global commandQueue
        commandQueue.put("TEST,hi")
        commandQueue.put("TEST/Voice,hi")
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

def wait_client(wait_c_check, wait_m_check, server_socket, messageQueue,client_socket_list):


    while wait_c_check():
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
def wait_message(wait_m_check, client_socket, messageQueue, client_socket_list):

    while wait_m_check():
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
            wait_m_check = False
        else:
            messageQueue.put(message)

def send_command(send_c_check, commandQueue, client_socket_list):
    while send_c_check():
        if commandQueue.qsize()>0:
            command = commandQueue.get(0)
            for soc in client_socket_list:
                soc.sendall(command.encode())

def activity(activity_check,messageQueue,commandQueue):

    while activity_check():
        if messageQueue.qsize()>0:
            message = messageQueue.get(0)
            messagelist = message.split(",")
            if messagelist[0]=="Voice":
                print("Voice")
                Voice_Command(messagelist[1],commandQueue)
            elif messagelist[0]=="Bell":
                print("Bell")
            elif messagelist[0]=="TEST":
                print("TEST")
            ##여기에 파츠 추가


def Voice_Command(message,commandQueue):
    if(message=="door open"):
        command = "Bell/kuku,Open"
        commandQueue.put()



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
                                            lambda:wait_m_check,
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