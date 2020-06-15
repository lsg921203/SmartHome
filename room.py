import threading
import tkinter as tk


class Application(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.geometry('600x600+100+100')  # 윈도우창 크기 조절
        self.create_widgets()
        self.state = "0"

    def create_widgets(self):  # 여기에서 위젯 변경

        self.command1 = tk.Button(self.master, font=60, text='voice command', command=self.Button_command1)
        self.command1.place(x=245, y=610)

        self.Exit = tk.Button(self.master, font=60, text='Exit', command=self.Exit)  # 이건 지우지 말기
        self.Exit.place(x=280, y=555)
        # self.up_web = tk.Button(self, width=10, font=60, text='web upload')
        # self.up_web.pack()

    def Button_command1(self):
        global connect

        print(Msg)
        connect.sendMessage("yo")
        connect.sendMessage(Msg)

    def Exit(self):  # 이건 지우지 말기
        global checkQcheck
        global connect
        connect.sendMessage("Disconnect")
        checkQcheck = False

        self.master.destroy()


####################################################
# 여기에서 function 추가 수정
def func1():  #
    print("hello")


def func2():
    print("I'm fine and you")



#################################################################
def getCommand():
    global checkQcheck
    global connect

    checkQcheck = True

def main():
    root = tk.Tk()
    A = Application(root)
    getCommand()
    root.mainloop()


main()
