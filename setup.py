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
        image_markers = aruco.drawDetectedMarkers(im.copy(), corners, ids)

        centers = []
        if ids is not None:
            for i in range(len(ids)):
                center_x = int((corners[i][0][0][0] + corners[i][0][2][0]) / 2)
                center_y = int((corners[i][0][0][1] + corners[i][0][2][1]) / 2)
                centers.append((center_x, center_y, ids[i][0]))
                cv2.circle(image_markers, (center_x, center_y), 5, (0, 255, 0), -1)

        # Display the result
        # cv2.imshow('ArUco Markers', image_markers)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        centers = np.array(centers)
        sorted_centers = centers[centers[:,2].argsort()]

        return sorted_centers