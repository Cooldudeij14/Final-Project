import pygame

class Note:
    def __init__(self, lane, hit_time, lane_width, note_height, colors, lane_start_x, hit_zone_y, note_speed, speed_multiplier, fps, white):
        self.lane = lane
        self.hit_time = hit_time
        self.w = lane_width
        self.h = note_height
        self.x = lane_start_x + (lane * lane_width) + 2.5
        self.y = -self.h
        self.color = colors[lane]
        self.hit_zone_y = hit_zone_y
        self.note_speed = note_speed
        self.speed_multiplier = speed_multiplier
        self.fps = fps
        self.white = white

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.w, self.h), border_radius=6)
        pygame.draw.rect(surface, self.white, (self.x, self.y, self.w, self.h), 2, border_radius=6)

    def update(self, current_song_time):
        time_until_hit = self.hit_time - current_song_time
        self.y = self.hit_zone_y - (time_until_hit * self.note_speed * self.speed_multiplier / 1000 * self.fps)




