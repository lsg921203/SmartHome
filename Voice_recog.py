import os, socket
import time

HOST = '192.168.137.1'
PORT = 9999

import time, serial

port = "/dev/ttyAMA0"
rate = 9600
ser = serial.Serial(port, rate)
ser.parity = serial.PARITY_NONE
ser.bytesize = serial.EIGHTBITS

try:
    if ser.isOpen():
        ser.close()
    ser.open()
    print('serial open')
    ser.flushInput()
    ser.flushOutput()
    time.sleep(0.1)
    print('test command')
    ser.write(serial.to_bytes([0xAA]))
    ser.write(serial.to_bytes([0x21]))
    time.sleep(0.3)
    print('input start')
    cnt = 0
    msg = ""
    while True:
        command = ser.readline()
        print(command)
        print("1.Munyeolujo, 2.bullkyu 3.kurtain kuddu 4.Aircon teulu 5.TV teulu")
        if command == b'Result:11\r\n':
            msg = 'door open'
            print(msg)
            '''
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((HOST, PORT))
            client_socket.sendall(msg.encode())
            client_socket.close()
            '''

        elif command == b'Result:12\r\n':
            msg = 'light on'
            print(msg)
            '''
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((HOST, PORT))
            client_socket.sendall(msg.encode())
            client_socket.close()
            '''

        elif command == b'Result:13\r\n':
            msg = 'curtain open'
            print(msg)
            '''
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((HOST, PORT))
            client_socket.sendall(msg.encode())
            client_socket.close()
            '''

        elif command == b'Result:14\r\n':
            msg = 'AC on'
            print(msg)
            '''
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((HOST, PORT))
            client_socket.sendall(msg.encode())
            client_socket.close()
            '''
        elif command == b'Result:15\r\n':
            msg = 'TV on'
            print(msg)
            '''
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((HOST, PORT))
            client_socket.sendall(msg.encode())
            client_socket.close()
            '''

        time.sleep(1)

except KeyboardInterrupt:
    print('testing end')
    pass

finally:
    ser.close()