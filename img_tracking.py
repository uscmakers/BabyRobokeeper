import cv2
from matplotlib import pyplot as plt
import time
from collections import deque

class BallTracking():

    def __init__(self, screen_width, screen_height, color, color_leeway, radius, is_video, video_link = ""):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.cap = None

        self.ball_r = color[0]
        self.ball_g = color[1]
        self.ball_b = color[2]

        self.red_leeway = color_leeway[0]
        self.green_leeway = color_leeway[1]
        self.blue_leeway = color_leeway[2]

        self.ball_radius = radius

        if is_video:
            self.cap = cv2.VideoCapture(str(video_link))

        else:
            self.cap = cv2.VideoCapture(0)

    # If we ara looking for the only thing that would have blue in it, for example
    def is_single_color(self, r, g, b):
        if abs(self.ball_r - r) <= self.red_leeway and abs(self.ball_g - g) <= self.green_leeway and abs(self.ball_b - b) <= self.blue_leeway:
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

        if total_pixels > 3*self.ball_radius and max_right[1]-max_left[1] >= self.ball_radius*2/3 and max_down[0]-max_up[0] >= self.ball_radius*2/3:
            center = (max_left[1] + self.ball_radius, max_up[0] + self.ball_radius)
            return True, center
        return False, (-1, -1)

    def get_center(self):        
        # Read in a frame
        ret, im = self.cap.read()
        for row in range(0, self.screen_height, int(self.ball_radius/2)):
            for col in range(0, self.screen_width, int(self.ball_radius/2)):
                if self.is_single_color(im[row][col][0], im[row][col][1], im[row][col][2]): 
                    top = max(0, row-self.ball_radius*4)
                    bottom = min(self.screen_height, row+self.ball_radius*4)
                    right = min(self.screen_width, col + self.ball_radius*4)
                    left = max(0, col - self.ball_radius*4)
                    bfs_true, center = self.bfs(im, row, col)
                    if bfs_true:
                        # print("Center (" + str(center[0]) + ", " + str(center[1]) + ")")
                        # Uncomment to see image
                        # plt.imshow(im)
                        # plt.show()

                        return center[0], center[1]
        # Uncomment to see image
        # plt.imshow(im)
        # plt.show()
        return -1, -1




highest_red = 255
lowest_red = 160

highest_green = 150
lowest_green = 80

highest_blue = 110
lowest_blue = 39

color = (int((highest_red+lowest_red)/2), int((highest_green+lowest_green)/2), int((highest_blue+lowest_blue)/2))
color_leeway = (highest_red - color[0], highest_green - color[1], highest_blue - color[2])
print(color)
print(color_leeway)
resolution = (1920, 1080)
ball_radius = 26

# img_tracking = BallTracking(resolution[0], resolution[1], color, color_leeway, ball_radius, False, "video_name")
# while True:
#     img_tracking.get_center()