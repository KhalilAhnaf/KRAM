from pygame.locals import *
import pygame, sys, math
import random
from random import randint
import time
import json
import datetime
from datetime import timedelta


# Constants
WIDTH, HEIGHT = 1000, 800  # Adjusted window size
FPS = 60
data = {}
data['fittslaw'] = [] 
pygame.init()
scr = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fitts' Law Experiment")
pygame.mouse.set_cursor(*pygame.cursors.broken_x)
succ_score = 0
unsucc_score = 0
xpos = 200
ypos = 200
# Change radius to change the width of the ball
# radius = 10

oldx = 0
oldy = 0
#COLORS
BLACK = (0, 0, 0)
NEON_GREEN = (57, 255, 20)
NEON_BLUE = (20, 57, 255)
NEON_PURPLE = (128, 0, 128)

# Task parameters
target_sizes = [10, 20, 40, 60]
target_distances = [(100, 200), (200, 400), (300, 600), (400, 800)]  # Adjusted positions based on your 'left' and 'right'
positions = ['left', 'right']

# Set initial position
pos = 0
pygame.mouse.set_pos(WIDTH/2, HEIGHT/2)

def calcDist(x1, y1, x2, y2):
    dist = math.hypot(x2 - x1, y2 - y1)
    return dist

def printstmt(succ, unsucc):
    print('Successful clicks:' + str(succ) + ' vs Unsuccessful clicks:' + str(unsucc))

while True:
    pygame.display.update(); scr.fill(BLACK)
    pygame.draw.circle(scr, NEON_PURPLE, (xpos, ypos), random.choice(target_sizes))
    start_time = datetime.datetime.now()
    x = pygame.mouse.get_pos()[0]
    y = pygame.mouse.get_pos()[1]

    sqx = (x - xpos)**2
    sqy = (y - ypos)**2
    for event in pygame.event.get():
        if event.type == QUIT:
            with open('data.json', 'w') as outfile:
                json.dump(data, outfile)
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            dist1 = math.sqrt(sqx + sqy)
            if dist1 < radius:
                difftime = datetime.datetime.now() - start_time
                print(str(difftime.microseconds))
                succ_score += 1
                dist = calcDist(oldx, oldy, xpos, ypos)

                # appending to data
                data['fittslaw'].append({
                    'time': difftime.microseconds,
                    'distance': dist,
                    'width': 2 * radius
                })
                print(data)
                print("distance by click:" + str(dist1))
                pygame.mouse.set_pos(350, 350)
                oldx = xpos
                oldy = ypos 
                xpos, ypos = target_distances[pos]  # Updated to use the adjusted positions
                print("target size:" + str(radius))
                print("target distances:" + str(target_distances[pos]))
                printstmt(succ_score, unsucc_score)
                pos = (pos + 1) % 4
                if pos == 4:
                    sys.exit()
            else:
                unsucc_score += 1
                printstmt(succ_score, unsucc_score)