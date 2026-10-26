import pygame


class UIManager:
    def __init__(self):
        self.font = pygame.font.Font(None, 30)
        self.title_font = pygame.font.Font(None, 68)

    def draw_hud(self, surface, score):
        label = self.font.render(f"HEIGHT  {score}", True, (245, 245, 250))
        surface.blit(label, (18, 16))
        hint = pygame.font.Font(None, 22).render("Move: A/D or arrows    Pause: Esc", True, (180, 190, 211))
        surface.blit(hint, (18, 48))

    def draw_pause_screen(self, surface):
        self._overlay(surface)
        self._center(surface, "PAUSED", -28, self.title_font)
        self._center(surface, "Press Esc to continue", 28, self.font)

    def draw_game_over(self, surface, score):
        self._overlay(surface)
        self._center(surface, "GAME OVER", -68, self.title_font)
        self._center(surface, f"Height: {score}", -8, self.font)
        self._center(surface, "R  Restart     Q  Quit", 42, self.font)

    def _overlay(self, surface):
        shade = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        shade.fill((8, 12, 24, 190))
        surface.blit(shade, (0, 0))

    def _center(self, surface, text, y_offset, font):
        rendered = font.render(text, True, (250, 248, 238))
        surface.blit(rendered, (surface.get_width() // 2 - rendered.get_width() // 2,
                                surface.get_height() // 2 + y_offset))
