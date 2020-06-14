import tkinter as tk
from tkinter import messagebox
import socket, os
import threading
import queue
import sys
import time

messageQueue = queue.Queue()
commandQueue = queue.Queue()
vedio1_frame_q = queue.Queue()
vedio2_frame_q = queue.Queue()
frame_queue_list = [vedio1_frame_q,vedio2_frame_q]
video_socket_list = [None,None]
client_socket_list = []
Parts_list = ["Voice","Bell"]
wait_c_check = False
wait_m_check = False
wait_v_check = False
wait_f_check = False
send_c_check = False
activity_check = False


HOST = "localhost"#'192.168.22.127'#'192.168.103.61'  #server ip
PORT = 9999         #server port
VIDEOPORT1 = 8888
VIDEOPORT2 = 7777
#server socket open. socket.AF_INET:주소체계(IPV4), socket.SOCK_STREAM:tcp
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_video_socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_video_socket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
class Application(tk.Frame):
    global commandQueue
    global wait_c_check
    global wait_m_check
    global send_c_check
    global activity_check

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.geometry('670x300+100+100')  # 윈도우창 크기 1600*900, 위치:100,100
        #self.master.resizable(True, True)
        #self.pack()
        self.effect = ['negative', 'sketch', 'pastel', 'watercolor']
        self.create_widgets()
        self.video_q_reader_check = True



    def create_widgets(self):

        self.img = tk.PhotoImage(file="refs/mic_img.png")#file="refs/mic_img.png"
        self.img_viewer1 = tk.Canvas(height=240, width=320)
        self.img_viewer1.place(x=10,y=10)
        self.img_viewer1.create_image(0,0,anchor='nw',image=self.img)

        self.img_viewer2 = tk.Canvas(height=240, width=320)
        self.img_viewer2.place(x=340, y=10)
        self.img_viewer2.create_image(0, 0, anchor='nw', image=self.img)
        #self.fname = tk.Label(self.master, text='')
        #self.fname.pack()

        self.command1 = tk.Button(self.master, font=60, text='command1', command=self.Button_command1)
        self.command1.place( x=10 , y=610)

        self.command2 = tk.Button(self.master, font=60, text='command2', command=self.Button_command2)
        self.command2.place(x=130, y=610)

        self.command3 = tk.Button(self.master, font=60, text='command3', command=self.Button_command3)
        self.command3.place(x=250, y=610)

        self.Exit = tk.Button(self.master, font=60, text='Exit', command=self.Exit)
        self.Exit.place(x=320, y=260)

        #self.up_web = tk.Button(self, width=10, font=60, text='web upload')
        #self.up_web.pack()



    def Button_command1(self):
        global commandQueue
        commandQueue.put("Door,door open")

        #print("TEST Voice,hi")
    def Button_command2(self):
        global commandQueue
        commandQueue.put("Door,warning")

    def Button_command3(self):
        global commandQueue
        commandQueue.put("Video,play")

    def Exit(self):
        global wait_c_check
        global wait_m_check
        global send_c_check
        global activity_check
        global wait_v_check
        global wait_f_check

        wait_c_check = False
        wait_m_check = False
        send_c_check = False
        activity_check = False
        wait_v_check = False
        wait_f_check = False
        self.video_q_reader_check = False

        self.master.destroy()



def mk_dir():
    if not os.path.isdir('refs'):
        print('refs 디렉토리 생성')
        os.mkdir('refs')

def dir_list():
    return os.listdir('refs')

def wait_client(ld_wcc, wait_m_check, server_socket, messageQueue,client_socket_list):
    server_socket.settimeout(0.5)
    while ld_wcc():
        try:
            client_socket, addr = server_socket.accept()
        except socket.timeout :
            continue
        print("클라이언트 연결")
        client_socket_list.append(client_socket)
        th_wait_message = threading.Thread(target=wait_message,
                                           args=(lambda:wait_m_check(),
                                                 client_socket,
                                                 messageQueue,
                                                 client_socket_list))
        th_wait_message.start()
    print("close wait client thread!")
    server_socket.close()
def wait_message(ld_wmc, client_socket, messageQueue, client_socket_list):
    client_socket.settimeout(0.5)
    while ld_wmc():
        try:
            data = client_socket.recv(1024)
        except socket.timeout :
            continue
        except Exception as e:
            print(e)
            break
        message = data.decode()
        if message.split(",")[1] == "Disconnect":
            print("Disconnect")
            print(len(client_socket_list))
            for idx, soc in enumerate(client_socket_list):
                if(soc == client_socket):
                    del client_socket_list[idx]
                    break
            print(len(client_socket_list))

            break
        else:
            messageQueue.put(message)
    client_socket.close()
    print("close wait message thread!")

