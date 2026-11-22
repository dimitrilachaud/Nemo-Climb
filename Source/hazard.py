import math
import pygame


class Hazard:
    """A lethal hazard placed on a platform."""

    def __init__(self, x, y, hazard_type="spikes"):
        self.hazard_type = hazard_type
        self.width, self.height = (20, 16) if hazard_type == "spikes" else (20, 20)
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.is_active = True
        self.phase = 0.0

    def update(self, dt):
        self.phase += dt

    def draw(self, surface, camera):
        if not self.is_active:
            return
        rect = camera.apply(self.rect)
        if self.hazard_type == "spikes":
            points = [(rect.left, rect.bottom), (rect.left + rect.width // 4, rect.top),
                      (rect.centerx, rect.bottom), (rect.right - rect.width // 4, rect.top),
                      (rect.right, rect.bottom)]
            pygame.draw.polygon(surface, (238, 102, 91), points)
            pygame.draw.lines(surface, (255, 190, 128), False, points, 2)
        else:
            pulse = round(2 * math.sin(self.phase * 5))
            pygame.draw.circle(surface, (108, 232, 235), rect.center, rect.width // 2 + pulse)
            pygame.draw.circle(surface, (237, 255, 226), rect.center, max(3, rect.width // 4))

    def check_collision(self, player_rect):
        return self.is_active and self.rect.colliderect(player_rect)

    def reset(self):
        self.is_active = True
        self.phase = 0.0
