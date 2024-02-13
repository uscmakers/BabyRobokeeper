from path_prediction import PathPrediction
from calibration import Calibration
from img_tracking import BallTracking
from arduino_communication import ArduinoCommunication
from setup import Setup
import time
import copy

DEBUG = True

SCREEN_WIDTH =  1280
SCREEN_HEIGHT =  720

TABLE_WIDTH = 475
TABLE_HEIGHT =  815

USING_VIDEO = True
VIDEO_NAME = "videos/T8.mov"

# Find all 4 corners
setup = Setup(SCREEN_WIDTH, SCREEN_HEIGHT, USING_VIDEO, VIDEO_NAME)
corners = setup.detect_aruco_markers()

# Perform calibration
cal = Calibration(corners[0], corners[1], corners[2], corners[3], TABLE_WIDTH, TABLE_HEIGHT)  # tr, tl, br, bl
if DEBUG:
    print('Corners')
cal.find_transformation_matrix()

# TO DO: Find color of ball automatically (to be added in Setup)
# Instructions: Place the ball in the middle of the table when code is run
# Output: color, ball_radius
color = (1,1,1)
color_leeway = (1,1,1)
ball_radius = 1

# While loop: Get pixel value, track path, send value through serial
img_tracking = BallTracking(SCREEN_WIDTH, SCREEN_HEIGHT, color, color_leeway, ball_radius, True, VIDEO_NAME)

path_prediction = PathPrediction(TABLE_WIDTH, TABLE_HEIGHT)
if not DEBUG:
    rpi_communication = ArduinoCommunication()

prev_x, prev_y = 0,0
prev_time = time.time()
path_end = 0
if not DEBUG:
    rpi_communication.send_msg(str(0))

while True:
    x, y = img_tracking.get_center()
    
    if x != -1:
        prj = cal.perform_transformation([x,y])

        if path_prediction.check_speed([prev_x, prev_y], prj, time.time()-prev_time ):
            prev_path_end = copy.deepcopy(path_end)
            path_end = path_prediction.find_path_end([prev_x, prev_y], prj)
            if path_end == float("-inf"):
                path_end = prev_path_end

            else:
                if not DEBUG:
                    rpi_communication.send_msg(str(path_end))

        prev_x = prj[0]
        prev_y = prj[1]
        
        curr_time = time.time()
        time_passed = curr_time - prev_time
        if 0.1 - time_passed >= 0:
            time.sleep(0.1 - time_passed)
        prev_time = curr_time
