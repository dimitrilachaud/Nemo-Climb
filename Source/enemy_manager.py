import random
from .enemy import Enemy


class EnemyManager:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.enemies = []

    def spawn_on_platform(self, platform, speed=72):
        # The platform provides a height reference only; the enemy does not attach to it.
        x = random.randint(0, self.screen_width - 34)
        y = platform.rect.top - random.randint(70, 140)
        direction = random.choice((-1, 1))
        self.enemies.append(Enemy(x, y, speed=speed, screen_width=self.screen_width,
                                  direction=direction))

    def update(self, dt, camera_offset):
        for enemy in self.enemies:
            enemy.update(dt)
        self.enemies = [enemy for enemy in self.enemies
                        if enemy.rect.top + camera_offset < self.screen_height + 80]

    def check_collision(self, player):
        return any(enemy.check_collision(player.rect) for enemy in self.enemies)

    def draw(self, surface, camera):
        for enemy in self.enemies:
            enemy.draw(surface, camera)

    def reset(self):
        self.enemies.clear()
