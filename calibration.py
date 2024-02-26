import numpy as np

class Calibration():
    def __init__(self, tr, tl, br, bl, table_width, table_height):
        self.points = [tr, tl, br, bl]
        self.table_width = table_width
        self.table_height = table_height

        A = []
        p1 = self.points
        p2 = [[0,self.table_width/2], [-self.table_height,self.table_width/2], [0,-self.table_width/2], [-self.table_height,-self.table_width/2]]
        for i in range(4):
            x, y = p1[i][0], p1[i][1]
            u, v = p2[i][0], p2[i][1]
            A.append([x, y, 1, 0, 0, 0, -u * x, -u * y, -u])
            A.append([0, 0, 0, x, y, 1, -v * x, -v * y, -v])
        A = np.asarray(A)
        U, S, Vh = np.linalg.svd(A)
        L = Vh[-1, :] / Vh[-1, -1]
        H = L.reshape(3, 3)
        self.H = H

    def get_transformation_matrix(self):
        return self.H
    
    def get_inverse_transformation_matrix(self):
        return np.linalg.inv(self.H)
    
    def perform_transformation(self, p1):
        return np.matmul(self.H, np.array([p1[0], p1[1], 1]))[:2]
    
    def perform_inverse_transformation(self, d1):
        return np.matmul(np.linalg.inv(self.H), np.array([0, d1, 1]))[:2]
