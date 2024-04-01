import cv2
import numpy as np
import matplotlib.pyplot as plt

img_name = 'videos/test_img.png'

# Read image
img = cv2.imread(img_name, cv2.IMREAD_ANYCOLOR)
plt.imshow(img)
plt.show()

# Blur image
img_blur = cv2.GaussianBlur(img, (3,3), sigmaX=0, sigmaY=0)
plt.imshow(img_blur, cmap='gray')
plt.show()

# Apply Canny filter
edges = cv2.Canny(image=img_blur, threshold1=100, threshold2=200)
plt.imshow(edges, cmap='gray')
plt.show()

# Blur the edge image
edges_blur = cv2.GaussianBlur(edges, (3,3), sigmaX=10, sigmaY=10)
plt.imshow(edges_blur, cmap='gray')
plt.show()

# Apply Hough circles on the blurred image. 
detected_circles = cv2.HoughCircles(edges_blur,  
                   cv2.HOUGH_GRADIENT, 1, 20, param1 = 50, 
               param2 = 30, minRadius = 1, maxRadius = 40) 

center = 0
radius = 0
if detected_circles is None:
    print("Error")
else:
    detected_circles = np.uint16(np.around(detected_circles))
    for circle in detected_circles[0,:]:
        a, b, r = circle[0], circle[1], circle[2]
        if r > 15 and r < 25:
            center = [a,b]
            radius = r

print('Center of circle: ', center)
print('Radius of circle: ', radius)
cv2.circle(img, center, radius, (255,0,0), 1)

plt.imshow(img)
plt.show()
