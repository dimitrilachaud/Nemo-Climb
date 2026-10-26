import random
from .platform import Platform


class PlatformManager:
    # Keep these in sync with Player's movement values so generated jumps remain reachable.
    PLAYER_SPEED = 300
    PLAYER_JUMP_STRENGTH = 690
    PLAYER_GRAVITY = 1750
    PLAYER_WIDTH = 34

    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.platforms = []
        self.last_platform_y = 0
        self.reset()

    def generate_initial_platforms(self):
        self.platforms = [Platform(self.screen_width // 2 - 65, self.screen_height - 55, 130)]
        self.last_platform_y = self.screen_height - 55
        while self.last_platform_y > -self.screen_height:
            self.generate_platform()

    def generate_platform(self):
        gap = random.randint(82, 124)
        width = random.randint(74, 126)
        previous = self.platforms[-1]

        # Time from takeoff until the player descends back to this platform's height.
        discriminant = self.PLAYER_JUMP_STRENGTH ** 2 - 2 * self.PLAYER_GRAVITY * gap
        landing_time = (
            self.PLAYER_JUMP_STRENGTH + discriminant ** 0.5
        ) / self.PLAYER_GRAVITY
        horizontal_reach = self.PLAYER_SPEED * landing_time
        center_reach = (
            horizontal_reach + previous.rect.width / 2 + width / 2 + self.PLAYER_WIDTH / 2
        )

        # Pick a reachable center, clamped to the screen. This limits the gap from
        # the previously generated platform while preserving varied placements.
        previous_center = previous.rect.centerx
        min_center = max(width // 2, round(previous_center - center_reach))
        max_center = min(self.screen_width - width // 2, round(previous_center + center_reach))
        center_x = random.randint(min_center, max_center)
        x = center_x - width // 2
        self.last_platform_y -= gap
        self.platforms.append(Platform(x, self.last_platform_y, width))

    def update(self, player_y, camera_offset):
        while self.last_platform_y > player_y - self.screen_height * 1.4:
            self.generate_platform()
        self.platforms = [p for p in self.platforms if p.rect.top + camera_offset < self.screen_height + 60]

    def draw(self, surface, camera):
        for platform in self.platforms:
            platform.draw(surface, camera)

    def reset(self):
        self.generate_initial_platforms()
