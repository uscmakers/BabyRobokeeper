from path_prediction import PathPrediction
from calibration import Calibration
from img_tracking import BallTracking
# from arduino_communication import ArduinoCommunication
from setup import Setup
import time

SCREEN_WIDTH =  1920
SCREEN_HEIGHT =  1080

TABLE_WIDTH = 475
TABLE_HEIGHT =  815

# Find all 4 corners
# TO DO - Finding all 4 corners (Brennen)
setup = Setup()
corners = setup.find_corners()


# Perform calibration
# cal = Calibration(corners[1], corners[0], corners[2], corners[3], TABLE_WIDTH, TABLE_HEIGHT)  # tr, tl, br, bl
cal = Calibration([1594,160], [290,205], [1580,920], [332,937], TABLE_WIDTH, TABLE_HEIGHT)
cal.find_transformation_matrix()

# While loop: Get pixel value, track path, send value through serial
img_tracking = BallTracking(SCREEN_WIDTH, SCREEN_HEIGHT)
path_prediction = PathPrediction(TABLE_WIDTH, TABLE_HEIGHT)
# rpi_communication = ArduinoCommunication()
prev_x, prev_y = 0,0

prev_time = time.time()

while True:
    x, y = img_tracking.get_center()
    prj = cal.perform_transformation([x,y])
    print(prj[0], prj[1])
    path_end = path_prediction.find_path_end([prev_x, prev_y], prj)
    # TO DO - smoothing (Enrique)
    # TO DO = get speed to see if it's worth looking at (Brennen)
    # path_prediction.check_speed([prev_x, prev_y], prj, time.time()-prev_time)
    prev_x = prj[0]
    prev_y = prj[1]
    # rpi_communication.send_msg(str(path_end))
    # print(path_end)
    prev_time = time.time()
