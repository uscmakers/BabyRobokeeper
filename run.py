from path_prediction import PathPrediction
from calibration import Calibration
from img_tracking import BallTracking
from arduino_communication import ArduinoCommunication
from setup import Setup
import time
import copy

DEBUG = False

MANUAL = True

SCREEN_WIDTH =  1920
SCREEN_HEIGHT =  1080

TABLE_WIDTH = 475
TABLE_HEIGHT =  815

USING_VIDEO = False
VIDEO_NAME = "videos/T8.mov"

# Find all 4 corners
setup = Setup(SCREEN_WIDTH, SCREEN_HEIGHT, TABLE_WIDTH, TABLE_HEIGHT, USING_VIDEO, VIDEO_NAME)
corners = setup.detect_aruco_markers()
if DEBUG:
    print(corners)

# Perform calibration
cal = Calibration(corners[1], corners[0], corners[3], corners[2], TABLE_WIDTH, TABLE_HEIGHT)  # tr, tl, br, bl



# Find color of ball automatically (to be added in Setup)
# Instructions: Place the ball in the middle of the table when code is run
# Output: color
color = setup.find_color(cal)  # This is assuming that we have no-glare paint, so the whole ball is basically the same color
if DEBUG:
    print(color)
color_leeway = (1,1,1)  # Hard-coded based on testing
ball_radius = 10  # Hard-coded based on testing (fixture leaves it set)

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

img_tracking = BallTracking(SCREEN_WIDTH, SCREEN_HEIGHT, color, color_leeway, ball_radius, False, "video_name")
path_prediction = PathPrediction(TABLE_WIDTH, TABLE_HEIGHT)

if not DEBUG:
    rpi_communication = ArduinoCommunication()

prev_x, prev_y = 0,0
prev_time = time.time()
path_end = 0
if not DEBUG:
    rpi_communication.send_msg(str(0))

# While loop: Get pixel value, track path, send value through serial
while True:

    x, y = img_tracking.get_center()
    
    if x != -1:
        prj = cal.perform_transformation([x,y])

        if path_prediction.check_speed([prev_x, prev_y], prj, time.time()-prev_time):
            prev_path_end = copy.deepcopy(path_end)
            path_end = path_prediction.find_path_end([prev_x, prev_y], prj)
            if path_end == float("-inf"):
                path_end = prev_path_end
            else:
                print("PATH END: ", str(path_end))
                if not DEBUG:
                    rpi_communication.send_msg(str(path_end))

        prev_x = prj[0]
        prev_y = prj[1]
        
        curr_time = time.time()
        time_passed = curr_time - prev_time
        if 0.1 - time_passed >= 0:
            time.sleep(0.1 - time_passed)
        prev_time = curr_time
