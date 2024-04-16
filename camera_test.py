import cv2
import time
import matplotlib.pyplot as plt
import numpy as np
import serial

cap = cv2.VideoCapture(0)
ret, im = cap.read()
plt.imshow(im)
plt.show()

ser = serial.Serial("/dev/cu.usbmodem21301", 9600, timeout=1)
ser.reset_input_buffer()

while True:
    im = cap.read()

    msg = 'test message\n'
    ser.write(msg.encode('utf-8'))

    time.sleep(1)