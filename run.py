from path_prediction import PathPrediction
from calibration import Calibration
from img_tracking import BallTracking
from arduino_communication import ArduinoCommunication
from setup import Setup
import time

SCREEN_WIDTH =  1920
SCREEN_HEIGHT =  1080

TABLE_WIDTH = 475
TABLE_HEIGHT =  815

# Find all 4 corners
setup = Setup()
corners = setup.detect_aruco_markers()
print("CORNERS", corners)

# Perform calibration
cal = Calibration(corners[1], corners[0], corners[2], corners[3], TABLE_WIDTH, TABLE_HEIGHT)  # tr, tl, br, bl
print("CORNERS", corners[1], corners[0], corners[2], corners[3])
cal = Calibration([1583,138], [265,130], [1582,945], [270,945], TABLE_WIDTH, TABLE_HEIGHT)
cal.find_transformation_matrix()

# While loop: Get pixel value, track path, send value through serial
img_tracking = BallTracking(SCREEN_WIDTH, SCREEN_HEIGHT)
path_prediction = PathPrediction(TABLE_WIDTH, TABLE_HEIGHT)
rpi_communication = ArduinoCommunication()
prev_x, prev_y = 0,0
smooth_queue = []
prev_time = time.time()
path_end = 0
print('Starting tracking...')
while True:
    x, y = img_tracking.get_center()
    prj = cal.perform_transformation([x,y])
    print('Coordinates: ', prj[0], prj[1])
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

        print('SENT: ', path_end)
        rpi_communication.send_msg(str(path_end))
    prev_x = prj[0]
    prev_y = prj[1]
    curr_time = time.time()
    time_passed = curr_time - prev_time
    if 0.35 - time_passed >= 0:
        time.sleep(0.35 - time_passed)
    prev_time = curr_time
    print('\n\n')
