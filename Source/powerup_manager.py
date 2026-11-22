from .powerup import PowerUp


class PowerUpManager:
    DURATION = 5.0
    TYPE_TO_EFFECT = {"heart": "immunity", "boots": "double_jump", "snowflake": "freeze"}

    def __init__(self, screen_height):
        self.screen_height = screen_height
        self.powerups = []
        self.timers = {effect: 0.0 for effect in self.TYPE_TO_EFFECT.values()}
        self.platforms_seen = 0
        self.next_type_index = 0

    def populate_platforms(self, platforms, camera_offset=0):
        for platform in platforms:
            if platform.powerup_checked:
                continue
            platform.powerup_checked = True
            if platform.reached or platform.platform_type == "moving":
                continue
            self.platforms_seen += 1
            # A pickup appears every fourth eligible platform; cycling the types
            # makes all three abilities available during ordinary play.
            if self.platforms_seen % 4 == 0:
                power_type = PowerUp.TYPES[self.next_type_index % len(PowerUp.TYPES)]
                self.next_type_index += 1
                self.powerups.append(PowerUp(platform.rect.centerx - 14,
                                             platform.rect.top - 34, power_type))

    def update(self, dt, camera_offset):
        expired = []
        for effect, remaining in self.timers.items():
            if remaining > 0:
                self.timers[effect] = max(0.0, remaining - dt)
                if self.timers[effect] == 0:
                    expired.append(effect)
        for powerup in self.powerups:
            powerup.update(dt)
        self.powerups = [powerup for powerup in self.powerups
                         if powerup.rect.top + camera_offset < self.screen_height + 80]
        return expired

    def collect(self, player_rect):
        collected = []
        for powerup in self.powerups:
            if powerup.check_collision(player_rect):
                powerup.is_active = False
                effect = self.TYPE_TO_EFFECT[powerup.power_type]
                self.timers[effect] = self.DURATION
                collected.append(effect)
        self.powerups = [powerup for powerup in self.powerups if powerup.is_active]
        return collected

    def is_active(self, effect):
        return self.timers.get(effect, 0.0) > 0

    def active_icons(self):
        effect_to_icon = {effect: icon for icon, effect in self.TYPE_TO_EFFECT.items()}
        return [(effect_to_icon[effect], remaining)
                for effect, remaining in self.timers.items() if remaining > 0]

    def draw(self, surface, camera):
        for powerup in self.powerups:
            powerup.draw(surface, camera)

    def reset(self):
        self.powerups.clear()
        for effect in self.timers:
            self.timers[effect] = 0.0
        self.platforms_seen = 0
        self.next_type_index = 0
