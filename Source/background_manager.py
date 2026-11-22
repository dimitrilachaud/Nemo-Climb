import pygame


class BackgroundManager:
    """Displays zone art and cross-fades between backgrounds."""

    FALLBACK_COLOR = (27, 35, 58)

    def __init__(self, backgrounds=None, screen_size=(540, 720), transition_seconds=1.8):
        self.backgrounds = backgrounds or {}
        self.screen_size = screen_size
        self.transition_seconds = transition_seconds
        self.current_background = "forest" if "forest" in self.backgrounds else None
        self.next_background = None
        self.transition_progress = 1.0
        self._scroll_blends = {}
        self._fallback = pygame.Surface(screen_size)
        self._fallback.fill(self.FALLBACK_COLOR)

    def update(self, dt, zone_name=None):
        if zone_name and zone_name != self.current_background and zone_name != self.next_background:
            self.start_transition(zone_name)
        if self.next_background is not None:
            self.transition_progress = min(1.0, self.transition_progress + dt / self.transition_seconds)
            if self.transition_progress >= 1.0:
                self.current_background = self.next_background
                self.next_background = None

    def start_transition(self, name):
        if name not in self.backgrounds:
            return
        if self.next_background is not None:
            self.current_background = self.next_background
        self.next_background = name
        self.transition_progress = 0.0

    def draw(self, surface):
        current = self.backgrounds.get(self.current_background, self._fallback)
        surface.blit(current, (0, 0))
        if self.next_background is not None:
            incoming = self.backgrounds[self.next_background]
            incoming.set_alpha(round(255 * self.transition_progress))
            surface.blit(incoming, (0, 0))
            incoming.set_alpha(None)

    def draw_vertical_sequence(self, surface, names, progress, blend_height=96):
        """Scroll the viewport down through a top-to-bottom list of zone images."""
        if not names:
            surface.blit(self._fallback, (0, 0))
            return
        height = surface.get_height()
        width = surface.get_width()
        travel = max(0, (len(names) - 1) * height)
        offset = max(0.0, min(1.0, progress)) * travel
        surface.fill(self.FALLBACK_COLOR)
        for index, name in enumerate(names):
            background = self.backgrounds.get(name, self._fallback)
            y = round(index * height - offset)
            surface.blit(background, (0, y))
        band_height = max(2, min(blend_height, height))
        for index in range(len(names) - 1):
            previous_name, next_name = names[index], names[index + 1]
            blend = self._get_scroll_blend(previous_name, next_name, band_height)
            seam_y = round((index + 1) * height - offset - band_height / 2)
            surface.blit(blend, (0, seam_y))

    def _get_scroll_blend(self, previous_name, next_name, band_height):
        key = (previous_name, next_name, band_height)
        if key in self._scroll_blends:
            return self._scroll_blends[key]
        width, height = self.screen_size
        previous = self.backgrounds.get(previous_name, self._fallback)
        following = self.backgrounds.get(next_name, self._fallback)
        blend = pygame.Surface((width, band_height))
        for row in range(band_height):
            previous_row = pygame.Surface((width, 1))
            previous_row.blit(previous, (0, 0), (0, height - band_height + row, width, 1))
            blend.blit(previous_row, (0, row))

            next_row = pygame.Surface((width, 1), pygame.SRCALPHA)
            next_row.blit(following, (0, 0), (0, row, width, 1))
            next_row.set_alpha(round(255 * row / (band_height - 1)))
            blend.blit(next_row, (0, row))
        self._scroll_blends[key] = blend
        return blend

    def reset(self, name="forest"):
        self.current_background = name if name in self.backgrounds else None
        self.next_background = None
        self.transition_progress = 1.0
