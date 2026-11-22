import pygame
from .powerup import PowerUp


class UIManager:
    def __init__(self, font_loader=None):
        self.font_loader = font_loader
        self.font = self._font(30)
        self.small_font = self._font(22)
        self.title_font = self._font(68)

    def _font(self, size):
        return self.font_loader("default", size) if self.font_loader else pygame.font.Font(None, size)

    def draw_character_select(self, surface, characters, selected_index, high_score=0):
        self._overlay(surface, 150)
        self._center(surface, "CHOOSE YOUR CLIMBER", -245, self.title_font)
        self._center(surface, "Select with Left/Right, then press Enter", -190, self.small_font)
        if not characters:
            self._center(surface, "No character sheets found", -20, self.font)
        else:
            selected_index %= len(characters)
            card_w, card_h = 150, 220
            gap = 18
            shown = min(3, len(characters))
            total_w = shown * card_w + (shown - 1) * gap
            start_x = max(14, (surface.get_width() - total_w) // 2)
            left = max(0, min(selected_index - shown // 2, len(characters) - shown))
            for visible_index in range(left, left + shown):
                character = characters[visible_index]
                character.selected = visible_index == selected_index
                rect = pygame.Rect(start_x + (visible_index - left) * (card_w + gap),
                                   surface.get_height() // 2 - 112, card_w, card_h)
                fill = (50, 76, 100) if character.selected else (34, 45, 66)
                border = (255, 218, 128) if character.selected else (100, 122, 151)
                pygame.draw.rect(surface, fill, rect, border_radius=14)
                pygame.draw.rect(surface, border, rect, 3 if character.selected else 1, border_radius=14)
                preview = pygame.Rect(rect.centerx - 32, rect.y + 24, 64, 92)
                character.draw(surface, preview)
                label = self.font.render(character.name, True, (248, 245, 233))
                surface.blit(label, (rect.centerx - label.get_width() // 2, rect.bottom - 54))
                hint = self.small_font.render("SELECTED" if character.selected else "", True, (255, 218, 128))
                surface.blit(hint, (rect.centerx - hint.get_width() // 2, rect.bottom - 28))
        self._center(surface, f"BEST RUN  {high_score} platforms", 258, self.small_font)
        self._center(surface, "Press S for audio settings", 292, self.small_font)

    def draw_intro_text(self, surface):
        surface.fill((0, 0, 0))
        font = pygame.font.Font(None, 27)
        lines = ("Climb to the top", "to rescue your partner")
        rendered_lines = []
        for line in lines:
            text = font.render(line, False, (245, 245, 245))
            rendered_lines.append(pygame.transform.scale(text, (text.get_width() * 2,
                                                                  text.get_height() * 2)))
        total_height = sum(line.get_height() for line in rendered_lines) + 14
        y = surface.get_height() // 2 - total_height // 2
        for line in rendered_lines:
            surface.blit(line, (surface.get_width() // 2 - line.get_width() // 2, y))
            y += line.get_height() + 14

    def handle_character_select_event(self, event, character_count, selected_index):
        if event.type != pygame.KEYDOWN or character_count <= 0:
            return selected_index, False, False
        if event.key in (pygame.K_LEFT, pygame.K_a):
            return (selected_index - 1) % character_count, False, False
        if event.key in (pygame.K_RIGHT, pygame.K_d):
            return (selected_index + 1) % character_count, False, False
        if event.key in (pygame.K_RETURN, pygame.K_SPACE):
            return selected_index, True, False
        if event.key == pygame.K_q:
            return selected_index, False, True
        return selected_index, False, False

    def draw_hud(self, surface, score, height, high_score, zone_name, flying=False,
                 active_powers=()):
        panel = pygame.Surface((surface.get_width(), 124), pygame.SRCALPHA)
        panel.fill((10, 15, 27, 145))
        surface.blit(panel, (0, 0))
        surface.blit(self.font.render(f"HEIGHT  {height}", True, (250, 248, 238)), (18, 12))
        surface.blit(self.small_font.render(f"SCORE  {score}     BEST  {high_score}", True, (215, 225, 239)), (18, 46))
        zone = self.small_font.render(zone_name.upper(), True, (255, 218, 128))
        surface.blit(zone, (surface.get_width() - zone.get_width() - 18, 18))
        controls = self.small_font.render("Move A/D   Hold Space/Up to jump   Camera rising",
                                          True, (185, 199, 218))
        surface.blit(controls, (18, 76))
        power_x = surface.get_width() - 18 - len(active_powers) * 66
        for index, (power_type, remaining) in enumerate(active_powers):
            icon_rect = pygame.Rect(power_x + index * 66, 43, 30, 30)
            PowerUp.draw_icon(surface, icon_rect, power_type)
            timer = self.small_font.render(f"{remaining:.1f}", True, (248, 248, 240))
            surface.blit(timer, (icon_rect.right + 3, 49))
        if flying:
            badge = self.small_font.render("DEV FLIGHT", True, (138, 243, 224))
            surface.blit(badge, (18, 101))

    def draw_pause_screen(self, surface):
        self._overlay(surface)
        self._center(surface, "PAUSED", -35, self.title_font)
        self._center(surface, "Esc: resume       S: audio settings", 24, self.small_font)
        self._center(surface, "R: character select       Q: quit", 58, self.small_font)

    def draw_audio_settings(self, surface, music_enabled, music_volume,
                            sfx_enabled, sfx_volume, return_label="BACK"):
        self._overlay(surface, 220)
        self._center(surface, "AUDIO SETTINGS", -270, self.title_font)
        music_toggle = pygame.Rect(330, 253, 150, 44)
        sfx_toggle = pygame.Rect(330, 383, 150, 44)
        self._right_label(surface, "Background Music", music_toggle.left - 18,
                          music_toggle.centery, self.font)
        self._draw_toggle(surface, music_toggle, music_enabled)
        self._center(surface, f"Music volume: {round(music_volume * 100)}%", -50,
                     self.small_font)
        self._draw_slider(surface, pygame.Rect(110, 337, 320, 12), music_volume)
        self._right_label(surface, "Sound Effects", sfx_toggle.left - 18,
                          sfx_toggle.centery, self.font)
        self._draw_toggle(surface, sfx_toggle, sfx_enabled)
        self._center(surface, f"Effects volume: {round(sfx_volume * 100)}%", 80,
                     self.small_font)
        self._draw_slider(surface, pygame.Rect(110, 467, 320, 12), sfx_volume)
        self._center(surface, "Click a toggle or slider. Press Esc to return.", 145,
                     self.small_font)
        back_rect = pygame.Rect(surface.get_width() // 2 - 100, 625, 200, 48)
        self.draw_button(surface, back_rect, return_label)

    def handle_audio_settings_event(self, event, surface, music_enabled,
                                    music_volume, sfx_enabled, sfx_volume):
        """Return updated settings and whether the settings screen should close."""
        if event.type == pygame.KEYDOWN and event.key in (pygame.K_ESCAPE, pygame.K_RETURN):
            return music_enabled, music_volume, sfx_enabled, sfx_volume, True

        if event.type not in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP,
                              pygame.MOUSEMOTION):
            return music_enabled, music_volume, sfx_enabled, sfx_volume, False

        position = getattr(event, "pos", pygame.mouse.get_pos())
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if pygame.Rect(330, 253, 150, 44).collidepoint(position):
                music_enabled = not music_enabled
            elif pygame.Rect(330, 383, 150, 44).collidepoint(position):
                sfx_enabled = not sfx_enabled
            elif pygame.Rect(surface.get_width() // 2 - 100, 625, 200, 48).collidepoint(position):
                return music_enabled, music_volume, sfx_enabled, sfx_volume, True

        dragging = event.type == pygame.MOUSEMOTION and bool(
            pygame.mouse.get_pressed()[0])
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 or dragging:
            slider_x, slider_y, slider_width = 110, 337, 320
            if abs(position[1] - slider_y) <= 18:
                music_volume = max(0.0, min(1.0, (position[0] - slider_x) / slider_width))
            slider_y = 467
            if abs(position[1] - slider_y) <= 18:
                sfx_volume = max(0.0, min(1.0, (position[0] - slider_x) / slider_width))
        return music_enabled, music_volume, sfx_enabled, sfx_volume, False

    def _draw_toggle(self, surface, rect, enabled):
        color = (47, 135, 111) if enabled else (83, 91, 106)
        pygame.draw.rect(surface, color, rect, border_radius=9)
        pygame.draw.rect(surface, (225, 235, 244), rect, 2, border_radius=9)
        label = "ON" if enabled else "OFF"
        text = self.font.render(label, True, (250, 248, 238))
        surface.blit(text, (rect.centerx - text.get_width() // 2,
                            rect.centery - text.get_height() // 2))

    def _right_label(self, surface, text, right, center_y, font):
        rendered = font.render(text, True, (250, 248, 238))
        surface.blit(rendered, (right - rendered.get_width(),
                                center_y - rendered.get_height() // 2))

    def _draw_slider(self, surface, rect, value):
        pygame.draw.rect(surface, (75, 88, 108), rect, border_radius=6)
        fill = pygame.Rect(rect.x, rect.y, round(rect.width * value), rect.height)
        if fill.width:
            pygame.draw.rect(surface, (114, 197, 225), fill, border_radius=6)
        knob_x = rect.x + round(rect.width * value)
        pygame.draw.circle(surface, (242, 248, 255), (knob_x, rect.centery), 11)
        pygame.draw.circle(surface, (62, 117, 155), (knob_x, rect.centery), 11, 2)

    def draw_game_over(self, surface, score, height, high_score):
        self._overlay(surface)
        self._center(surface, "GAME OVER", -82, self.title_font)
        self._center(surface, f"Run score: {score}     Height: {height}", -22, self.font)
        self._center(surface, f"Best score: {high_score}", 20, self.small_font)
        self._center(surface, "R: character select      Q: quit", 66, self.small_font)

    def draw_button(self, surface, rect, label, selected=False):
        pygame.draw.rect(surface, (58, 82, 108) if selected else (34, 45, 66), rect, border_radius=8)
        pygame.draw.rect(surface, (255, 218, 128) if selected else (100, 122, 151), rect, 2, border_radius=8)
        text = self.font.render(label, True, (250, 248, 238))
        surface.blit(text, (rect.centerx - text.get_width() // 2, rect.centery - text.get_height() // 2))

    def draw_game_over_event(self, surface, score, height, high_score):
        self.draw_game_over(surface, score, height, high_score)

    def _overlay(self, surface, alpha=190):
        shade = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        shade.fill((8, 12, 24, alpha))
        surface.blit(shade, (0, 0))

    def _center(self, surface, text, y_offset, font):
        rendered = font.render(text, True, (250, 248, 238))
        surface.blit(rendered, (surface.get_width() // 2 - rendered.get_width() // 2,
                                surface.get_height() // 2 + y_offset))
