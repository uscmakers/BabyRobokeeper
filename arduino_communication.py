import serial

class ArduinoCommunication():
    def __init__(self):
        self.ser = serial.Serial('COM4', 9600, timeout=1)
        self.ser.reset_input_buffer()

    def send_msg(self,msg):
        msg = msg + '\n'
        self.ser.write(msg.encode('utf-8'))
        line = ""
        while (line == ""):
            self.ser.write(msg.encode('utf-8'))
            line = self.ser.readline().decode('utf-8').rstrip()
            if (line != ""):
                print(line)