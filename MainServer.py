import _tkinter as tk
import socket, os

def mk_dir():
    if not os.path.isdir('refs'):
        print('refs 디렉토리 생성')
        os.mkdir('refs')

def dir_list():
    return os.listdir('refs')