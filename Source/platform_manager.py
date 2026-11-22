import random
from .platform import Platform


class PlatformManager:
    # These movement values match Player and are used to bound generated jumps.
    PLAYER_SPEED = 300
    PLAYER_JUMP_STRENGTH = 690
    PLAYER_GRAVITY = 1750
    PLAYER_WIDTH = 42
    SAFE_LANDING_WIDTH = 56

    def __init__(self, screen_width, screen_height, difficulty_manager):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.difficulty_manager = difficulty_manager
        self.platforms = []
        self.last_platform_y = 0
        self.last_generated_platform = None
        self.run_start_y = screen_height - 55 - 54
        self.freeze_moving = False
        self.reset()

    def generate_initial_platforms(self):
        start = Platform(self.screen_width // 2 - 65, self.screen_height - 55, 130)
        start.reached = True
        self.platforms = [start]
        self.last_generated_platform = start
        self.last_platform_y = start.rect.y
        while self.last_platform_y > -self.screen_height:
            self.generate_platform()

    def generate_platform(self):
        target_height = max(0, int(self.run_start_y - self.last_platform_y))
        settings = self.difficulty_manager.get_platform_settings(target_height)
        gap = random.randint(settings["min_gap"], settings["max_gap"])
        width = random.randint(settings["min_width"], settings["max_width"])
        previous = self.last_generated_platform

        platform_type = "moving" if random.random() < settings["moving_chance"] else "static"
        move_range = min(28, max(16, width // 4)) if platform_type == "moving" else 0

        # Use the descending crossing of the jump arc to bound horizontal reach.
        discriminant = self.PLAYER_JUMP_STRENGTH ** 2 - 2 * self.PLAYER_GRAVITY * gap
        landing_time = (self.PLAYER_JUMP_STRENGTH + max(0, discriminant) ** 0.5) / self.PLAYER_GRAVITY
        horizontal_reach = self.PLAYER_SPEED * landing_time
        previous_safe_radius = max(0, (min(previous.rect.width, self.SAFE_LANDING_WIDTH)
                                       - self.PLAYER_WIDTH) / 2)
        next_safe_radius = max(0, (min(width, self.SAFE_LANDING_WIDTH)
                                   - self.PLAYER_WIDTH) / 2)
        # Reserve enough flight distance to travel between the clear center strips,
        # including the worst-case movement of both platforms and a safety margin.
        center_reach = max(0, horizontal_reach - 16 + previous_safe_radius
                           + next_safe_radius - previous.move_range - move_range)

        previous_center = previous.start_x + previous.rect.width / 2
        min_center = max(width // 2, round(previous_center - center_reach))
        max_center = min(self.screen_width - width // 2,
                         round(previous_center + center_reach))
        center_x = random.randint(min_center, max_center)
        x = center_x - width // 2

        self.last_platform_y -= gap
        platform = Platform(x, self.last_platform_y, width,
                            platform_type=platform_type,
                            move_speed=settings["move_speed"],
                            move_range=move_range)
        platform.set_frozen(self.freeze_moving)
        self.platforms.append(platform)
        self.last_generated_platform = platform

    def update(self, dt, player_y, camera_offset):
        while self.last_platform_y > player_y - self.screen_height * 1.4:
            self.generate_platform()
        for platform in self.platforms:
            platform.set_frozen(self.freeze_moving)
            platform.update(dt)
        self.remove_offscreen_platforms(camera_offset)

    def remove_offscreen_platforms(self, camera_offset):
        self.platforms = [platform for platform in self.platforms
                          if platform is self.last_generated_platform or
                          not platform.is_off_screen(camera_offset, self.screen_height)]

    def draw(self, surface, camera):
        for platform in self.platforms:
            platform.draw(surface, camera)

    def reset(self):
        self.freeze_moving = False
        self.generate_initial_platforms()
