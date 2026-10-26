import pygame
from .character import Character


class Player:
    def __init__(self, x, y, character=None):
        self.width, self.height = 34, 44
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.speed = 300
        self.jump_strength = 690
        self.gravity = 1750
        self.character = character or Character()
        self.is_alive = True
        self.is_grounded = True

    def handle_input(self, keys):
        direction = int(keys[pygame.K_RIGHT] or keys[pygame.K_d]) - int(
            keys[pygame.K_LEFT] or keys[pygame.K_a]
        )
        self.velocity.x = direction * self.speed

    def jump(self):
        if self.is_grounded:
            self.velocity.y = -self.jump_strength
            self.is_grounded = False

    def update(self, dt, platforms, screen_width):
        previous_bottom = self.rect.bottom
        self.is_grounded = False
        self.position.x += self.velocity.x * dt
        self.position.y += self.velocity.y * dt
        self.velocity.y += self.gravity * dt
        self.rect.topleft = (round(self.position.x), round(self.position.y))

        # Wrap at screen edges so a missed horizontal edge does not end a run.
        if self.rect.right < 0:
            self.rect.left = screen_width
        elif self.rect.left > screen_width:
            self.rect.right = 0
        self.position.x = self.rect.x

        if self.velocity.y > 0:
            for platform in platforms:
                if (previous_bottom <= platform.rect.top and
                        self.rect.bottom >= platform.rect.top and
                        self.rect.right > platform.rect.left and
                        self.rect.left < platform.rect.right):
                    self.rect.bottom = platform.rect.top
                    self.position.y = self.rect.y
                    self.velocity.y = 0
                    self.is_grounded = True
                    return True
        return False

    def draw(self, surface, camera):
        self.character.draw(surface, camera.apply(self.rect))

    def reset(self, x, y):
        self.position.update(x, y)
        self.rect.topleft = (x, y)
        self.velocity.update(0, 0)
        self.is_alive = True
        self.is_grounded = True
