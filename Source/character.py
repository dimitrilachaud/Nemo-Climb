import pygame


class Character:
    """Single starter character; replace the drawn placeholder with art later."""

    def __init__(self, color=(248, 197, 92)):
        self.color = color

    def draw(self, surface, rect):
        pygame.draw.rect(surface, self.color, rect, border_radius=8)
        # Simple face keeps the prototype readable without image assets.
        eye_y = rect.y + max(7, rect.height // 3)
        pygame.draw.circle(surface, (35, 39, 55), (rect.x + rect.width // 3, eye_y), 2)
        pygame.draw.circle(surface, (35, 39, 55), (rect.x + 2 * rect.width // 3, eye_y), 2)
