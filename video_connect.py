import socket, os

import time
class video_connect:
    def __init__(self,HOST,PORT,VideoNum):
        self.HOST = HOST  # '192.168.103.61'  #server ip
        self.PORT = PORT  # server port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.HOST, self.PORT))

        self.VideoNum = VideoNum

    def sendImage(self,path):
        f = open(path, 'rb')
        body = f.read()
        f.close()

        self.client_socket.sendall(body)


    def closeSoc(self):
        self.client_socket.close()