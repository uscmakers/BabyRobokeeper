from path_prediction import PathPrediction
from calibration import Calibration
from img_tracking import BallTracking
from arduino_communication import ArduinoCommunication
from setup import Setup
import time
import copy

SCREEN_WIDTH =  1280
SCREEN_HEIGHT =  720

TABLE_WIDTH = 475
TABLE_HEIGHT =  815


# Find all 4 corners
# corners = setup.detect_aruco_markers()

# -------  WHERE TO UPDATE FROM VIDEO ------- #
# The only things to change if we are using a live cam is: 
# Change using_video from True to False, 
# Comment out the redeclaration of SCREEN_WIDTH  and SCREEN_HEIGHT,
using_video = True
video_name = "T1.mov" # Leave as is or blank if not using video, just do not delete/comment out variable name
color = (205, 105, 63)
color_leeway = (50, 30, 37)
resolution = (1280, 720)
ball_radius = 17
# Comment out when running live
SCREEN_WIDTH =  resolution[0]
SCREEN_HEIGHT =  resolution[1]


# print("CORNERS", corners)

# Perform calibration

# Find all 4 corners
setup = Setup(SCREEN_WIDTH, SCREEN_HEIGHT, using_video, video_name)
corners = setup.detect_aruco_markers()

cal = Calibration(corners[1], corners[0], corners[2], corners[3], TABLE_WIDTH, TABLE_HEIGHT)  # tr, tl, br, bl
print("CORNERS", corners[1], corners[0], corners[2], corners[3])
# cal = Calibration([1058,122], [207,90], [1043,644], [183,615], TABLE_WIDTH, TABLE_HEIGHT)
cal.find_transformation_matrix()

# While loop: Get pixel value, track path, send value through serial
img_tracking = BallTracking(1280, 720, color, color_leeway, ball_radius, True, "T1.mov")

path_prediction = PathPrediction(TABLE_WIDTH, TABLE_HEIGHT)
# rpi_communication = ArduinoCommunication()
prev_x, prev_y = 0,0
smooth_queue = []
prev_time = time.time()
path_end = 0
print('Starting tracking...')
# rpi_communication.send_msg(str(-999))
while True:
    time1 = time.time()
    x, y = img_tracking.get_center()
    time1_time = time.time() - time1

    time2 = time.time()
    prj = cal.perform_transformation([x,y])
    time2_time = time.time() - time2

    # print('Coordinates: ', prj[0], prj[1])
    

    if path_prediction.check_speed([prev_x, prev_y], prj, time.time()-prev_time ) and x != -1:
        print(x, y)
        prev_path_end = copy.deepcopy(path_end)
        path_end = path_prediction.find_path_end([prev_x, prev_y], prj)
        if path_end == None:
            path_end = prev_path_end
        
        # smooth_queue.insert(0, path_end)
        # if len(smooth_queue) > 5:
        #     smooth_queue = smooth_queue[:5]
        # smooth_queue = path_prediction.exponential_smoothing(smooth_queue)
        # path_end = smooth_queue[0]

        if path_end >= 0:
            print("SENT: " + str(path_end))
            # rpi_communication.send_msg(str(path_end))

    prev_x = prj[0]
    prev_y = prj[1]
    curr_time = time.time()
    time_passed = curr_time - prev_time
    if 0.30 - time_passed >= 0:
        time.sleep(0.30 - time_passed)
    prev_time = curr_time
