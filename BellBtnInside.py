import RPi.GPIO as GPIO
import time, os, threading
import tkinter as tk
from tkinter import *
from tkinter import ttk

GPIO.setmode(GPIO.BOARD)

SW = 7
pins = [11, 13, 15]
pin = 37
data = [260, 290, 330, 340, 380, 430, 490, 510]

GPIO.setup(pin, GPIO.OUT)  # speaker
buz = GPIO.PWM(pin, 100)

GPIO.setup(SW, GPIO.IN)  # switch


def bellSPK():
    buz.start(100)
    buz.ChangeDutyCycle(90)
    buz.ChangeFrequency(data[3])
    time.sleep(1)
    buz.ChangeFrequency(1)
    time.sleep(0.03)
    buz.ChangeDutyCycle(90)
    buz.ChangeFrequency(data[3])
    time.sleep(1)
    buz.ChangeFrequency(1)
    time.sleep(0.03)
    buz.stop()


while 1:
    GPIO.wait_for_edge(SW, GPIO.RISING, 300)
    print('pushed')
    bellSPK()
    time.sleep(3)
    print('ready')

print('stop')
GPIO.cleanup()