import serial

class ArduinoCommunication():
    def __init__(self):
        pass

    def send_msg(msg):
        ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
        ser.reset_input_buffer()

        msg = msg + '\n'
        ser.write(msg.encode('utf-8'))