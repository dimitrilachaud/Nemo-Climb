import pygame


class Enemy:
    """A flying enemy that moves horizontally at a fixed speed."""

    def __init__(self, x, y, enemy_type="flyer", speed=72, screen_width=540, direction=1):
        self.width, self.height = 34, 28
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.enemy_type = enemy_type
        self.speed = abs(speed)
        self.screen_width = screen_width
        self.direction = 1 if direction >= 0 else -1
        self.velocity = pygame.Vector2(self.direction * self.speed, 0)
        self.is_active = True

    def update(self, dt):
        if not self.is_active:
            return
        self.rect.x += round(self.velocity.x * dt)
        if self.velocity.x > 0 and self.rect.left >= self.screen_width:
            self.rect.right = 0
        elif self.velocity.x < 0 and self.rect.right <= 0:
            self.rect.left = self.screen_width

    def draw(self, surface, camera):
        if not self.is_active:
            return
        rect = camera.apply(self.rect)
        wing_y = rect.centery + (2 if self.direction > 0 else -2)
        pygame.draw.polygon(surface, (146, 99, 185),
                            [(rect.left + 5, wing_y), (rect.centerx, rect.top - 7),
                             (rect.centerx + 2, rect.bottom - 2)])
        pygame.draw.polygon(surface, (146, 99, 185),
                            [(rect.right - 5, wing_y), (rect.centerx, rect.top - 7),
                             (rect.centerx - 2, rect.bottom - 2)])
        pygame.draw.ellipse(surface, (210, 119, 205), rect)
        pygame.draw.circle(surface, (255, 245, 215), (rect.centerx + 5, rect.centery - 2), 3)
        pygame.draw.circle(surface, (40, 31, 60), (rect.centerx + 6, rect.centery - 2), 1)

    def check_collision(self, player_rect):
        return self.is_active and self.rect.colliderect(player_rect)

    def reset(self):
        self.is_active = True
