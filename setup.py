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
        cv2.imwrite('videos/test_img4.png', im)
        plt.imshow(im)
        plt.show()

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

        # Split image based on color
        img_blue, img_green, img_red = cv2.split(small_img)
        plt.imshow(img_blue, cmap='gray')
        plt.show()
        plt.imshow(img_red, cmap='gray')
        plt.show()

        # Create mask
        blue_mask = img_blue > 220
        red_mask = img_red < 150
        mask = blue_mask & red_mask
        mask = mask.astype(np.uint8) * 255
        plt.imshow(mask, cmap='gray')
        plt.show()

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if len(contours) > 0:
            # Find the contour with the maximum area (the circle contour)
            max_contour = max(contours, key=cv2.contourArea)
            
            # Fit a circle to the contour
            (x, y), radius = cv2.minEnclosingCircle(max_contour)
            local_center = (int(x), int(y))
            radius = int(radius)
            
            # Draw the circle on the original image
            result_image = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
            cv2.circle(result_image, local_center, radius, (0, 255, 0), 2)
            plt.imshow(result_image)
            plt.show()
        else:
            print("No ball detected.")

        # Translate local center to center of entire image
        center = [local_center[0]+ylim[0], local_center[1]+xlim[0]]
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