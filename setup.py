import numpy as np
import cv2
import cv2.aruco as aruco
from matplotlib import pyplot as plt


class Setup():
    def __init__(self):
        pass

    def detect_aruco_markers(self):
        cap = cv2.VideoCapture(0, apiPreference=cv2.CAP_ANY, params=[cv2.CAP_PROP_FRAME_WIDTH, 1920, cv2.CAP_PROP_FRAME_HEIGHT, 1080])
        ret, im = cap.read()

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

        centers = np.array(centers)
        sorted_centers = centers[centers[:,2].argsort()]

        return sorted_centers