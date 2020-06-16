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
            return self.hear2Act2()
        elif Mode==self.Modes[1]:
            print(self.Modes[1])

    def wait_command(self):
        self.ser.write(serial.to_bytes([0xAA]))
        self.ser.write(serial.to_bytes([0x00]))

    '''
        def hear2Act(self):
            cnt=0
            msg=""
            try:
                print("1.hyunkwanmoon, 2.LED 3.changmoon 4.Aircon 5.TV")
                command = self.ser.readline()
                print(command)

                if command == b'Result:11\r\n':  # door
                    self.wait_command()

                    print('waiting')
                    time.sleep(0.3)

                    command = self.ser.readline()
                    print(command)

                    self.ser.write(serial.to_bytes([0xAA]))
                    self.ser.write(serial.to_bytes([0x22]))

                    print('waiting')
                    print("1.yeoluju")
                    time.sleep(0.3)

                    command = self.ser.readline()
                    print(command)


                    command = self.ser.readline()
                    if command == b'Result:13\r\n':
                        if self.targetParts[0][1] != "opened":
                            self.targetParts[0][1] = "opened"
                            print("door opened")
                            self.wait_command()
                            self.ser.close()
                            print('waiting')
                            return self.targetParts[0]  ###############################
                        else:
                            print("Already door opened")
                            self.wait_command()
                            self.ser.close()
                            print('waiting')
                            return self.targetParts[0]  ###############################


                elif command == b'Result:12\r\n':  # LED
                    self.wait_command()
                    print('waiting')
                    time.sleep(0.3)
                    command = self.ser.readline()
                    print(command)
                    self.ser.write(serial.to_bytes([0xAA]))
                    self.ser.write(serial.to_bytes([0x22]))
                    print('waiting')
                    time.sleep(0.3)
                    print("1.kyuzo 2.kkuzo")
                    # group 2 question
                    command = self.ser.readline()
                    if command == b'Result:12\r\n':
                        if self.targetParts[1][1] != "on":
                            self.targetParts[1][1] = "on"
                            print("LED turned on")

                        else:
                            print("Already LED on")
                        self.wait_command()
                        print('waiting')
                        time.sleep(0.3)
                        command = self.ser.readline()
                        print(command)
                        self.ser.write(serial.to_bytes([0xAA]))
                        self.ser.write(serial.to_bytes([0x31]))
                        print('waiting')
                        time.sleep(0.3)
                        while True:  # group 3 question
                            print("1.barkye 2.udupkye")
                            command = self.ser.readline()
                            if command == b'Result:11\r\n':
                                if self.targetParts[1][2] != "brightly":
                                    self.targetParts[1][2] = "brightly"
                                    print("LED turned on brightly")
                                    self.wait_command()
                                    print('waiting')
                                    self.ser.close()
                                    return self.targetParts[1]  ###############################
                                else:
                                    print("Already LED turned on brightly")
                                    self.wait_command()
                                    print('waiting')
                                    self.ser.close()
                                    return self.targetParts[1]  ###############################
                            elif command == b'Result:12\r\n':
                                if self.targetParts[1][2] != "not brightly":
                                    self.targetParts[1][2] = "not brightly"
                                    print("LED turned on brightly")
                                    self.wait_command()
                                    print('waiting')
                                    self.ser.close()
                                    return self.targetParts[1]  ###############################
                                else:
                                    print("Already LED turned on not brightly")
                                    self.wait_command()
                                    print('waiting')
                                    self.ser.close()
                                    return self.targetParts[1]  ###############################
                            elif command == b'Result:15\r\n':
                                print("Welcome !")

                    elif command == b'Result:15\r\n':
                        if self.targetParts[1][1] != "off":
                            self.targetParts[1][1] = "off"
                            self.targetParts[1][2] = "None"
                            print("LED turned off")
                            self.wait_command()
                            print('waiting')
                            self.ser.close()
                            return self.targetParts[1]  ###############################
                        else:
                            print("Already LED turned off")
                            self.wait_command()
                            print('waiting')
                            self.ser.close()
                            return self.targetParts[1]  ###############################
                elif command == b'Result:13\r\n':  # window
                    self.wait_command()
                    print('waiting')
                    time.sleep(0.3)
                    command = self.ser.readline()
                    print(command)
                    self.ser.write(serial.to_bytes([0xAA]))
                    self.ser.write(serial.to_bytes([0x22]))
                    print('waiting')
                    time.sleep(0.3)
                    print("1.yeoluju 2.dadaju")
                    while True:  # group 2 question
                        command = self.ser.readline()
                        if command == b'Result:13\r\n':
                            if self.targetParts[2][1] != "opened":
                                self.targetParts[2][1] = "opened"
                                print("window opened")
                                self.wait_command()
                                print('waiting')
                                self.ser.close()
                                return self.targetParts[2]  ###############################
                            else:
                                print("Already window opened")
                                self.wait_command()
                                print('waiting')
                                self.ser.close()
                                return self.targetParts[2]  ###############################
                        elif command == b'Result:11\r\n':
                            if self.targetParts[2][1] != "closed":
                                self.targetParts[2][1] = "closed"
                                print("window opened")
                                self.wait_command()
                                print('waiting')
                                self.ser.close()
                                return self.targetParts[2]  ###############################
                            else:
                                print("Already window closed")
                                self.wait_command()
                                print('waiting')
                                self.ser.close()
                                return self.targetParts[2]  ###############################
                elif command == b'Result:14\r\n':  # AC
                    self.wait_command()
                    print('waiting')
                    time.sleep(0.3)
                    command = self.ser.readline()
                    print(command)
                    self.ser.write(serial.to_bytes([0xAA]))
                    self.ser.write(serial.to_bytes([0x22]))
                    print('waiting')
                    time.sleep(0.3)
                    print("1.teuluju 2.kkujo")
                    while True:  # group 2 question
                        command = self.ser.readline()
                        if command == b'Result:14\r\n':
                            if self.targetParts[3][1] != "on":
                                self.targetParts[3][1] = "on"
                                print("AC turned on")
                                self.wait_command()
                                print('waiting')
                                self.ser.close()
                                return self.targetParts[3]  ###############################
                            else:
                                print("Already AC on")
                                self.wait_command()
                                print('waiting')
                                self.ser.close()
                                return self.targetParts[3]  ###############################
                        elif command == b'Result:15\r\n':
                            if self.targetParts[3][1] != "off":
                                self.targetParts[3][1] = "off"
                                print("AC turned off")
                                self.wait_command()
                                print('waiting')
                                self.ser.close()
                                return self.targetParts[3]  ###############################
                            else:
                                print("Already AC off")
                                self.wait_command()
                                print('waiting')
                                self.ser.close()
                                return self.targetParts[3]  ###############################

                elif command == b'Result:15\r\n':  # TV
                    self.wait_command()
                    print('waiting')
                    time.sleep(0.3)
                    command = self.ser.readline()
                    print(command)
                    self.ser.write(serial.to_bytes([0xAA]))
                    self.ser.write(serial.to_bytes([0x22]))
                    print('waiting')
                    time.sleep(0.3)
                    print("1.teuluju 2.kkujo")
                    while True:  # group 2 question
                        command = self.ser.readline()
                        if command == b'Result:14\r\n':
                            if self.targetParts[4][1] != "on":
                                self.targetParts[4][1] = "on"
                                print("TV turned on")
                                self.wait_command()
                                print('waiting')
                                self.ser.close()
                                return self.targetParts[4]  ###############################
                            else:
                                print("Already TV on")
                                self.wait_command()
                                print('waiting')
                                self.ser.close()
                                return self.targetParts[4]  ###############################
                        elif command == b'Result:15\r\n':
                            if self.targetParts[4][1] != "off":
                                self.targetParts[4][1] = "off"
                                print("TV turned off")
                                self.wait_command()
                                print('waiting')
                                self.ser.close()
                                return self.targetParts[4]  ###############################
                            else:
                                print("Already TV off")
                                self.wait_command()
                                print('waiting')
                                self.ser.close()
                                return self.targetParts[4]  ###############################

            except KeyboardInterrupt:
                print('voice command ended.')
                pass
            finally:
                self.wait_command()
                time.sleep(0.3)
                self.ser.close()
    '''

    def Door_selection(self):
        print("1.yeoluju")
        command = self.ser.readline()
        print(command)
        if command == b'Result:13\r\n':
            self.wait_command()
            self.ser.close()
            print('waiting')
            return self.targetParts[0] # 알아들음
        return self.targetParts[5]# 못 알아들음
    def LED_selection(self):
        print("1.kyuzo 2.kkuzo")
        command = self.ser.readline()
        print(command)
        if command == b'Result:11\r\n':
            self.targetParts[1][1] = "on"
            print("LED turned on")
            self.wait_command()
            print('waiting')
            self.ser.close()
            return self.targetParts[1]

        elif command == b'Result:12\r\n':
            self.targetParts[1][1] = "off"
            print("LED turned off")
            self.wait_command()
            print('waiting')
            self.ser.close()
            return self.targetParts[1]
        return self.targetParts[5]# 못 알아들음
    def Window_selection(self):
        return self.targetParts[5]  # 못 알아들음
    def AC_selection(self):
        print("1.teuluju 2.kkujo")
        command = self.ser.readline()
        print(command)
        if command == b'Result:14\r\n':
            self.targetParts[3][1] = "on"
            print("AC turned on")
            self.wait_command()
            print('waiting')
            self.ser.close()
            return self.targetParts[3]

        elif command == b'Result:15\r\n':
            self.targetParts[3][1] = "off"
            print("AC turned off")
            self.wait_command()
            print('waiting')
            self.ser.close()
            return self.targetParts[3]
        return self.targetParts[5]# 못 알아들음
    def TV_selection(self):
        print("1.teuluju 2.kkujo")
        command = self.ser.readline()
        print(command)
        if command == b'Result:14\r\n':
            self.targetParts[4][1] = "on"
            print("AC turned on")
            self.wait_command()
            print('waiting')
            self.ser.close()
            return self.targetParts[3]

        elif command == b'Result:15\r\n':
            self.targetParts[4][1] = "off"
            print("AC turned off")
            self.wait_command()
            print('waiting')
            self.ser.close()
            return self.targetParts[3]
        return self.targetParts[5]  # 못 알아들음

    def import_ch_2(self,partsName):

        self.ser.write(serial.to_bytes([0xAA]))
        self.ser.write(serial.to_bytes([0x22]))

        if partsName == "Door":
            print('waiting')
            time.sleep(0.3)

            print(partsName)
            return self.Door_selection()

        elif partsName == "LED":
            print('waiting')
            time.sleep(0.3)

            print(partsName)
            return self.LED_selection()

        elif partsName == "Window":
            print('waiting')
            time.sleep(0.3)

            print(partsName)
            return self.Window_selection()

        elif partsName == "AC":
            print('waiting')
            time.sleep(0.3)

            print(partsName)
            return self.AC_selection()

        elif partsName == "TV":
            print('waiting')
            time.sleep(0.3)

            print(partsName)
            return self.TV_selection()

    def hear2Atct2(self):
        cnt = 0
        msg = ""

        cnt = 0
        msg = ""
        try:
            print("1.hyunkwanmoon, 2.LED 3.changmoon 4.Aircon 5.TV")
            command = self.ser.readline()
            print(command)
            if command == b'Result:11\r\n':  # Door
                self.wait_command()

                print('waiting')
                time.sleep(0.3)

                self.import_ch_2("Door")
            elif command == b'Result:12\r\n':  # LED
                self.wait_command()

                print('waiting')
                time.sleep(0.3)

                self.import_ch_2("LED")
            elif command == b'Result:13\r\n':  # Window
                self.wait_command()

                print('waiting')
                time.sleep(0.3)

                self.import_ch_2("Window")
            elif command == b'Result:14\r\n':  # AC
                self.wait_command()

                print('waiting')
                time.sleep(0.3)

                self.import_ch_2("AC")
            elif command == b'Result:15\r\n':  # TV
                self.wait_command()

                print('waiting')
                time.sleep(0.3)

                self.import_ch_2("TV")
        except KeyboardInterrupt:
            print('voice command ended.')
            pass
        finally:
            self.wait_command()
            time.sleep(0.3)
            self.ser.close()
