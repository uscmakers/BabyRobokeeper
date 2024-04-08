import numpy as np
import cv2
import cv2.aruco as aruco
import matplotlib.pyplot as plt


class Setup():
    def __init__(self, table_width, table_height, is_video, video_link = ""):
        if is_video:
            self.cap = cv2.VideoCapture(str(video_link))
        else:
            self.cap = cv2.VideoCapture(0)

        ret, im = self.cap.read()

        self.screen_width = np.size(im, 1)
        self.screen_height = np.size(im, 0)
        self.table_width = table_width
        self.table_height = table_height


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

        # Get coordinates of middle of table
        middle = [-self.table_height/2, 0]
        pixel = cal.perform_inverse_transformation(middle)
        pixel = [int(pix) for pix in pixel]
        
        # Get pixels surrounding found middle
        small_img = im[pixel[1]-50:pixel[1]+51, pixel[0]-50:pixel[0]+51]
        xlim = [pixel[1]-50, pixel[1]+50]
        ylim = [pixel[0]-50, pixel[0]+50]
        plt.imshow(small_img)
        plt.show()

        # Blur the image for edge detection
        img_blur = cv2.GaussianBlur(small_img, (3,3), sigmaX=0, sigmaY=0)
        plt.imshow(img_blur, cmap='gray')
        plt.show()

        # Get the edges from blurred image
        edges = cv2.Canny(image=img_blur, threshold1=100, threshold2=200)
        plt.imshow(edges, cmap='gray')
        plt.show()

        # Blur edge image
        edges_blur = cv2.GaussianBlur(edges, (3,3), sigmaX=10, sigmaY=10)
        plt.imshow(edges_blur, cmap='gray')
        plt.show()

        # Apply Hough circles on the blurred image. 
        detected_circles = cv2.HoughCircles(edges_blur,  
                        cv2.HOUGH_GRADIENT, 1, 20, param1 = 50, 
                    param2 = 30, minRadius = 1, maxRadius = 40) 

        # Get the center and radius of the ball
        local_center = 0
        radius = 0
        if detected_circles is None:
            print("Error")
        else:
            detected_circles = np.uint16(np.around(detected_circles))
            for circle in detected_circles[0,:]:
                a, b, r = circle[0], circle[1], circle[2]
                if r > 15 and r < 25:
                    local_center = [a,b]
                    radius = r
        print('Center of circle: ', local_center)
        print('Radius of circle: ', radius)
        cv2.circle(small_img, local_center, radius, (255,0,0), 1)
        plt.imshow(small_img)
        plt.show()

        # Translate local center to center of entire image
        center = [local_center[0]+ylim[0], local_center[1]+ylim[0]]
        print('Center with respect to whole image: ', center)
        plt.imshow(im)
        plt.show()

        # Get color of four points around the ball
        r_vals = []
        g_vals = []
        b_vals = []
        for pt in [center[0]-(radius//2), center[0]+(radius//2)]:
            r_vals.append(im[center[1]][pt][0])
            b_vals.append(im[center[1]][pt][1])
            g_vals.append(im[center[1]][pt][2])
        
        for pt in [center[1]-(radius//2), center[1]+(radius//2)]:
            r_vals.append(im[pt][center[0]][0])
            b_vals.append(im[pt][center[0]][1])
            g_vals.append(im[pt][center[0]][2])

        r = np.average(r_vals)
        b = np.average(b_vals)
        g = np.average(g_vals)
        return [r, g, b], radius
    
    def get_width(self):
        return self.screen_width

    def get_height(self):
        return self.screen_height