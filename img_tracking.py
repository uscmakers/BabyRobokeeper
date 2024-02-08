import cv2
from matplotlib import pyplot as plt
import time
from collections import deque

# Approximate radius of ball in relation to the above dimensions
# Maybe calculate using formula later
BALL_RADIUS = 18

# for the func is_single_color(r, g, b), so that you only have to change it here
# DISTINCTIVE_RED = False
# DISTINCTIVE_GREEN = True
# DISTINCTIVE_BLUE = False

# for the func is_color_rgb(r, g, b), the target color and the amount of wiggle room the color match will have
# COLOR_LEEWAY = 175


RED_LEEWAY = 40
GREEN_LEEWAY = 20
BLUE_LEEWAY = 20

BALL_R = 175
BALL_G = 80
BALL_B = 40


class BallTracking():

    def __init__(self, screen_width, screen_height, color, color_leeway, radius, is_video, video_link = ""):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.cap = None

        if is_video:
            BALL_R = color[0]
            BALL_G = color[1]
            BALL_B = color[2]

            RED_LEEWAY = color_leeway[0]
            GREEN_LEEWAY = color_leeway[1]
            BLUE_LEEWAY = color_leeway[2]

            BALL_RADIUS = radius

            self.cap = cv2.VideoCapture("videos/" + str(video_link))

        else:
            self.cap = cv2.VideoCapture(0, apiPreference=cv2.CAP_ANY, params=[cv2.CAP_PROP_FRAME_WIDTH, screen_width, cv2.CAP_PROP_FRAME_HEIGHT, screen_height])

    # If we ara looking for the only thing that would have blue in it, for example
    def is_single_color(self, r, g, b):
        if abs(BALL_R - r) <= RED_LEEWAY and abs(BALL_G - g) <= GREEN_LEEWAY and abs(BALL_B - b) <= BLUE_LEEWAY:
            return True
        return False


    def bfs(self, im, start_row, start_col):
        # Define the directions (up, down, left, right)
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        # Get the dimensions of the image
        num_rows, num_cols = len(im), len(im[0])
        # Create a 2D array to keep track of visited pixels
        visited = [[False for _ in range(num_cols)] for _ in range(num_rows)]
        # Create a queue for BFS
        queue = deque([(start_row, start_col)])
        # Perform BFS
        total_pixels = 0
        # We know that it will always be short right and down by .68
        # Keep track of the farthest pixels
        max_left = (-1, 100000)
        max_right = (-1, -1)
        max_up = (100000, -1)
        max_down = (-1, -1)
        while queue:
            row, col = queue.popleft()
            # Mark the current pixel as visited
            visited[row][col] = True
            # Process neighbors
            for dr, dc in directions:
                new_row, new_col = row + dr, col + dc
                # Check if the new pixel is within bounds and is of the desired color
                if 0 <= new_row < num_rows and 0 <= new_col < num_cols and not visited[new_row][new_col] and self.is_single_color(im[new_row][new_col][0], im[new_row][new_col][1], im[new_row][new_col][2]):
                    queue.append((new_row, new_col))
                    # Update the furthest left, right, up, and down
                    if max_left[1] > new_col:
                        max_left = (new_row, new_col)
                    if max_right[1] < new_col:
                        max_right = (new_row, new_col)
                    if max_up[0] > new_row:
                        max_up = (new_row, new_col)
                    if max_down[0] < new_row:
                        max_down = (new_row, new_col)
                    visited[new_row][new_col] = True
                    total_pixels += 1

        if total_pixels > 3*BALL_RADIUS and max_right[1]-max_left[1] >= BALL_RADIUS*2/3 and max_down[0]-max_up[0] >= BALL_RADIUS*2/3:
            center = (max_left[1] + BALL_RADIUS, max_up[0] + BALL_RADIUS)
            return True, center
        return False, (-1, -1)




    def get_center(self):        
        # Read in a frame
        ret, im = self.cap.read()
        # 
        # print(len(im))
        # print(len(im[0]))
        for row in range(0, self.screen_height, int(BALL_RADIUS/2)):
            for col in range(0, self.screen_width, int(BALL_RADIUS/2)):
                if self.is_single_color(im[row][col][0], im[row][col][1], im[row][col][2]): 
                    top = max(0, row-BALL_RADIUS*4)
                    bottom = min(self.screen_height, row+BALL_RADIUS*4)
                    right = min(self.screen_width, col + BALL_RADIUS*4)
                    left = max(0, col - BALL_RADIUS*4)
                    bfs_true, center = self.bfs(im, row, col)
                    if bfs_true:
                        # print("Center (" + str(center[0]) + ", " + str(center[1]) + ")")
                        # Uncomment to see image
                        plt.imshow(im)
                        plt.show()

                        return center[0], center[1]
        # Uncomment to see image
        # plt.imshow(im)
        # plt.show()
        return -1, -1





# img_tracking = BallTracking(1280, 720, (205, 105, 63), (50, 30, 37), 17, True, "T1.mov")
# while True:
#     img_tracking.get_center()