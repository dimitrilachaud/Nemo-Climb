import pygame


class BackgroundManager:
    """One-color MVP backdrop, ready to be replaced by a background image."""

    def __init__(self, color=(27, 35, 58)):
        self.color = color

    def update(self, _dt):
        pass

    def draw(self, surface):
        surface.fill(self.color)
        # Quiet decorative stars serve as a starter background treatment.
        for x, y, radius in ((48, 88, 2), (260, 145, 2), (470, 70, 1), (340, 285, 2), (95, 330, 1)):
            pygame.draw.circle(surface, (111, 131, 166), (x, y), radius)

    def reset(self):
        pass
