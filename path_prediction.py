## Predict where the ball will be at by the time it arrives to the goal
import numpy as np

class PathPrediction():
    def __init__(self, table_width, table_height):
        #constants
        self.table_width = table_width
        self.table_height = table_height

    def find_path_end(self, p1, p2):
        x1 = p1[0]
        y1 = p1[1]
        x2 = p2[0]
        y2 = p2[1]
        m = (y2-y1)/(x2-x1)
        loops = 0
        if x2 < x1:
            return float("-inf")
        while True:
            loops += 1
            path_end = self.find_y_intercept(x1, y1, m)
            if loops > 5:
                return float("-inf")
            elif path_end > self.table_height/2 or path_end < -self.table_height/2:
                self.calculate_new_path(x1, y1, m)
            else:
                return path_end

    def find_y_intercept(self, x1, y1, m):
        return -m*x1 + y1

    def calculate_new_path(self, x1, y1, m):
        if (m > 0):
            x1 = (self.table_height/2 - y1 + m*x1) / m
            y1 = self.table_height/2
        else:
            x1 = (-self.table_height/2 - y1 + m*x1) / m
            y1 = -self.table_height/2
        m = -m

    def exponential_smoothing(self, smooth_queue):
        alpha = 0.9
        for i in range(1, len(smooth_queue)):
            smooth_queue[0] = alpha * smooth_queue[0] + (1-alpha)*smooth_queue[i]
        return smooth_queue

    def check_speed(self, prev, curr, time):
        distance = np.sqrt((prev[0]-curr[0])**2 + (prev[1]-curr[1])**2)
        return ((distance/time) > 100)