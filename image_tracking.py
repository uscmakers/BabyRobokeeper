import cv2
from matplotlib import pyplot as plt
import time

# Dimensions of my iPhone currently
SCREEN_WIDTH = 1920
SCREEN_HEIGHT =  1080

# Approximate radius of ball in relation to the above dimensions
# Maybe calculate using formula later
BALL_RADIUS = 60

# for the func is_single_color(r, g, b), so that you only have to change it here
DISTINCTIVE_RED = True
DISTINCTIVE_GREEN = True
DISTINCTIVE_BLUE = False

# for the func is_color_rgb(r, g, b), the target color and the amount of wiggle room the color match will have
COLOR_LEEWAY = 50
BALL_R = 100
BALL_G = 0
BALL_B = 100

# If we are looking for the only thing that would have blue in it, for example
def is_single_color(r, g, b):
    if DISTINCTIVE_RED:
        
        if r <= 30 and g <= 30 and b <= 30:
            return True
    elif DISTINCTIVE_GREEN:
        if g <= 128:
            return True
    elif DISTINCTIVE_BLUE:
        if b >= 40:
            return True
    return False
        
# If we are looking for a color that is similar to something on the board, like purple on a red board
def is_color_rgb(r, g, b):
    if abs(BALL_R - r) <= COLOR_LEEWAY and abs(BALL_G - g) <= COLOR_LEEWAY and abs(BALL_B - b) <= COLOR_LEEWAY:
        return True
    return False

# row goes to 1080
# col dgoes to 1920
# INCOMPLETE. NEED TO CHECK IF MISFIRE COLOR MATCH AND IF SAME POINT IS REACHED ACCIDENTLY
def find_and_map_ball(row, col):
    # visited = [[0 for col in range(BALL_RADIUS * 2)] for row in range(BALL_RADIUS * 2)]
    
    # Ensures that the area we are looking at does not go out of bunds
    top = max(0, row-int(BALL_RADIUS*2.5))
    bottom = min(SCREEN_HEIGHT, row+int(BALL_RADIUS*2.5))
    right = min(SCREEN_WIDTH, col + int(BALL_RADIUS*2.5))
    left = max(0, col - int(BALL_RADIUS*2.5))
    print("Top:" + str(top))
    print("Bottom:" + str(bottom))
    print("Right:" + str(right))
    print("Left:" + str(left))

    p1 = ()
    p2 = ()
    p3 = ()
    # Loop from the left until you garunteed hit a point on the ball

    print("Good Shit is at: ", int(5 * (bottom-top)/5))


    for i in range(left, right):
        for num_div in range(1, 4):
            if is_single_color(im[int(top + (bottom-top)/num_div)][i][0], im[int(top + (bottom-top)/num_div)][i][1], im[int(top + (bottom-top)/num_div)][i][2]):
                p1 = (int(top + (bottom-top)/num_div), i)
                break
    for i in range(top, bottom):
        for num_div in range(1, 4):
            if is_single_color(im[i][int(left + (right-left)/num_div)][0], im[i][int(left + (right-left)/num_div)][1], im[i][int(left + (right-left)/num_div)][2]):
                p2 = (int(top + (bottom-top)/num_div), i)
                break

    for i in range(left, right):
        for num_div in range(3, 0, -1):
            if is_single_color(im[int(top + (bottom-top)/num_div)][i][0], im[int(top + (bottom-top)/num_div)][i][1], im[int(top + (bottom-top)/num_div)][i][2]):
                p3 = (int(top + (bottom-top)/num_div), i)
                break

    #     # Change it up to make sure we hit the ball
        # print("Good Shit is at: ", int(5 * (bottom-top)/5))
    #     if is_single_color(im[int(4 * (bottom-top)/5)][350][0], im[int(3 * (bottom-top)/5)][350][1], im[int(3 * (bottom-top)/5)][350][2]):
    #         print("GOTTEM")
    #         break
    #     if i % 3 == 0:
    #         # Check if the top third is good
    #         if is_single_color(im[int(2 * (bottom-top)/5)][i][0], im[int(2 * (bottom-top)/5)][i][1], im[int(2 * (bottom-top)/5)][i][2]):
    #             print("SUCCESS FOR P1")
    #             # Eventually check if at least 30% to the right of it is the correct color
    #             p1 = (int(2 * (bottom-top)/5), i)
    #             break
    #     elif i % 3 == 1:
    #         # Check if the bottom third is good
    #         if is_single_color(im[int(3 * (bottom-top)/5)][i][0], im[int(3 * (bottom-top)/5)][i][1], im[int(3 * (bottom-top)/5)][i][2]):
    #             print("SUCCESS FOR P1")
    #             # Eventually check if at least 30% to the right of it is the correct color
    #             p1 = (int(3 * (bottom-top)/5), i)
    #             break
    #     else:
    #         # Check if the bottom third is good
    #         if is_single_color(im[int(4 * (bottom-top)/5)][i][0], im[int(4 * (bottom-top)/5)][i][1], im[int(4 * (bottom-top)/5)][i][2]):
    #             print("SUCCESS FOR P1")
    #             # Eventually check if at least 30% to the right of it is the correct color
    #             p1 = (int(4 * (bottom-top)/5), i)
    #             break

    # for i in range(top, bottom):
    #     # Change it up to make sure we hit the ball
    #     if i % 3 == 0:
    #         # Check if the left third is good
    #         if is_single_color(im[i][int(2 * (right-left)/5)][0], im[i][int(2 * (right-left)/5)][1], im[i][int(2 * (right-left)/5)][2]):
    #             print("SUCCESS FOR P2")
    #             # Eventually check if at least 30% to the right of it is the correct color
    #             p2 = (i, int(2 * (right-left)/5))
    #             break
    #     elif i % 3 == 1:
    #         # Check if the left third is good
    #         if is_single_color(im[i][int(3 * (right-left)/5)][0], im[i][int(3 * (right-left)/5)][1], im[i][int(3 * (right-left)/5)][2]):
    #             print("SUCCESS FOR P2")
    #             # Eventually check if at least 30% to the right of it is the correct color
    #             p2 = (i, int(3 * (right-left)/5))
    #             break
    #     else:
    #         # Check if the left third is good
    #         if is_single_color(im[i][int(4 * (right-left)/5)][0], im[i][int(4 * (right-left)/5)][1], im[i][int(4 * (right-left)/5)][2]):
    #             print("SUCCESS FOR P2")
    #             # Eventually check if at least 30% to the right of it is the correct color
    #             p2 = (i, int(4 * (right-left)/5))
    #             break
    
    # for i in range(right, left, -1):
    #     # Change it up to make sure we hit the ball
    #     if i % 3 == 0:
    #         # Check if the top third is good
    #         if is_single_color(im[int(2 * (bottom-top)/5)][i][0], im[int(2 * (bottom-top)/5)][i][1], im[int(2 * (bottom-top)/5)][i][2]):
    #             print("SUCCESS FOR P3")
    #             # Eventually check if at least 30% to the right of it is the correct color
    #             p3 = (int(2 * (bottom-top)/5), i)
    #             break
    #     elif i % 3 == 1:
    #         # Check if the bottom third is good
    #         if is_single_color(im[int(3 * (bottom-top)/5)][i][0], im[int(3 * (bottom-top)/5)][i][1], im[int(3 * (bottom-top)/5)][i][2]):
    #             print("SUCCESS FOR P3")
    #             # Eventually check if at least 30% to the right of it is the correct color
    #             p3 = (int(3 * (bottom-top)/5), i)
    #             break
    #     else:
    #         # Check if the bottom third is good
    #         if is_single_color(im[int(4 * (bottom-top)/5)][i][0], im[int(4 * (bottom-top)/5)][i][1], im[int(4 * (bottom-top)/5)][i][2]):
    #             print("SUCCESS FOR P3")
    #             # Eventually check if at least 30% to the right of it is the correct color
    #             p3 = (int(4 * (bottom-top)/5), i)
    #             break
    
    d1 = pow(p1[0], 2) + pow(p1[1], 2)
    d2 = pow(p2[0], 2) + pow(p2[1], 2)
    d3 = pow(p3[0], 2) + pow(p3[1], 2)


    center_x = (d1 * (p2[1] - p3[1]) + d2 * (p3[1] - p1[1]) + d3 * (p1[1] - p2[1])) / (2 * (p1[0] * (p2[1] - p3[1]) + p2[0] * (p3[1] - p1[1]) + p3[0] * (p1[1] - p2[1])))
    center_y = (d1 * (p2[0] - p3[0]) + d2 * (p3[0] - p1[0]) + d3 * (p1[0] - p2[0])) / (2 * (p1[1] * (p2[0] - p3[0]) + p2[1] * (p3[0] - p1[0]) + p3[1] * (p1[0] - p2[0])))
    return(center_x, center_y)

    # return (-1, -1)



