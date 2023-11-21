import numpy as np
import cv2

class Setup():
    def __init__():
        pass

    def is_red(r, g, b): 
        if r > 200 and g <= 50 and b <= 50:
            return True

    def find_corners(self):
        cap = cv2.VideoCapture(0)
        ret, im = cap.read()
        imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

        circles = cv2.HoughCircles(imgray, cv2.HOUGH_GRADIENT, 1, 50, param1=100, param2=30, minRadius=0, maxRadius=50)
        points = np.zeros(shape=(4, 2))
        index = 0
        if circles is not None:
            circles = np.uint16(np.around(circles))
            for i in circles[0, :]:
                    x = i[0]
                    y = i[1]
                    center = (i[0], i[1])
                    # circle center
                    #cv2.circle(im, center, 1, (255, 0, 255), 3)
                    # circle outline
                    radius = i[2]
                    #cv2.circle(im, center, radius, (0, 255, 0), 3)
                    print('Center: {}, {}'.format(i[0], i[1]))
                    if (self.is_red(im[y][x][2], im[y][x][1], im[y][x][0])):
                        points[index] = [x,y]
                        cv2.circle(im, center, radius, (0, 255, 0), 3)
                        index += 1

            sorted1 = points[points[:,0].argsort()]
            left = sorted1[:2]
            right = sorted1[2:]
            sorted_left = left[left[:,1].argsort()]
            sorted_right = right[right[:,1].argsort()]
            output = np.concatenate((sorted_left, sorted_right))

            return output