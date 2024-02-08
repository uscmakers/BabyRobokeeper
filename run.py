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
# Comment out the redeclaration of SCREEN_WIDTH and SCREEN_HEIGHT,
# Comment in the auto-find corners tracking after the setup declaration on line 43
using_video = True
video_name = "T8.mov" # Leave as is or blank if not using video, just do not delete/comment out variable name
color = (205, 105, 63)
color_leeway = (50, 30, 37)
resolution = (1280, 720)
ball_radius = 17
corners = ([1088,77], [222,78], [1077,622], [220,590])
cal_0 = corners[0]
cal_1 = corners[0]
cal_2 = corners[0]
cal_3 = corners[0]

# COMMENT OUT WHEN RUNNING LIVE
SCREEN_WIDTH =  resolution[0]
SCREEN_HEIGHT =  resolution[1]


# Find all 4 corners
setup = Setup(SCREEN_WIDTH, SCREEN_HEIGHT, using_video, video_name)
# COMMENT IN WHEN RUNNING LIVE
# corners = setup.detect_aruco_markers()

# Perform calibration
cal = Calibration(corners[0], corners[1], corners[2], corners[3], TABLE_WIDTH, TABLE_HEIGHT)  # tr, tl, br, bl
print("CORNERS", corners[1], corners[0], corners[2], corners[3])

cal.find_transformation_matrix()

# While loop: Get pixel value, track path, send value through serial
img_tracking = BallTracking(SCREEN_WIDTH, SCREEN_HEIGHT, color, color_leeway, ball_radius, True, video_name)

path_prediction = PathPrediction(TABLE_WIDTH, TABLE_HEIGHT)
# rpi_communication = ArduinoCommunication()
prev_x, prev_y = 0,0
smooth_queue = []
prev_time = time.time()
path_end = 0
print('Starting tracking...')
# rpi_communication.send_msg(str(-999))
first_time = True
while True:
    time1 = time.time()
    x, y = img_tracking.get_center()
    time1_time = time.time() - time1

    time2 = time.time()
    time2_time = time.time() - time2

    # print('Coordinates: ', prj[0], prj[1])
    
    if x != -1:
        prj = cal.perform_transformation([x,y])
        # print("projected x: ", prj[0], "      projected y: ", prj[1])

        if path_prediction.check_speed([prev_x, prev_y], prj, time.time()-prev_time ):
            prev_path_end = copy.deepcopy(path_end)
            path_end = path_prediction.find_path_end([prev_x, prev_y], prj)
            if path_end == float("-inf"):
                path_end = prev_path_end
            
                # smooth_queue.insert(0, path_end)
                # if len(smooth_queue) > 5:
                #     smooth_queue = smooth_queue[:5]
                # smooth_queue = path_prediction.exponential_smoothing(smooth_queue)
                # path_end = smooth_queue[0]
                # print("Path end:", path_end)
            else:
                if first_time:
                    print("Throwing out initial prediction:", path_end)
                    first_time = False
                else:
                    print("SENT: " + str(path_end))
                # rpi_communication.send_msg(str(path_end))


            # else:
            #     print("Path end is -inf")

        prev_x = prj[0]
        prev_y = prj[1]
        curr_time = time.time()
        time_passed = curr_time - prev_time
        if 0.1 - time_passed >= 0:
            time.sleep(0.1 - time_passed)
        prev_time = curr_time
