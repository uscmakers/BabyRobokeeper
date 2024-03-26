import numpy as np
import cv2
import cv2.aruco as aruco
import matplotlib.pyplot as plt


class Setup():
    def __init__(self, screen_width, screen_height, table_width, table_height, is_video, video_link = ""):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.table_width = table_width
        self.table_height = table_height
        if is_video:
            self.cap = cv2.VideoCapture(str(video_link))
        else:
            self.cap = cv2.VideoCapture(0)


    def detect_aruco_markers(self):
        ret, im = self.cap.read()
        # plt.imshow(im)
        # plt.show()

        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        dictionary = aruco.getPredefinedDictionary(aruco.DICT_4X4_100)
        parameters =  aruco.DetectorParameters()
        detector = aruco.ArucoDetector(dictionary, parameters)
        corners, ids, rejectedImgPoints = detector.detectMarkers(gray)
        points = []
        if ids is not None:
            for i in range(len(ids)):
                point_x = int(corners[i][0][0][0])
                point_y = int(corners[i][0][0][1])
                points.append((point_x, point_y, ids[i][0]))

        points = np.array(points)
        print("Points: ",  points)
        sorted_centers = points[points[:,2].argsort()]

        return sorted_centers
    
    def find_color(self, cal):
        ret, im = self.cap.read()

        # DEBUGGING
        # print("Data type of pixel values:", im.dtype)
        # print("Min pixel value:", np.min(im))
        # print("Max pixel value:", np.max(im))
        # print("Color space of the image before conversion:", im.shape)

        # Get coordinates of middle of table
        middle = [-self.table_height/2, 0]
        pixel = cal.perform_inverse_transformation(middle)
        pixel = [int(pix) for pix in pixel]
        red_vals = []
        green_vals = []
        blue_vals = []
        for i in range(-1,2):
            for j in range(-1, 2):
                red_vals.append(im[pixel[1]+i][pixel[0]+j][0])
                green_vals.append(im[pixel[1]+i][pixel[0]+j][1])
                blue_vals.append(im[pixel[1]+i][pixel[0]+j][2])

        # Get color of that pixel
        r = np.average(red_vals)
        g = np.average(green_vals)
        b = np.average(blue_vals)

        # DEBUGGING
        # print('R: ', r, 'G: ', g, 'B: ', b)
        # plt.imshow(im)
        # plt.show()

        return [r, g, b]
    