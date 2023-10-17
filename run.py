from ball_tracking import PathPrediction

x1 = -10
y1=  0
x2 = -9
y2 = 1.5
path = PathPrediction(x1, y1, x2, y2)
print(path.find_path_end())