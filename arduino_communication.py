import serial
import serial.tools.list_ports

class ArduinoCommunication():
    def __init__(self):

        # Attempt to find an Arduino connected via serial
        arduino_ports = [
            p.device
            for p in serial.tools.list_ports.comports()
            if 'IOUSBHostDevice' in p.description
        ]

        if not arduino_ports:
            raise IOError("No Arduino found")
        
        if len(arduino_ports) > 1:
            print("Multiple Arduino devices found. Using: ", arduino_ports[0])
        
        print("ARDUINO PORT: ", arduino_ports[0])

        # Initiate Serial Connection
        self.ser = serial.Serial(arduino_ports[0], 9600, timeout=1)
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