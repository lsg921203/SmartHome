import time,serial
class voice_machine:
    def __init__(self,targetParts):
        port="/dev/ttyAMA0"
        rate = 9600
        self.ser=serial.Serial(port,rate)
        self.ser.parity = serial.PARITY_NONE
        self.ser.bytesize=serial.EIGHTBITS
        self.Modes=["hear2Act","userSetting"]
        #self.targetParts=[["door","closed"], ["LED","off","None"], ["window","closed"], ["AC","off"], ["TV","off"]]
        self.targetParts=targetParts
        
    def mode(self,Mode):
        if Mode==self.Modes[0]:
            print(self.Modes[0])
            if self.ser.isOpen():
                self.ser.close()
            self.ser.open()
            #print('serial open')
            self.ser.flushInput()
            self.ser.flushOutput()
            time.sleep(0.1)
            #print('test command')
            self.ser.write(serial.to_bytes([0xAA]))
            self.ser.write(serial.to_bytes([0x21]))
            time.sleep(0.3)
            print('hearing...')
            return self.hear2Act()
        elif Mode==self.Modes[1]:
            print(self.Modes[1])
            
    def hear2Act(self):
        cnt=0
        msg=""
        try:
            while True:#group 1 question
                print("1.hyunkwanmoon, 2.LED 3.changmoon 4.Aircon 5.TV")
                command=self.ser.readline()
                print(command)
                if command==b'Result:11\r\n':#door
                    self.ser.write(serial.to_bytes([0xAA]))
                    self.ser.write(serial.to_bytes([0x00]))
                    print('waiting')
                    time.sleep(0.3)
                    command=self.ser.readline()
                    print(command)
                    self.ser.write(serial.to_bytes([0xAA]))
                    self.ser.write(serial.to_bytes([0x22]))
                    print('waiting')
                    time.sleep(0.3)
                    command=self.ser.readline()
                    print(command)
                    print("1.yeoluju")
                    while True: #group 2 question
                        command=self.ser.readline()
                        if command==b'Result:13\r\n':
                            if self.targetParts[0][1]!="opened":
                                self.targetParts[0][1]="opened"
                                print("door opened")
                                self.ser.write(serial.to_bytes([0xAA]))
                                self.ser.write(serial.to_bytes([0x00]))
                                self.ser.close()
                                print('waiting')
                                return self.targetParts[0]###############################
                            else:
                                print("Already door opened")
                                self.ser.write(serial.to_bytes([0xAA]))
                                self.ser.write(serial.to_bytes([0x00]))
                                self.ser.close()
                                print('waiting')
                                return self.targetParts[0]###############################
                                
                    
                elif command==b'Result:12\r\n':#LED
                    self.ser.write(serial.to_bytes([0xAA]))
                    self.ser.write(serial.to_bytes([0x00]))
                    print('waiting')
                    time.sleep(0.3)
                    command=self.ser.readline()
                    print(command)
                    self.ser.write(serial.to_bytes([0xAA]))
                    self.ser.write(serial.to_bytes([0x22]))
                    print('waiting')
                    time.sleep(0.3)
                    print("1.kyuzo 2.kkuzo")
                    while True:#group 2 question
                        command=self.ser.readline()
                        if command==b'Result:12\r\n':
                            if self.targetParts[1][1]!="on":
                                self.targetParts[1][1]="on"
                                print("LED turned on")
                                
                            else:
                                print("Already LED on")
                            self.ser.write(serial.to_bytes([0xAA]))
                            self.ser.write(serial.to_bytes([0x00]))
                            print('waiting')
                            time.sleep(0.3)
                            command=self.ser.readline()
                            print(command)
                            self.ser.write(serial.to_bytes([0xAA]))
                            self.ser.write(serial.to_bytes([0x31]))
                            print('waiting')
                            time.sleep(0.3)
                            while True:#group 3 question
                                print("1.barkye 2.udupkye")
                                command=self.ser.readline()
                                if command==b'Result:11\r\n':
                                    if self.targetParts[1][2]!="brightly":
                                        self.targetParts[1][2]="brightly"
                                        print("LED turned on brightly")
                                        self.ser.write(serial.to_bytes([0xAA]))
                                        self.ser.write(serial.to_bytes([0x00]))
                                        print('waiting')
                                        self.ser.close()
                                        return self.targetParts[1]###############################
                                    else:
                                        print("Already LED turned on brightly")
                                        self.ser.write(serial.to_bytes([0xAA]))
                                        self.ser.write(serial.to_bytes([0x00]))
                                        print('waiting')
                                        self.ser.close()
                                        return self.targetParts[1]###############################
                                elif command==b'Result:12\r\n':
                                    if self.targetParts[1][2]!="not brightly":
                                        self.targetParts[1][2]="not brightly"
                                        print("LED turned on brightly")
                                        self.ser.write(serial.to_bytes([0xAA]))
                                        self.ser.write(serial.to_bytes([0x00]))
                                        print('waiting')
                                        self.ser.close()
                                        return self.targetParts[1]###############################
                                    else:
                                        print("Already LED turned on not brightly")
                                        self.ser.write(serial.to_bytes([0xAA]))
                                        self.ser.write(serial.to_bytes([0x00]))
                                        print('waiting')
                                        self.ser.close()
                                        return self.targetParts[1]###############################
                                elif command==b'Result:15\r\n':
                                        print("Welcome !")

                        elif command==b'Result:15\r\n':
                             if self.targetParts[1][1]!="off":
                                 self.targetParts[1][1]="off"
                                 self.targetParts[1][2]="None"
                                 print("LED turned off")
                                 self.ser.write(serial.to_bytes([0xAA]))
                                 self.ser.write(serial.to_bytes([0x00]))
                                 print('waiting')
                                 self.ser.close()
                                 return self.targetParts[1]###############################
                             else:
                                 print("Already LED turned off")
                                 self.ser.write(serial.to_bytes([0xAA]))
                                 self.ser.write(serial.to_bytes([0x00]))
                                 print('waiting')
                                 self.ser.close()
                                 return self.targetParts[1]###############################
                elif command==b'Result:13\r\n':#window
                    self.ser.write(serial.to_bytes([0xAA]))
                    self.ser.write(serial.to_bytes([0x00]))
                    print('waiting')
                    time.sleep(0.3)
                    command=self.ser.readline()
                    print(command)
                    self.ser.write(serial.to_bytes([0xAA]))
                    self.ser.write(serial.to_bytes([0x22]))
                    print('waiting')
                    time.sleep(0.3)
                    print("1.yeoluju 2.dadaju")
                    while True: #group 2 question
                        command=self.ser.readline()
                        if command==b'Result:13\r\n':
                            if self.targetParts[2][1]!="opened":
                                self.targetParts[2][1]="opened"
                                print("window opened")
                                self.ser.write(serial.to_bytes([0xAA]))
                                self.ser.write(serial.to_bytes([0x00]))
                                print('waiting')
                                self.ser.close()
                                return self.targetParts[2]###############################
                            else:
                                print("Already window opened")
                                self.ser.write(serial.to_bytes([0xAA]))
                                self.ser.write(serial.to_bytes([0x00]))
                                print('waiting')
                                self.ser.close()
                                return self.targetParts[2]###############################
                        elif command==b'Result:11\r\n':
                            if self.targetParts[2][1]!="closed":
                                self.targetParts[2][1]="closed"
                                print("window opened")
                                self.ser.write(serial.to_bytes([0xAA]))
                                self.ser.write(serial.to_bytes([0x00]))
                                print('waiting')
                                self.ser.close()
                                return self.targetParts[2]###############################
                            else:
                                print("Already window closed")
                                self.ser.write(serial.to_bytes([0xAA]))
                                self.ser.write(serial.to_bytes([0x00]))
                                print('waiting')
                                self.ser.close()
                                return self.targetParts[2]###############################
                elif command==b'Result:14\r\n':#AC
                    self.ser.write(serial.to_bytes([0xAA]))
                    self.ser.write(serial.to_bytes([0x00]))
                    print('waiting')
                    time.sleep(0.3)
                    command=self.ser.readline()
                    print(command)
                    self.ser.write(serial.to_bytes([0xAA]))
                    self.ser.write(serial.to_bytes([0x22]))
                    print('waiting')
                    time.sleep(0.3)
                    print("1.teuluju 2.kkujo")
                    while True: #group 2 question
                        command=self.ser.readline()
                        if command==b'Result:14\r\n':
                            if self.targetParts[3][1]!="on":
                                self.targetParts[3][1]="on"
                                print("AC turned on")
                                self.ser.write(serial.to_bytes([0xAA]))
                                self.ser.write(serial.to_bytes([0x00]))
                                print('waiting')
                                self.ser.close()
                                return self.targetParts[3]###############################
                            else:
                                print("Already AC on")
                                self.ser.write(serial.to_bytes([0xAA]))
                                self.ser.write(serial.to_bytes([0x00]))
                                print('waiting')
                                self.ser.close()
                                return self.targetParts[3]###############################
                        elif command==b'Result:15\r\n':
                            if self.targetParts[3][1]!="off":
                                self.targetParts[3][1]="off"
                                print("AC turned off")
                                self.ser.write(serial.to_bytes([0xAA]))
                                self.ser.write(serial.to_bytes([0x00]))
                                print('waiting')
                                self.ser.close()
                                return self.targetParts[3]###############################
                            else:
                                print("Already AC off")
                                self.ser.write(serial.to_bytes([0xAA]))
                                self.ser.write(serial.to_bytes([0x00]))
                                print('waiting')
                                self.ser.close()
                                return self.targetParts[3]###############################
                            
                elif command==b'Result:15\r\n':#TV
                    self.ser.write(serial.to_bytes([0xAA]))
                    self.ser.write(serial.to_bytes([0x00]))
                    print('waiting')
                    time.sleep(0.3)
                    command=self.ser.readline()
                    print(command)
                    self.ser.write(serial.to_bytes([0xAA]))
                    self.ser.write(serial.to_bytes([0x22]))
                    print('waiting')
                    time.sleep(0.3)
                    print("1.teuluju 2.kkujo")
                    while True: #group 2 question
                        command=self.ser.readline()
                        if command==b'Result:14\r\n':
                            if self.targetParts[4][1]!="on":
                                self.targetParts[4][1]="on"
                                print("TV turned on")
                                self.ser.write(serial.to_bytes([0xAA]))
                                self.ser.write(serial.to_bytes([0x00]))
                                print('waiting')
                                self.ser.close()
                                return self.targetParts[4]###############################
                            else:
                                print("Already TV on")
                                self.ser.write(serial.to_bytes([0xAA]))
                                self.ser.write(serial.to_bytes([0x00]))
                                print('waiting')
                                self.ser.close()
                                return self.targetParts[4]###############################
                        elif command==b'Result:15\r\n':
                            if self.targetParts[4][1]!="off":
                                self.targetParts[4][1]="off"
                                print("TV turned off")
                                self.ser.write(serial.to_bytes([0xAA]))
                                self.ser.write(serial.to_bytes([0x00]))
                                print('waiting')
                                self.ser.close()
                                return self.targetParts[4]###############################
                            else:
                                print("Already TV off")
                                self.ser.write(serial.to_bytes([0xAA]))
                                self.ser.write(serial.to_bytes([0x00]))
                                print('waiting')
                                self.ser.close()
                                return self.targetParts[4]###############################

        except KeyboardInterrupt:
            print('voice command ended.')
            pass
        finally:
            self.ser.write(serial.to_bytes([0xAA]))
            self.ser.write(serial.to_bytes([0x00]))
            time.sleep(0.3)
            self.ser.close()
