

import pygame
import time

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("c:/Users/Ishaan.Joshi28/.vscode/FInal/song4.mp3")


song_chart = []

# creating a map and set variables
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

LEAD_TIME = ((HIT_Y + NOTE_SIZE) * 1000 / (NOTE_SPEED * FPS))
#colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (147, 0, 211)
NOTE_COLORS = [(0, 255, 255), (255, 128, 0), (255, 50, 50), (50, 255, 50), (50, 100, 255), (255, 255, 50), (255, 50, 255)]

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Rhythm Game")
clock = pygame.time.Clock()

font_large = pygame.font.SysFont("Arial", 40, bold=True)
font_small = pygame.font.SysFont("Arial", 24)
font_msg = pygame.font.SysFont("Arial", 50, bold=True)

#create action with keys

KEYS = [pygame.K_z, pygame.K_x, pygame.K_c, pygame.K_v, pygame.K_b, pygame.K_n, pygame.K_m]
LANE_KEYS = ['Z', 'X', 'C', 'V', 'B', 'N', 'M']
key_labels = [font_large.render(key, True, WHITE) for key in LANE_KEYS]

#point variables

notes = []
score = 0
streak = 0
multiplier = 1
high_score = 0
message = ""
message_timer = 0
message_color = WHITE
game_started = False
button_time = None



#Start button

Start_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, 200, 100)    
button_text = font_large.render("Start", True, (0, 255, 0))

flash = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
flash.fill((255, 255, 255, 40))  # Start fully transparent

#Game start/ start button click

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif not game_started and button_time is None:
            if event.type == pygame.MouseButtonDown:
                if Start_rect.collidepoint(event.pos):
                    button_time = pygame.time.get_ticks()
        elif event.type == pygame.KEYDOWN:

            if event.key in KEYS:
                clicked_lane = KEYS.index(event.key)
                flash[clicked_lane] = 6
                hit_detected = False

                for note in notes[:]:
                    if note.lane == clicked_lane and abs(note.y - HIT_Y) < HIT_WINDOW:
                        notes.remove(note)
                        hit_detected = True
                        score += 25 * multiplier
                        streak += 1
                        if streak % 10 == 0:
                            multiplier += 1
                        message = "Perfect!"
                        message_color = (0, 255, 0)
                        message_timer = pygame.time.get_ticks()
                        break

                if not hit_detected:

                    message = "Miss!"
                    message_color = (255, 0, 0)
                    message_timer = pygame.time.get_ticks()
                    streak = 0
                    multiplier = 1
                    score -= 10

    if game_started:
        current_time = pygame.mixer.music.get_pos()

        while song_chart and current_time >= (song_chart[0][0] - 1200 - LEAD_TIME):
            target_hit_time, lane = song_chart.pop(0)
            notes.append(Note(lane, target_hit_time - 1200, LANE_WIDTH, NOTE_SIZE, NOTE_COLORS, LANE_X, HIT_Y, NOTE_SPEED, SPEED_MULTIPLIER, FPS, WHITE))

        for note in notes[:]:
            note.update(current_time)
            if note.y > SCREEN_HEIGHT:
                notes.remove(note)
                score -= 10
                streak = 0
                feedback_msg = "MISS!"
                feedback_color = (255, 0, 0)
                feedback_timer = 20

    screen.fill(BLACK)

    pygame.draw.rect(screen, PURPLE, (LANE_X, HIT_Y, LANE_WIDTH * 7, 60))

    for i in range(7):
        lx = LANE_X + (i * LANE_WIDTH)
        if flash[i] > 0:
            screen.blit(flash, (lx, 0))
            flash[i] -= 1
        pygame.draw.rect(screen, WHITE, (lx + 5, HIT_Y, LANE_WIDTH - 10, 60), 3)

            



