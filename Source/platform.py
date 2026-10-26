import pygame


class Platform:
    def __init__(self, x, y, width, height=14):
        self.rect = pygame.Rect(x, y, width, height)

    def update(self, _dt):
        pass

    def draw(self, surface, camera):
        rect = camera.apply(self.rect)
        pygame.draw.rect(surface, (93, 190, 145), rect, border_radius=6)
        pygame.draw.rect(surface, (53, 132, 106), (rect.x, rect.y + 7, rect.width, 7), border_radius=4)
