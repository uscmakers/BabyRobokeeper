from path_prediction import PathPrediction
from calibration import Calibration
from curr_ball_tracking import BallTracking
from arduino_communication import ArduinoCommunication

SCREEN_WIDTH =  1920
SCREEN_HEIGHT =  1080

TABLE_WIDTH = 485
TABLE_HEIGHT =  790

# Find all 4 corners
# TO DO - Finding all 4 corners (Brennen)
tr = [0,0]
tl = [0,0]
br = [0,0]
bl = [0,0]

# Perform calibration
cal = Calibration(tr, tl, br, bl, TABLE_WIDTH, TABLE_HEIGHT)
cal.find_transformation_matrix()

# While loop: Get pixel value, track path, send value through serial
img_tracking = BallTracking(SCREEN_WIDTH, SCREEN_HEIGHT)
path_prediction = PathPrediction(TABLE_WIDTH, TABLE_HEIGHT)
rpi_communication = ArduinoCommunication()
prev_x, prev_y = 0,0
smooth_queue = []
while True:
    x, y = img_tracking.get_center()   # TO DO - rename function, bug fixes, return separately (not tuple), color adjustment (Kayal)
    prj = cal.perform_transformation([x,y])
    path_end = path_prediction.find_path_end([prev_x, prev_y], prj)
    smooth_queue.insert(0, path_end)
    if len(smooth_queue) > 5:
        smooth_queue = smooth_queue[:5]
    smooth_queue = path_prediction.exponential_smoothing(smooth_queue)
    # TO DO = get speed to see if it's worth looking at (Brennen)
    prev_x = prj[0]
    prev_y = prj[1]
    rpi_communication.send_msg(str(smooth_queue))