def wait_video(ld_wvc,wait_frame_check,video_num, server_socket,video_list):
    print("start wait_video thread")
    server_socket.settimeout(0.5)
    while ld_wvc():
        try:
            client_socket, addr = server_socket.accept()
        except socket.timeout:
            continue
        print("video1 연결")
        video_list[video_num] = client_socket
        th_wait_message = threading.Thread(target=wait_frame,
                                           args=(lambda: wait_frame_check(),
                                                 client_socket,
                                                 video_num,
                                                 video_list))
        th_wait_message.start()
    print("close wait video"+str(video_num)+" thread!")
    server_socket.close()
def wait_frame(ld_wfc, client_socket,video_num, video_list):
    global frame_queue_list
    client_socket.settimeout(0.5)
    while ld_wfc():
        try:
            data = client_socket.recv(50000)
        except socket.timeout:
            continue
        except Exception as e:
            print(e)
            break
        frame_queue_list[video_num].put(data)

    video_list[video_num] = None
    client_socket.close()


    print("close wait message thread!")

def send_command(ld_scc, commandQueue, client_socket_list):
    while ld_scc():
        if commandQueue.qsize()>0:
            command = commandQueue.get(0)
            for soc in client_socket_list:
                soc.sendall(command.encode())
    print("close send command thread!")

def video_q_reader(app,videoNum):
    global frame_queue_list
    print("start video_q_reader thread")
    if (videoNum == 0):
        path = 'refs/video1_frame.png'
    elif (videoNum == 1):
        path = 'refs/video2_frame.png'

    while(app.video_q_reader_check):
        try:
            if (frame_queue_list[videoNum].qsize() > 0):
                f = open(path, 'wb')
                f.write(frame_queue_list[videoNum].get(0))
                f.close()
                ################## 이거 하던중
                image = tk.PhotoImage(file=path)
                if (videoNum == 0):
                    app.img_viewer1.create_image(0, 0, anchor='nw', image=image)
                elif (videoNum == 1):
                    app.img_viewer2.create_image(0, 0, anchor='nw', image=image)
        except Exception as e:
            print(e)
            break
    print("close video_q_reader thread")
###################################################################
def Voice_Command(message,commandQueue):
    if(message=="door open"):
        command = "Bell/kuku,Open"
        commandQueue.put()
###################################################################
def activity(ld_ac,messageQueue,commandQueue):

    while ld_ac():
        if messageQueue.qsize()>0:
            message = messageQueue.get(0)
            messagelist = message.split(",")
            if messagelist[0]=="Voice":
                print("Voice")
                Voice_Command(messagelist[1],commandQueue)
            elif messagelist[0]=="Door":
                print("Door")
            elif messagelist[0]=="TEST":
                print("TEST")
            ##여기에 파츠 추가
    print("close activity thread!")





def main(app):
    global wait_c_check
    global wait_m_check
    global send_c_check
    global activity_check
    global messageQueue
    global client_socket_list
    global commandQueue
    global server_socket
    global server_video_socket1
    global server_video_socket2
    global video_socket_list
    mk_dir()


    #포트 여러번 바인드하면 발생하는 에러 방지
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_video_socket1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_video_socket2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #바인드:오픈한 소켓에 IP와 PORT 할당
    server_socket.bind((HOST, PORT))
    server_video_socket1.bind((HOST, VIDEOPORT1))
    server_video_socket2.bind((HOST, VIDEOPORT2))
    #이제 accept할 수 있음을 알림
    server_socket.listen()
    server_video_socket1.listen()
    server_video_socket2.listen()

    wait_c_check = True
    wait_m_check = True
    th_wait_client = threading.Thread(target= wait_client,
                                      args=(lambda: wait_c_check,
                                            lambda: wait_m_check,
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

    global wait_v_check
    global wait_f_check
    wait_v_check = True
    wait_f_check = True

    th = threading.Thread(target=wait_video,
                          args=(lambda: wait_v_check,
                                lambda: wait_f_check,
                                0,
                                server_video_socket1,
                                video_socket_list))
    th.start()

    th = threading.Thread(target=wait_video,
                          args=(lambda: wait_v_check,
                                lambda: wait_f_check,
                                1,
                                server_video_socket2,
                                video_socket_list))
    th.start()

    th = threading.Thread(target=video_q_reader,
                                args=(app,0))
    th.start()
    th = threading.Thread(target=video_q_reader,
                                args=(app,1))
    th.start()

root = tk.Tk()
app = Application(master=root)
main(app)
app.mainloop()