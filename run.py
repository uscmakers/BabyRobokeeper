from path_prediction import PathPrediction
from calibration import Calibration
from img_tracking import BallTracking
from arduino_communication import ArduinoCommunication
from setup import Setup
import time
import copy
import cv2
import numpy as np

DEBUG = False

MANUAL = True

SCREEN_WIDTH =  1920
SCREEN_HEIGHT =  1080

TABLE_WIDTH = 475
TABLE_HEIGHT =  815

USING_VIDEO = True
VIDEO_NAME = "videos/ArucoTest2.mov"

# Find all 4 corners
setup = Setup(TABLE_WIDTH, TABLE_HEIGHT, USING_VIDEO, VIDEO_NAME)
# setup.getArudinoPort()
# print("test")
SCREEN_WIDTH = setup.get_width()
SCREEN_HEIGHT = setup.get_height()

if DEBUG:
    print("Screen Width: ", SCREEN_WIDTH)
    print("Screen Height: ", SCREEN_HEIGHT)

corners = setup.detect_aruco_markers()
if DEBUG:
    print(corners)

# Perform calibration
cal = Calibration(corners[1], corners[0], corners[3], corners[2], TABLE_WIDTH, TABLE_HEIGHT)  # tr, tl, br, bl

# Find color of ball automatically (to be added in Setup)
# Instructions: Place the ball in the middle of the table when code is run
# Output: color
color, ball_radius = setup.find_color(cal)  # This is assuming that we have no-glare paint, so the whole ball is basically the same color
if DEBUG:
    print('Color: ', color)
    print('Radius: ', ball_radius)

color_leeway = (100,70,70)  # Hard-coded based on testing

if MANUAL:
    highest_red = 255
    lowest_red = 160

    highest_green = 150
    lowest_green = 80

    highest_blue = 110
    lowest_blue = 39

    color = (int((highest_red+lowest_red)/2), int((highest_green+lowest_green)/2), int((highest_blue+lowest_blue)/2))
    color_leeway = (highest_red - color[0], highest_green - color[1], highest_blue - color[2])
    print(color)
    print(color_leeway)
    ball_radius = 26

img_tracking = BallTracking(SCREEN_WIDTH, SCREEN_HEIGHT, color, color_leeway, ball_radius, USING_VIDEO, VIDEO_NAME)
path_prediction = PathPrediction(TABLE_WIDTH, TABLE_HEIGHT)

if not DEBUG:
    rpi_communication = ArduinoCommunication()

prev_x, prev_y = 0,0
prev_time = time.time()
path_end = 0
if not DEBUG:
    rpi_communication.send_msg(str(0))

time_since_send = 0
# While loop: Get pixel value, track path, send value through serial
while True:

    if ((time_since_send != 0) and (time.time() - time_since_send > 1.5)):
        if DEBUG:
            print("Resetting to middle")
        time_since_send = 0
        if not DEBUG:
            rpi_communication.send_msg(str(0))

    x, y = img_tracking.get_center()
    
    if x != -1:
        prj = cal.perform_transformation([x,y])

        if path_prediction.check_speed([prev_x, prev_y], prj, time.time()-prev_time):
            prev_path_end = copy.deepcopy(path_end)
            path_end = path_prediction.find_path_end([prev_x, prev_y], prj)


            if path_end == float("-inf"):
                path_end = prev_path_end
            else:
                outlier_result = path_prediction.check_outlier(path_end)
                if (outlier_result == True):
                    if DEBUG:
                        print("OUTLIER: ", str(path_end))
                    # time_since_send = time.time()
                    # if not DEBUG:
                    #     rpi_communication.send_msg(str(outlier_result))
                    #     print("OUTLIER: ", str(path_end))
                    #     print(outlier_result)
                else:
                    if DEBUG:
                        print("PATH END: ", str(path_end))
                    time_since_send = time.time()
                    if not DEBUG:
                        rpi_communication.send_msg(str(path_end))

        prev_x = prj[0]
        prev_y = prj[1]
        
        curr_time = time.time()
        time_passed = curr_time - prev_time
        if 0.1 - time_passed >= 0:
            time.sleep(0.1 - time_passed)
        prev_time = curr_time

