class DifficultyManager:
    """Height zones control platform dimensions, obstacle rates, and scenery."""

    ENDLESS_TIER_HEIGHT = 2000

    ZONES = (
        {"name": "Forest Canopy", "start": 0, "background": "forest",
         "gap": (82, 116), "width": (96, 132), "moving": 0.0, "hazard": 0.04, "enemy": 0.04},
        {"name": "Cloud Layer", "start": 2000, "background": "cloud",
         "gap": (86, 120), "width": (86, 122), "moving": 0.12, "hazard": 0.09, "enemy": 0.08},
        {"name": "Rocky Reach", "start": 4000, "background": "rocky",
         "gap": (90, 124), "width": (76, 112), "moving": 0.20, "hazard": 0.14, "enemy": 0.13},
        {"name": "Night Summit", "start": 6000, "background": "night",
         "gap": (94, 126), "width": (68, 104), "moving": 0.28, "hazard": 0.19, "enemy": 0.18},
    )

    def __init__(self):
        self.current_zone = 0
        self.zone_height = self.ZONES[1]["start"]
        self.difficulty_level = 1
        self.update(0)

    def update(self, height):
        index = 0
        for candidate, zone in enumerate(self.ZONES):
            if height >= zone["start"]:
                index = candidate
        self.current_zone = index
        if index == len(self.ZONES) - 1:
            extra_tiers = max(0, (int(height) - self.ZONES[index]["start"]) // self.ENDLESS_TIER_HEIGHT)
            self.difficulty_level = index + 1 + extra_tiers
            self.zone_height = self.ZONES[index]["start"] + (extra_tiers + 1) * self.ENDLESS_TIER_HEIGHT
        else:
            self.difficulty_level = index + 1
            self.zone_height = self.ZONES[index + 1]["start"]

    def get_zone(self, height=None):
        if height is None:
            return self.ZONES[self.current_zone]
        index = 0
        for candidate, zone in enumerate(self.ZONES):
            if height >= zone["start"]:
                index = candidate
        return self.ZONES[index]

    def _zone_index(self, height=None):
        if height is None:
            return self.current_zone
        index = 0
        for candidate, zone in enumerate(self.ZONES):
            if height >= zone["start"]:
                index = candidate
        return index

    def _endless_tiers(self, height=None):
        if height is None:
            return max(0, self.difficulty_level - len(self.ZONES))
        final_start = self.ZONES[-1]["start"]
        return max(0, (int(height) - final_start) // self.ENDLESS_TIER_HEIGHT)

    def get_platform_settings(self, height=None):
        zone = self.get_zone(height)
        zone_index = self._zone_index(height)
        tiers = self._endless_tiers(height)
        # Keep platforms wide enough for the player hitbox and the protected
        # landing strip while steadily shrinking them as endless tiers rise.
        min_width = max(48, zone["width"][0] - tiers)
        max_width = max(min_width, zone["width"][1] - 3 * tiers)
        return {"min_gap": zone["gap"][0], "max_gap": zone["gap"][1],
                "min_width": min_width, "max_width": max_width,
                "moving_chance": min(0.95, zone["moving"] + 0.04 * tiers),
                "move_speed": min(240, 44 + zone_index * 10 + 12 * tiers)}

    def get_enemy_settings(self, height=None):
        zone = self.get_zone(height)
        tiers = self._endless_tiers(height)
        return {"spawn_chance": min(0.95, zone["enemy"] + 0.04 * tiers),
                "speed": 72 + 12 * self._zone_index(height)}

    def get_hazard_settings(self, height=None):
        zone = self.get_zone(height)
        return {"spawn_chance": zone["hazard"], "types": ("spikes", "energy_orb")}

    def get_background_zone(self, height=None):
        return self.get_zone(height)["background"]

    def get_zone_name(self, height=None):
        name = self.get_zone(height)["name"]
        tiers = self._endless_tiers(height)
        return f"{name} +{tiers}" if tiers else name
