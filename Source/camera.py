import pygame


class Camera:
    def __init__(self, screen_height):
        self.offset_y = 0.0
        self.scroll_threshold = screen_height * 0.38

    def update(self, player):
        target_offset = self.scroll_threshold - player.rect.y
        if target_offset > self.offset_y:
            self.offset_y = target_offset

    def apply(self, rect):
        moved = rect.copy()
        moved.y += round(self.offset_y)
        return moved

    def get_screen_position(self, position):
        return pygame.Vector2(position.x, position.y + self.offset_y)

    def reset(self):
        self.offset_y = 0.0
