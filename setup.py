import numpy as np
import cv2
import matplotlib.pyplot as plt

class Setup():
    def __init__(self):
        pass

    def is_red(self, r, g, b): 
        if r > 40 and r < 110 and g > 145 and g < 240 and b > 200:
            return True
        else:
             return False

    def find_corners(self):
        print('here')
        cap = cv2.VideoCapture(1, apiPreference=cv2.CAP_ANY, params=[cv2.CAP_PROP_FRAME_WIDTH, 1920, cv2.CAP_PROP_FRAME_HEIGHT, 1080])
        ret, im = cap.read()
        imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

        circles = cv2.HoughCircles(imgray, cv2.HOUGH_GRADIENT, 1, 50, param1=80, param2=20, minRadius=9, maxRadius=40)
        
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
                    print('Center: {}, {}, {}'.format(i[0], i[1], im[y][x]))
                    
                    if (self.is_red(im[y][x][0], im[y][x][1], im[y][x][2])):
                        points[index] = [x,y]
                        # cv2.circle(im, center, radius, (0, 255, 0), 3)
                        index += 1

            sorted1 = points[points[:,0].argsort()]
            left = sorted1[:2]
            right = sorted1[2:]
            sorted_left = left[left[:,1].argsort()]
            sorted_right = right[right[:,1].argsort()]
            output = np.concatenate((sorted_left, sorted_right))

            cv2.imwrite('sample_img.png', im)
            plt.imshow(im)
            plt.show()

            return output