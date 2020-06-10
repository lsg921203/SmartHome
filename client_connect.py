import socket, os
import threading
import queue
class client_connect():
    def __init__(self,HOST,PORT,PartsName):
        self.HOST = HOST  # '192.168.103.61'  #server ip
        self.PORT = PORT  # server port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.HOST, self.PORT))
        self.recvCommandQ = queue.Queue()
        self.data = ""
        self.PartsName = PartsName

    def waitCommand(self):
        self.data = self.client_socket.recv(1024)
        self.data = self.data.decode()
        SplitCommand = self.data.split(",")
        targetParts = SplitCommand[0].split("/")
        targetCheck = False
        for tp in targetParts:
            if(tp == self.PartsName):
                targetCheck = True
                break
        #