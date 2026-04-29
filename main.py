import pygame
import time

pygame.init()

song_chart = []

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
FPS = 60
NOTE_SPEED = 5
LANE_WIDTH = 70
SPEED_MULTIPLIER = 1.0
NOTE_SIZE = 30
LANE_X = (SCREEN_WIDTH - (7 * LANE_WIDTH)) // 2
HIT_Y = 550
HIT_WINDOW = 50

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (147, 0, 211)
NOTE_COLORS = [(0, 255, 255), (255, 128, 0), (255, 50, 50), (50, 255, 50), (50, 100, 255), (255, 255, 50), (255, 50, 255)]

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Rhythm Game")
clock = pygame.time.Clock()



