from pygame.locals import *
import pygame, sys, math
import random
from random import randint
import time
import json
import datetime
from datetime import timedelta


# Constants
WIDTH, HEIGHT = 800, 800  # Adjusted window size
FPS = 60
data = {}
data['fittslaw'] = [] 
pygame.init()
scr = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fitts' Law Experiment")
pygame.mouse.set_cursor(*pygame.cursors.broken_x)
succ_score = 0
unsucc_score = 0
xpos = WIDTH/2
ypos = HEIGHT/2

oldx = 0
oldy = 0
#COLORS
BLACK = (0, 0, 0)
NEON_GREEN = (57, 255, 20)
NEON_BLUE = (20, 57, 255)
NEON_PURPLE = (128, 0, 128)

# Task parameters
circle_clicked = False
target_sizes = [10, 20, 40, 60]
target_distances = [(0, HEIGHT/2), (100, HEIGHT/2), (200, HEIGHT/2), (300, HEIGHT/2),(500, HEIGHT/2), (600, HEIGHT/2), (700, HEIGHT/2), (800, HEIGHT/2)]
positions = ['left', 'right'] #Un-used

# Set initial position
pos = 0
pygame.mouse.set_pos(WIDTH/2, HEIGHT/2)

def calcDist(x1, y1, x2, y2):
    dist = math.hypot(x2 - x1, y2 - y1)
    return dist

def printstmt(succ, unsucc):
    print('Successful clicks:' + str(succ) + ' vs Unsuccessful clicks:' + str(unsucc))

radius = 50
position = WIDTH/2, HEIGHT/2

def nextRad():
    radius = random.choice(target_sizes)
    return radius

def nextPos():
    position = random.choice(target_distances)
    return position

clock = pygame.time.Clock()

while True:
    scr.fill(BLACK)  # Clear the screen once per frame
    pygame.draw.circle(scr, NEON_PURPLE, position, radius)
    start_time = datetime.datetime.now()

    for event in pygame.event.get():
        if event.type == QUIT:
            with open('data.json', 'w') as outfile:
                json.dump(data, outfile)
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not circle_clicked:
            x, y = pygame.mouse.get_pos()

            dist1 = math.sqrt((x - position[0])**2 + (y - position[1])**2)
            if dist1 < radius:
                difftime = datetime.datetime.now() - start_time
                print(str(difftime.microseconds))
                succ_score += 1
                circle_clicked = True
                dist = calcDist(oldx, oldy, xpos, ypos)

                # appending to data
                data['fittslaw'].append({
                    'time': difftime.microseconds,
                    'distance': dist,
                    'width': 2 * radius
                })
                print(data)
                print("distance by click:" + str(dist1))
                oldx = xpos
                oldy = ypos
                xpos, ypos = nextPos()
                position = xpos, ypos
                radius = nextRad()
                print("target size:" + str(radius))
                print("target distances:" + str(target_distances[pos]))
                printstmt(succ_score, unsucc_score)
                pos = (pos + 1) % 4
                if pos == 4:
                    sys.exit()
            else:
                unsucc_score += 1
                printstmt(succ_score, unsucc_score)

        elif event.type == pygame.MOUSEBUTTONUP:
            circle_clicked = False

    pygame.display.flip()  # Update the entire display
    clock.tick(FPS)  # Cap the frame rate to the specified FPS