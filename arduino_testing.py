import serial

def send_msg(msg):
    msg = msg + '\n'
    ser.write(msg.encode('utf-8'))
    line = ""
    while (line == ""):
        ser.write(msg.encode('utf-8'))
        line = ser.readline().decode('utf-8').rstrip()
        if (line != ""):
            print(line)

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

ser = serial.Serial(arduino_ports[0], 9600, timeout=1)
ser.reset_input_buffer()

values = [0,0] # Update values to sent here

for v in values:
    send_msg(str(v))