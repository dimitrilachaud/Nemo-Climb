import pygame


class Character:
    """One selectable character with a 4-column by 5-row sprite sheet."""

    ANIMATION_ROWS = {"idle": 0, "walk": 1, "jump": 2, "hurt": 3, "power_up": 4}

    def __init__(self, name="Explorer", color=(248, 197, 92), frames=None):
        self.name = name
        self.color = color
        self.frames = frames or {}
        self.selected = False
        self.animation = "idle"
        self.frame_index = 0
        self.frame_timer = 0.0
        self.facing_left = False

    @classmethod
    def from_sheet(cls, name, sheet):
        frames = {animation: [] for animation in cls.ANIMATION_ROWS}
        width, height = sheet.get_size()
        for animation, row in cls.ANIMATION_ROWS.items():
            for column in range(4):
                x0, x1 = round(column * width / 4), round((column + 1) * width / 4)
                y0, y1 = round(row * height / 5), round((row + 1) * height / 5)
                source = sheet.subsurface((x0, y0, x1 - x0, y1 - y0))
                cell = pygame.Surface(source.get_size(), pygame.SRCALPHA)
                cell.blit(source, (0, 0))
                bounds = cell.get_bounding_rect(min_alpha=1)
                if bounds.width and bounds.height:
                    art = cell.subsurface(bounds)
                    target_w, target_h = 52, 58
                    scale = min(target_w / art.get_width(), target_h / art.get_height())
                    size = (max(1, round(art.get_width() * scale)), max(1, round(art.get_height() * scale)))
                    art = pygame.transform.smoothscale(art, size)
                    frame = pygame.Surface((64, 64), pygame.SRCALPHA)
                    frame.blit(art, (32 - size[0] // 2, 62 - size[1]))
                else:
                    frame = pygame.Surface((64, 64), pygame.SRCALPHA)
                frames[animation].append(frame)
        return cls(name=name, frames=frames)

    def load_sprite(self, path):
        sheet = pygame.image.load(path).convert_alpha()
        self.frames = self.from_sheet(self.name, sheet).frames

    def get_sprite(self, animation=None):
        animation = animation or self.animation
        sequence = self.frames.get(animation) or self.frames.get("idle")
        return sequence[self.frame_index % len(sequence)] if sequence else None

    def update_animation(self, dt, animation=None):
        animation = animation if animation in self.ANIMATION_ROWS else "idle"
        if animation != self.animation:
            self.animation = animation
            self.frame_index = 0
            self.frame_timer = 0.0
        sequence = self.frames.get(self.animation, [])
        if len(sequence) > 1:
            rate = 0.12 if self.animation in ("walk", "jump") else 0.2
            self.frame_timer += dt
            while self.frame_timer >= rate:
                self.frame_timer -= rate
                self.frame_index = (self.frame_index + 1) % len(sequence)

    def draw(self, surface, rect):
        frame = self.get_sprite()
        if frame is None:
            pygame.draw.rect(surface, self.color, rect, border_radius=8)
            eye_y = rect.y + max(7, rect.height // 3)
            pygame.draw.circle(surface, (35, 39, 55), (rect.x + rect.width // 3, eye_y), 2)
            pygame.draw.circle(surface, (35, 39, 55), (rect.x + 2 * rect.width // 3, eye_y), 2)
            return
        image = pygame.transform.smoothscale(frame, (rect.width + 12, rect.height + 8))
        if self.facing_left:
            image = pygame.transform.flip(image, True, False)
        surface.blit(image, (rect.centerx - image.get_width() // 2, rect.bottom - image.get_height()))
