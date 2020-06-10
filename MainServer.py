import _tkinter as tk
import socket, os
import threading
import queue

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.geometry('400x600+100+100')  # 윈도우창 크기 1600*900, 위치:100,100
        self.master.resizable(True, True)
        self.pack()
        self.effect = ['negative', 'sketch', 'pastel', 'watercolor']
        self.create_widgets()

    def create_widgets(self):
        self.ra = []
        self.dir_l = tk.Label(self, width=10, font=60, text='폴더경로:')
        self.dir_l.pack()
        self.dir_e = tk.Entry(self, width=30)  # 입력창
        self.dir_e.pack()

        self.file_l = tk.Label(self, width=10, font=60, text='파일명:')
        self.file_l.pack()
        self.file_e = tk.Entry(self, width=30)  # 입력창
        self.file_e.pack()

        self.save_btn = tk.Button(self, width=10, font=60, text='촬영')
        self.save_btn.pack()

        self.effect_l = tk.Label(self, width=10, font=60, text='사진효과')
        self.effect_l.pack()

        self.radioval = tk.IntVar()
        for idx, i in enumerate(self.effect):
            self.ra.append(tk.Radiobutton(self, text=i, variable=self.radioval, value=idx))
            self.ra[len(self.ra) - 1].pack()

        self.img = tk.PhotoImage(file="")
        self.img_viewer = tk.Label(self.master, image=self.img)
        self.img_viewer.pack()

        self.fname = tk.Label(self.master, text='')
        self.fname.pack()

        self.up_soc = tk.Button(self, width=10, font=60, text='socket upload')
        self.up_soc.pack()

        self.up_web = tk.Button(self, width=10, font=60, text='web upload')
        self.up_web.pack()

root = tk.Tk()
app = Application(master=root)
wait_c_check = False
wait_m_check = False
messageQueue = queue.Queue()
th_wait_message_list = []
def mk_dir():
    if not os.path.isdir('refs'):
        print('refs 디렉토리 생성')
        os.mkdir('refs')

def dir_list():
    return os.listdir('refs')

def wait_client(wait_c_check, wait_m_check, server_socket, messageQueue,th_wait_message_list):
    while wait_c_check:
        client_socket, addr = server_socket.accept()
        th_wait_message_list.append(client_socket)
        th_wait_message = threading.Thread(target=wait_client,args=(lambda:wait_m_check,client_socket,messageQueue))

def wait_message(wait_m_check, client_socket,messageQueue):
    while wait_m_check:
        data = client_socket.recv(1024)
        menu = data.decode()
        messageQueue.put(menu)


def main():
    mk_dir()
    HOST = '192.168.22.127'#'192.168.103.61'  #server ip
    PORT = 9999         #server port

    #server socket open. socket.AF_INET:주소체계(IPV4), socket.SOCK_STREAM:tcp
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #포트 여러번 바인드하면 발생하는 에러 방지
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    #바인드:오픈한 소켓에 IP와 PORT 할당
    server_socket.bind((HOST, PORT))

    #이제 accept할 수 있음을 알림
    server_socket.listen()

    th_wait_client = threading.Thread(target= wait_client,
                                      args=(lambda:wait_c_check,
                                            lambda:wait_m_check,
                                            server_socket,
                                            messageQueue,
                                            th_wait_message_list))

    #th_command



app.mainloop()