cap = cv2.VideoCapture(0)

# Get a frame from the cap device
# avg = 0
# for i in range(100):
#     start = time.time()
#     ret, frame = cap.read()
#     plt.imshow(frame)
#     # plt.show()
#     # time.sleep(2)
#     end = time.time()
#     print("Time ellapsed: " + str(end - start))
#     if i > 0:
#         avg += end - start



ret, im = cap.read()
print(type(im))


print("---------------")
# im = cv2.imread('ball.png')
# print(type(im))
print("-----------------------")

# print("There")

# print((im[0]))
# print((im[1000]))

# print(len(im))



# plt.imshow(im)
# plt.show()


start = time.time()


print(len(im))
print(len(im[0]))

# print(len(im[0]))
for row in range(0, SCREEN_HEIGHT-1, BALL_RADIUS):
    for col in range(0, SCREEN_WIDTH-1, BALL_RADIUS):
        if is_single_color(im[row][col][0], im[row][col][1], im[row][col][2]) and is_single_color(im[row+1][col+1][0], im[row+1][col+1][1], im[row+1][col+1][2]) and is_single_color(im[row-1][col-1][0], im[row-1][col-1][1], im[row-1][col-1][2]):
            print("Found Color at position: " + str(col) + ", " + str(row))
            print("Colors at position include " + str(im[row][col]) + "\n\n")
            print("Colors at position 176, 221 include " + str(im[176][221]) + "\n\n")

            plt.imshow(im)
            plt.show()      
            center = find_and_map_ball(row, col)
            # bfs(row, col)
            
            print("Center of ball found at pos (" + str(center[0]) + ", " + str(center[1]) + ")")
            break

print("Time ellapsed 2: " + str(time.time() - start))





# start = time.time()

# # Convert image to grayscale
# imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
# # Run Canny algorithm
# edges = cv2.Canny(imgray,100,200)
# # Identify edges
# ret, thresh = cv2.threshold(edges, 127, 255, 0)
# # Find contours
# contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# # Draw contours in green and create result image
# cv2.drawContours(im, contours, -1, (0,255,0), 3)
# cv2.imwrite('result.png',im)

# # Print coordinates for each identified object
# # for cnt in contours:
# #    (x,y),radius = cv2.minEnclosingCircle(cnt)
# #    center = (int(x),int(y))
# #    radius = int(radius)
# #    print('Contour: centre {},{}, radius {}'.format(x,y,radius))


# print("Time ellapsed 2: " + str(time.time() - start))

# print(ret)


