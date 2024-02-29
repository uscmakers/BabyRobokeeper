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
            self.cap = cv2.VideoCapture(1, apiPreference=cv2.CAP_ANY, params=[cv2.CAP_PROP_FRAME_WIDTH, screen_width, cv2.CAP_PROP_FRAME_HEIGHT, screen_height])


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
        sorted_centers = points[points[:,2].argsort()]

        return sorted_centers
    
    def find_color(self, cal):
        ret, im = self.cap.read()

        # Get coordinates of middle of table
        middle = [-self.table_height/2, 0]
        pixel = cal.perform_inverse_transformation(middle)
        pixel = [int(pix) for pix in pixel]
        print(pixel)   # This value is correct (coordinate of the middle of table is correct)

        # Get color of that pixel
        ret, im = self.cap.read()
        print(im[pixel[0],pixel[1]])  # This value is not correct (color of middle of table is incorrect)
        plt.imshow(im)
        plt.show()
        b, g, r = im[pixel[0],pixel[1]]
        return [b, g, r]
    