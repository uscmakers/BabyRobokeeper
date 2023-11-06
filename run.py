from path_prediction import PathPrediction
from calibration import Calibration

TABLE_WIDTH = 10
TABLE_HEIGHT =  5

# Calibration
tr_x = 0
tr_y = 5
tl_x = -10
tl_y = 5
br_x = 0
br_y = 0
bl_x = -10
bl_y = 0
cal = Calibration([tr_x,tr_y], [tl_x,tl_y], [br_x,br_y], [bl_x,bl_y], TABLE_WIDTH, TABLE_HEIGHT)
cal.find_transformation_matrix()
prj = cal.perform_transformation([0,2.5])
print(prj)

# # Path prediction
# x1 = -10
# y1=  0
# x2 = -9
# y2 = 1.5
# path = PathPrediction(x1, y1, x2, y2)
# print(path.find_path_end())

