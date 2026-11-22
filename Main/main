import os
import random
import sys

import pygame

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from Source.asset_manager import AssetManager
from Source.background_manager import BackgroundManager
from Source.camera import Camera
from Source.difficulty_manager import DifficultyManager
from Source.enemy_manager import EnemyManager
from Source.hazard_manager import HazardManager
from Source.high_score_manager import HighScoreManager
from Source.platform_manager import PlatformManager
from Source.player import Player
from Source.powerup_manager import PowerUpManager
from Source.score_manager import ScoreManager
from Source.ui_manager import UIManager
from Source.character import Character


class Game:
    WIDTH, HEIGHT = 540, 720
    FPS = 60
    # Per-effect multipliers are scaled by the Sound Effects slider.
    SFX_DEFAULT_VOLUMES = {
        "game_start_sound": 1.0,
        "game_over_sound": 1.0,
        "item_pick_up_sound": 0.05,
        "jump_sound": 0.20,
    }
    INTRO_TEXT_SECONDS = 2.6
    INTRO_IMAGE_SECONDS = 1.7
    INTRO_SCROLL_SECONDS = 4.0
    INTRO_SCROLL_ZONES = (
        "night",
        "transition_night_to_rock",
        "rocky",
        "transition_rock_to_cloud",
        "cloud",
        "transition_cloud_to_forest",
        "forest",
    )

    def __init__(self):
        pygame.init()
        try:
            if pygame.mixer.get_init() is None:
                pygame.mixer.init()
        except pygame.error:
            pass
        pygame.display.set_caption("Nemo Climb")
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = "character_select"

        self.asset_manager = AssetManager(screen_size=(self.WIDTH, self.HEIGHT))
        self.asset_manager.load_assets()
        self.music_enabled = True
        self.sfx_enabled = True
        self.music_volume = 0.55
        self.sfx_volume = 0.8
        self.settings_return_state = "character_select"
        self.music_started = False
        self._apply_audio_settings()
        self.characters = self.asset_manager.characters or [Character()]
        self.selected_character_index = 0
        self.difficulty_manager = DifficultyManager()
        self.background = BackgroundManager(self.asset_manager.backgrounds,
                                            (self.WIDTH, self.HEIGHT))
        self.camera = Camera(self.HEIGHT)
        self.platform_manager = PlatformManager(self.WIDTH, self.HEIGHT,
                                                self.difficulty_manager)
        self.enemy_manager = EnemyManager(self.WIDTH, self.HEIGHT)
        self.hazard_manager = HazardManager(self.HEIGHT)
        self.powerup_manager = PowerUpManager(self.HEIGHT)
        self.score_manager = ScoreManager()
        self.high_score_manager = HighScoreManager()
        self.ui_manager = UIManager(self.asset_manager.get_font)
        self.player = None
        self.run_started_y = 0
        self.cheat_keys = (pygame.K_f, pygame.K_l, pygame.K_y)
        self.cheat_progress = 0
        self.cheat_last_input_ms = 0
        self.intro_timer = 0.0

    @property
    def selected_character(self):
        return self.characters[self.selected_character_index]

    def run(self):
        while self.running:
            dt = min(self.clock.tick(self.FPS) / 1000, 1 / 30)
            self.handle_events()
            self.update(dt)
            self.draw()
        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif self.state == "settings":
                (self.music_enabled, self.music_volume, self.sfx_enabled,
                 self.sfx_volume, close_settings) = self.ui_manager.handle_audio_settings_event(
                    event, self.screen, self.music_enabled, self.music_volume,
                    self.sfx_enabled, self.sfx_volume)
                self._apply_audio_settings()
                if close_settings:
                    self.state = self.settings_return_state
                    if self.state == "playing":
                        self._start_background_music()
            elif self.state == "character_select":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                    self.settings_return_state = "character_select"
                    self.state = "settings"
                else:
                    index, start, quit_game = self.ui_manager.handle_character_select_event(
                        event, len(self.characters), self.selected_character_index)
                    self.selected_character_index = index
                    if start:
                        self.start_game()
                    elif quit_game:
                        self.running = False
            elif event.type == pygame.KEYDOWN:
                if self.state == "playing":
                    self._handle_fly_cheat(event)
                    if event.key == pygame.K_ESCAPE:
                        self.state = "paused"
                        if self.music_started:
                            pygame.mixer.music.pause()
                    elif event.key == pygame.K_q:
                        self.running = False
                elif self.state == "paused":
                    if event.key == pygame.K_ESCAPE:
                        self.state = "playing"
                        self._start_background_music()
                        if self.music_enabled and self.music_started:
                            pygame.mixer.music.unpause()
                    elif event.key == pygame.K_s:
                        self.settings_return_state = "paused"
                        self.state = "settings"
                    elif event.key == pygame.K_r:
                        self.return_to_character_select()
                    elif event.key == pygame.K_q:
                        self.running = False
                elif self.state == "game_over":
                    if event.key == pygame.K_r:
                        self.return_to_character_select()
                    elif event.key in (pygame.K_q, pygame.K_ESCAPE):
                        self.running = False

    def start_game(self):
        self.difficulty_manager.update(0)
        self.camera.reset()
        self.platform_manager.reset()
        self.enemy_manager.reset()
        self.hazard_manager.reset()
        self.powerup_manager.reset()
        start = self.platform_manager.platforms[0]
        self.player = Player(start.rect.centerx - 21, start.rect.top - 54,
                             self.selected_character)
        self.run_started_y = self.player.position.y
        self.score_manager.reset(self.run_started_y)
        self.background.reset(self.difficulty_manager.get_background_zone(0))
        self.intro_timer = 0.0
        self.state = "intro_text"
        self._play_effect("game_start_sound")
        if pygame.mixer.get_init() is not None:
            pygame.mixer.music.stop()
        self.music_started = False

    def return_to_character_select(self):
        if pygame.mixer.get_init() is not None:
            pygame.mixer.music.stop()
        self.music_started = False
        self.background.reset(self.difficulty_manager.get_background_zone(0))
        self.state = "character_select"

    def reset_game(self):
        """The plan's restart flow begins again at character selection."""
        self.return_to_character_select()

    def _handle_fly_cheat(self, event):
        now = pygame.time.get_ticks()
        if now - self.cheat_last_input_ms > 1500:
            self.cheat_progress = 0
        self.cheat_last_input_ms = now

        expected = self.cheat_keys[self.cheat_progress]
        if event.key == expected:
            self.cheat_progress += 1
            if self.cheat_progress == len(self.cheat_keys):
                active = self.player.toggle_flight()
                self.cheat_progress = 0
                print("Developer flight enabled." if active else "Developer flight disabled.")
        elif event.key == self.cheat_keys[0]:
            self.cheat_progress = 1
        else:
            self.cheat_progress = 0

    def update(self, dt):
        if self.state == "character_select":
            self.selected_character.update_animation(dt, "idle")
            return
        if self.state == "intro_text":
            self.intro_timer += dt
            if self.intro_timer >= self.INTRO_TEXT_SECONDS:
                self.intro_timer = 0.0
                self.state = "intro_image"
            return
        if self.state == "intro_image":
            self.intro_timer += dt
            if self.intro_timer >= self.INTRO_IMAGE_SECONDS:
                self.intro_timer = 0.0
                self.state = "intro_scroll"
            return
        if self.state == "intro_scroll":
            self.intro_timer += dt
            if self.intro_timer >= self.INTRO_SCROLL_SECONDS:
                self.state = "playing"
                self._start_background_music()
            return
        if self.state != "playing" or self.player is None:
            return

        keys = pygame.key.get_pressed()
        self.player.handle_input(keys)
        if not self.player.flying and (keys[pygame.K_SPACE] or keys[pygame.K_UP]):
            if self.player.jump():
                self._play_effect("jump_sound")

        self.powerup_manager.update(dt, self.camera.offset_y)
        self.player.set_double_jump_active(self.powerup_manager.is_active("double_jump"))
        self.platform_manager.freeze_moving = self.powerup_manager.is_active("freeze")
        self.platform_manager.update(dt, self.player.position.y, self.camera.offset_y)
        self.powerup_manager.populate_platforms(self.platform_manager.platforms,
                                               self.camera.offset_y)
        self._populate_platform_features()
        self.enemy_manager.update(dt, self.camera.offset_y)
        self.hazard_manager.update(dt, self.camera.offset_y)
        landed_platform = self.player.update(dt, self.platform_manager.platforms, self.WIDTH)
        if landed_platform is not None:
            self.score_manager.platform_reached(landed_platform)
            self.player.refresh_double_jump_on_landing()

        collected_powers = self.powerup_manager.collect(self.player.rect)
        if collected_powers:
            self._play_effect("item_pick_up_sound")
        if "double_jump" in collected_powers:
            self.player.set_double_jump_active(self.powerup_manager.is_active("double_jump"))

        self.score_manager.update(self.player.position.y)
        self.high_score_manager.update_high_score(self.score_manager.get_score())
        self.difficulty_manager.update(self.score_manager.highest_height)
        zone_background = self.difficulty_manager.get_background_zone()
        self.background.update(dt, zone_background)
        self.camera.update(self.player, dt)

        hit_enemy = self.enemy_manager.check_collision(self.player)
        hit_hazard = self.hazard_manager.check_collision(self.player)
        screen_player = self.camera.apply(self.player.rect)
        outside_camera = screen_player.bottom < 0 or screen_player.top > self.HEIGHT
        if (hit_enemy or hit_hazard) and not self.powerup_manager.is_active("immunity"):
            self.player.set_hurt()
            self.end_game()
        elif outside_camera:
            self.end_game()

    def _populate_platform_features(self):
        for platform in self.platform_manager.platforms:
            if platform.feature_checked:
                continue
            platform.feature_checked = True
            height = max(0, int(self.run_started_y - platform.rect.y))
            # Keep the starting steps clear; hazards and enemies begin after the player
            # has learned the jump rhythm and become more common in later zones.
            if height < 240 or platform.platform_type == "moving":
                continue
            hazard_settings = self.difficulty_manager.get_hazard_settings(height)
            enemy_settings = self.difficulty_manager.get_enemy_settings(height)
            roll = random.random()
            if roll < hazard_settings["spawn_chance"]:
                placed = self.hazard_manager.spawn_on_platform(
                    platform, random.choice(hazard_settings["types"]))
                if not placed and random.random() < enemy_settings["spawn_chance"]:
                    self.enemy_manager.spawn_on_platform(platform, enemy_settings["speed"])
            elif roll < hazard_settings["spawn_chance"] + enemy_settings["spawn_chance"]:
                self.enemy_manager.spawn_on_platform(platform, enemy_settings["speed"])

    def end_game(self):
        if self.state == "game_over":
            return
        self.high_score_manager.update_high_score(self.score_manager.get_score())
        self.state = "game_over"
        if pygame.mixer.get_init() is not None:
            pygame.mixer.music.stop()
        self.music_started = False
        self._play_effect("game_over_sound")

    def _play_effect(self, name):
        if not self.sfx_enabled or pygame.mixer.get_init() is None:
            return
        sound = self.asset_manager.get_sound(name)
        if sound is not None:
            sound.play()

    def _apply_audio_settings(self):
        if pygame.mixer.get_init() is None:
            return
        for name, sound in self.asset_manager.sounds.items():
            default_volume = self.SFX_DEFAULT_VOLUMES.get(name, 1.0)
            sound.set_volume(self.sfx_volume * default_volume if self.sfx_enabled else 0.0)
        pygame.mixer.music.set_volume(self.music_volume if self.music_enabled else 0.0)
        if not self.music_enabled and self.music_started:
            pygame.mixer.music.stop()
            self.music_started = False
        elif self.music_enabled and self.state == "playing":
            self._start_background_music()

    def _start_background_music(self):
        if (not self.music_enabled or pygame.mixer.get_init() is None or
                self.music_started):
            return
        music_path = self.asset_manager.music_tracks.get("game_loop_music")
        if music_path:
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.set_volume(self.music_volume)
            pygame.mixer.music.play(-1)
            self.music_started = True

    def draw(self):
        if self.state == "settings":
            self.background.draw(self.screen)
            self.ui_manager.draw_audio_settings(
                self.screen, self.music_enabled, self.music_volume,
                self.sfx_enabled, self.sfx_volume,
                "RETURN TO PAUSE" if self.settings_return_state == "paused" else "BACK")
            pygame.display.flip()
            return
        if self.state == "intro_text":
            self.ui_manager.draw_intro_text(self.screen)
            pygame.display.flip()
            return
        if self.state == "intro_image":
            intro_image = self.asset_manager.get_background("intro")
            self.screen.fill((0, 0, 0))
            if intro_image is not None:
                self.screen.blit(intro_image, (0, 0))
            pygame.display.flip()
            return
        if self.state == "intro_scroll":
            progress = min(1.0, self.intro_timer / self.INTRO_SCROLL_SECONDS)
            self.background.draw_vertical_sequence(self.screen, self.INTRO_SCROLL_ZONES, progress)
            pygame.display.flip()
            return
        self.background.draw(self.screen)
        if self.state == "character_select":
            self.ui_manager.draw_character_select(self.screen, self.characters,
                                                  self.selected_character_index,
                                                  self.high_score_manager.high_score)
        else:
            self.platform_manager.draw(self.screen, self.camera)
            self.powerup_manager.draw(self.screen, self.camera)
            self.hazard_manager.draw(self.screen, self.camera)
            self.enemy_manager.draw(self.screen, self.camera)
            if self.player:
                self.player.draw(self.screen, self.camera)
            self.ui_manager.draw_hud(self.screen, self.score_manager.get_score(),
                                     self.score_manager.highest_height,
                                     self.high_score_manager.high_score,
                                     self.difficulty_manager.get_zone_name(),
                                     self.player.flying if self.player else False,
                                     self.powerup_manager.active_icons())
            if self.state == "paused":
                self.ui_manager.draw_pause_screen(self.screen)
            elif self.state == "game_over":
                self.ui_manager.draw_game_over(self.screen, self.score_manager.get_score(),
                                               self.score_manager.highest_height,
                                               self.high_score_manager.high_score)
        pygame.display.flip()


if __name__ == "__main__":
    Game().run()
