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
# setup = Setup()
# corners = setup.find_corners()


# Perform calibration
# cal = Calibration(corners[1], corners[0], corners[2], corners[3], TABLE_WIDTH, TABLE_HEIGHT)  # tr, tl, br, bl
cal = Calibration([1656,132], [255,143], [1602,920], [313,920], TABLE_WIDTH, TABLE_HEIGHT)
cal.find_transformation_matrix()

# While loop: Get pixel value, track path, send value through serial
img_tracking = BallTracking(SCREEN_WIDTH, SCREEN_HEIGHT)
path_prediction = PathPrediction(TABLE_WIDTH, TABLE_HEIGHT)
# rpi_communication = ArduinoCommunication()
prev_x, prev_y = 0,0
smooth_queue = []
prev_time = time.time()
path_end = 0
while True:
    x, y = img_tracking.get_center()
    prj = cal.perform_transformation([x,y])
    print(prj[0], prj[1])
    if path_prediction.check_speed([prev_x, prev_y], prj, time.time()-prev_time):
        prev_path_end = path_end
        path_end = path_prediction.find_path_end([prev_x, prev_y], prj)
        if path_end == None:
            path_end = prev_path_end
        
        # smooth_queue.insert(0, path_end)
        # if len(smooth_queue) > 5:
        #     smooth_queue = smooth_queue[:5]
        # smooth_queue = path_prediction.exponential_smoothing(smooth_queue)
        # path_end = smooth_queue[0]

        print(path_end)
    prev_x = prj[0]
    prev_y = prj[1]
    rpi_communication.send_msg(str(path_end))
    print('\n\n')
    curr_time = time.time()
    time_passed = curr_time - prev_time
    time.sleep(0.5 - time_passed)
    prev_time = curr_time
