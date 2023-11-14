## Predict where the ball will be at by the time it arrives to the goal

class PathPrediction():
    def __init__(self, l, w, x1, y1, x2, y2):
        #constants
        self.l = 50
        self.w = 10

        #inputs
        self.x1 = x1
        self.y1 = y1
        self.m = (y2-y1)/(x2-x1)

    def find_path_end(self):
        while True:
            path_end = self.find_y_intercept()
            if path_end > self.w/2 or path_end < -self.w/2:
                self.calculate_new_path()
            else:
                return path_end

    def find_y_intercept(self):
        return -self.m * self.x1 + self.y1

    def calculate_new_path(self):
        if (self.m > 0):
            self.x1 = (self.w/2 - self.y1 + self.m*self.x1) / self.m
            self.y1 = self.w/2
        else:
            self.x1 = (-self.w/2 - self.y1 + self.m*self.x1) / self.m
            self.y1 = -self.w/2
        self.m = -self.m

