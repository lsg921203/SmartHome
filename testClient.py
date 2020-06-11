import client_connect
import threading
import queue
import tkinter as tk
import time
##########################
checkQcheck =False
HOST = "192.168.22.127"
PORT = 9999
connect = client_connect.client_connect(HOST, PORT, "TEST")
#########################################
class Application(tk.Frame):


    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.geometry('600x600+100+100')  # 윈도우창 크기 1600*900, 위치:100,100
        self.create_widgets()

    def create_widgets(self):



        self.command1 = tk.Button(self.master, font=60, text='command1', command=self.Button_command1)
        self.command1.place( x=245 , y=610)

        self.Exit = tk.Button(self.master, font=60, text='Exit', command=self.Exit)
        self.Exit.place(x=280, y=555)
        #self.up_web = tk.Button(self, width=10, font=60, text='web upload')
        #self.up_web.pack()

    def Button_command1(self):
        global connect
        connect.sendMessage("yo")



    def Exit(self):
        global checkQcheck
        global connect
        connect.sendMessage("Disconnect")
        checkQcheck = False

        self.master.destroy()
####################################################
def func1():
    print("hello")

def func2():
    print("I'm fine and you")

def checkQueue(checkQcheck,commandQ):
    global  connect
    while checkQcheck:
        if(commandQ.qsize()>0):
            message = commandQ.get(0)
            if message == "hi":
                func1()
            elif message == "how are you":
                func2()
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
