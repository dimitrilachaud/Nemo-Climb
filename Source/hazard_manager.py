import random
from .hazard import Hazard


class HazardManager:
    def __init__(self, screen_height):
        self.screen_height = screen_height
        self.hazards = []

    def spawn_on_platform(self, platform, hazard_type="spikes"):
        width = 20
        safe_width = 56
        edge_gap = 4
        side_space = (platform.rect.width - safe_width) // 2
        if platform.platform_type == "moving" or side_space < width + edge_gap:
            return False
        safe_left = platform.rect.centerx - safe_width // 2
        safe_right = safe_left + safe_width
        if random.choice((True, False)):
            x = platform.rect.left + edge_gap
            if x + width > safe_left - edge_gap:
                x = safe_right + edge_gap
        else:
            x = platform.rect.right - width - edge_gap
            if x < safe_right + edge_gap:
                x = platform.rect.left + edge_gap
        y = platform.rect.top - (16 if hazard_type == "spikes" else 20)
        self.hazards.append(Hazard(x, y, hazard_type))
        return True

    def update(self, dt, camera_offset):
        for hazard in self.hazards:
            hazard.update(dt)
        self.hazards = [hazard for hazard in self.hazards
                        if hazard.rect.top + camera_offset < self.screen_height + 80]

    def check_collision(self, player):
        return player.check_hazard_collision(self.hazards)

    def draw(self, surface, camera):
        for hazard in self.hazards:
            hazard.draw(surface, camera)

    def reset(self):
        self.hazards.clear()
