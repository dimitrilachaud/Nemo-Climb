import pygame


class Platform:
    def __init__(self, x, y, width, height=14, platform_type="static",
                 move_speed=48, move_range=36):
        self.rect = pygame.Rect(x, y, width, height)
        self.platform_type = platform_type
        self.move_speed = move_speed
        self.move_direction = 1
        self.move_range = move_range if platform_type == "moving" else 0
        self.start_x = x
        self.delta_x = 0
        self.reached = False
        self.feature_checked = False
        self.powerup_checked = False
        self.is_frozen = False
        self.ice_amount = 0.0
        self.ice_break_timer = 0.0
        self.ICE_BREAK_DURATION = 0.48

    def set_frozen(self, frozen):
        frozen = bool(frozen and self.platform_type == "moving")
        if frozen == self.is_frozen:
            return
        self.is_frozen = frozen
        if not frozen and self.ice_amount > 0:
            self.ice_break_timer = self.ICE_BREAK_DURATION
        elif frozen:
            self.ice_break_timer = 0.0

    def update(self, dt):
        if self.is_frozen:
            self.ice_amount = min(1.0, self.ice_amount + dt / 0.32)
        elif self.ice_break_timer > 0:
            self.ice_break_timer = max(0.0, self.ice_break_timer - dt)
            self.ice_amount = self.ice_break_timer / self.ICE_BREAK_DURATION
        else:
            self.ice_amount = 0.0
        self.move(dt)

    def move(self, dt):
        old_x = self.rect.x
        if self.platform_type != "moving" or self.is_frozen:
            self.delta_x = 0
            return
        self.rect.x += round(self.move_direction * self.move_speed * dt)
        if self.rect.x < self.start_x - self.move_range:
            self.rect.x = self.start_x - self.move_range
            self.move_direction = 1
        elif self.rect.x > self.start_x + self.move_range:
            self.rect.x = self.start_x + self.move_range
            self.move_direction = -1
        self.delta_x = self.rect.x - old_x

    def is_off_screen(self, camera_offset, screen_height):
        # Platforms above the viewport are still ahead of the climber and will
        # scroll into view later. Only discard platforms that have fallen behind.
        return self.rect.top + camera_offset > screen_height + 80

    def draw(self, surface, camera):
        rect = camera.apply(self.rect)
        if self.platform_type == "moving":
            main, shade, accent = (103, 173, 225), (61, 112, 163), (195, 229, 255)
        else:
            main, shade, accent = (93, 190, 145), (53, 132, 106), (179, 235, 195)
        pygame.draw.rect(surface, main, rect, border_radius=6)
        pygame.draw.rect(surface, shade, (rect.x, rect.y + 7, rect.width, max(1, rect.height - 7)), border_radius=4)
        pygame.draw.line(surface, accent, (rect.x + 8, rect.y + 3), (rect.right - 8, rect.y + 3), 2)
        if self.ice_amount > 0:
            alpha = round(225 * self.ice_amount)
            ice = pygame.Surface((rect.width, rect.height + 15), pygame.SRCALPHA)
            pygame.draw.rect(ice, (178, 232, 255, alpha),
                             (0, 0, rect.width, rect.height), border_radius=6)
            pygame.draw.line(ice, (239, 251, 255, min(255, alpha + 25)),
                             (5, 3), (max(5, rect.width - 5), 3), 2)
            # Short, uneven icicles hang beneath frozen moving platforms.
            icicle_color = (190, 237, 255, alpha)
            highlight_color = (237, 251, 255, min(255, alpha + 20))
            for index, x in enumerate(range(12, rect.width - 5, 22)):
                tip_y = rect.height + 5 + (index % 3) * 3
                pygame.draw.polygon(ice, icicle_color,
                                    [(x - 3, rect.height - 1),
                                     (x + 3, rect.height - 1),
                                     (x, tip_y)])
                pygame.draw.line(ice, highlight_color,
                                 (x - 1, rect.height), (x, tip_y - 2), 1)
            if self.ice_break_timer > 0:
                # Cracks emerge as the ice breaks, then fade with the overlay.
                crack_alpha = round(245 * self.ice_amount)
                crack_color = (63, 139, 181, crack_alpha)
                mid = rect.width // 2
                pygame.draw.lines(ice, crack_color, False,
                                  [(mid, 2), (mid - 4, 6), (mid + 1, 8),
                                   (mid - 2, rect.height - 1)], 2)
                pygame.draw.lines(ice, crack_color, False,
                                  [(mid - 3, 6), (mid - 8, 5), (mid - 11, 2)], 1)
                pygame.draw.lines(ice, crack_color, False,
                                  [(mid, 8), (mid + 6, 6), (mid + 9, 3)], 1)
            surface.blit(ice, (rect.x, rect.y - 1))
