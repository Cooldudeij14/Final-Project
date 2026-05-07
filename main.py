

import pygame
import time

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("c:/Users/Ishaan.Joshi28/.vscode/FInal/song4.mp3")


song_chart = [(1465, 0), (1637, 0), (1818, 0), (1996, 1), (2353, 1), (2534, 1),
    (2905, 2), (3087, 2), (3265, 3), (3450, 3), (3814, 3), (3997, 4),
    (4361, 5), (4541, 4), (4721, 5), (4903, 6), (5268, 5), (5452, 6),
    (5630, 6), (5806, 6), (6534, 1), (6909, 3), (7087, 5), (7276, 4),
    (7450, 3), (7634, 5), (7810, 4), (7997, 3), (8352, 4), (8534, 3),
    (8727, 6), (9090, 5), (9456, 6), (9636, 0), (9823, 0), (10001, 0),
    (10181, 0), (10365, 0), (10545, 0), (10721, 0), (10910, 6), (11087, 1),
    (11270, 0), (11621, 0), (11634, 6), (11999, 5), (12363, 5), (12732, 5),
    (12906, 5), (13092, 4), (13276, 3), (13452, 5), (13636, 4), (13819, 3),
    (14174, 4), (14356, 3), (14543, 6), (14909, 5), (15272, 6), (15624, 1),
    (15808, 1), (15990, 2), (16179, 1), (16368, 0), (16558, 0), (16724, 6),
    (16918, 0), (17098, 0), (17274, 1), (17454, 0), (17814, 6), (18181, 6),
    (18545, 5), (18724, 5), (18903, 4), (19088, 3), (19268, 5), (19452, 4),]

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

    for note in notes:
        note.draw(screen)

    screen.blit(font_small.render(f"SCORE: {score}", True, WHITE), (20, 20))
    screen.blit(font_small.render(f"STREAK: {streak}", True, WHITE), (20, 50))
    screen.blit(font_small.render(f"MULTIPLIER: {multiplier:.1f}x", True, WHITE), (20, 80))
    screen.blit(font_small.render(f"HIGH SCORE: {max(score, high_score)}", True, (255, 215, 0)), (SCREEN_WIDTH - 250, 20))

    if score > high_score:
        high_score = score
    
    if feedback_timer > 0:
        msg_surf = font_msg.render(feedback_msg, True, feedback_color)
        screen.blit(msg_surf, ((SCREEN_WIDTH - msg_surf.get_width()) // 2, SCREEN_HEIGHT // 2))
        feedback_timer -= 1

    if not game_started:
        pygame.draw.rect(screen, WHITE, button_rect, border_radius=10)
        screen.blit(button_text, button_text.get_rect(center=button_rect.center))

            



