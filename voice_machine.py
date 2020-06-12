import time,serial
class voice_machine:
    def __init__(self,targetParts):
        port="/dev/ttyAMA0"
        rate = 9600
        self.ser=serial.Serial(port,rate)
        self.ser.parity = serial.PARITY_NONE
        self.ser.bytesize=serial.EIGHTBITS
        self.Modes=["hear2Act","userSetting"]
        #self.targetParts=[["door","closed"], ["light","off"], ["curtain","closed"], ["AC","off"], ["TV","off"]]
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
            while True:
                command=self.ser.readline()
                print(command)
                print("1.Munyeolujo, 2.bullkyu 3.kurtain kuddu 4.Aircon teulu 5.TV teulu")
                if command==b'Result:11\r\n':
                    if self.targetParts[0][1]=="closed":
                        self.targetParts[0][1]="opened"
                        print(self.targetParts[0][1])
                        msg='door opened'
                    else:
                        msg='door is already opened'
                    print(msg)
                    cnt=1
                    return self.targetParts[0]
                elif command==b'Result:12\r\n':
                    if self.targetParts[1][1]=="off":
                        self.targetParts[1][1]="on"
                        msg='light on'
                    else:
                        msg='light is already turned on'
                    print(msg)
                    cnt=1
                    return self.targetParts[1]
                elif command==b'Result:13\r\n':
                    if self.targetParts[2][1]=="closed":
                        self.targetParts[2][1]="opened"
                        msg='curtain opened'
                    else:
                        msg='curtain is already opened'
                    print(msg)
                    cnt=1
                    return self.targetParts[2]
                elif command==b'Result:14\r\n':
                    if self.targetParts[3][1]=="off":
                        self.targetParts[3][1]="on"
                        msg='AC on'
                    else:
                        msg='AC is already turned on'
                    print(msg)
                    cnt=1
                    return self.targetParts[3]
                elif command==b'Result:15\r\n':
                    if self.targetParts[4][1]=="off":
                        self.targetParts[4][1]="on"
                        msg='TV on'
                    else:
                        msg='TV is already turned on'
                    print(msg)
                    cnt=1
                    return self.targetParts[4]
                time.sleep(1)
                if cnt==1:
                    break;
        except KeyboardInterrupt:
            print('voice command ended.')
            pass
        finally:
            self.ser.close()