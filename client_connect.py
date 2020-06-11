import socket, os
import threading
import queue
class client_connect:
    def __init__(self,HOST,PORT,PartsName):
        self.HOST = HOST  # '192.168.103.61'  #server ip
        self.PORT = PORT  # server port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.HOST, self.PORT))
        self.recvCommandQ = queue.Queue()
        self.data = ""
        self.PartsName = PartsName
        self.waitCommandCheck = True
        self.t1 = threading.Thread(target=self.waitCommand)
        self.t1.start()


    def waitCommand(self):
        while self.waitCommandCheck:
            self.data = self.client_socket.recv(1024)
            self.data = self.data.decode()
            SplitCommand = self.data.split(",")
            targetParts = SplitCommand[0].split("/")
            targetCheck = False
            for tp in targetParts:
                if (tp == self.PartsName):
                    targetCheck = True
                    break
            if (targetCheck):
                self.recvCommandQ.put(SplitCommand[1])

    def sendMessage(self,message):
        data = self.PartsName + "," + message
        data = data.encode()
        self.client_socket.sendall(data)

    def getCommandQueue(self):
        return  self.recvCommandQ

    def exitWaitCommand(self):
        waitCommandCheck = False