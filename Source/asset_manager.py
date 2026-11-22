import os
import pygame
from .character import Character


class AssetManager:
    """Loads optional sprite sheets, zone backgrounds, fonts, and sounds."""

    def __init__(self, asset_folder=None, screen_size=(540, 720)):
        self.asset_folder = asset_folder or os.path.join(os.path.dirname(os.path.dirname(__file__)), "Assets")
        self.screen_size = screen_size
        self.sprites = {}
        self.backgrounds = {}
        self.characters = []
        self.fonts = {}
        self.sounds = {}
        self.music_tracks = {}

    @staticmethod
    def _asset_key(filename):
        key = os.path.splitext(filename)[0]
        return key[:-4].lower() if key.lower().endswith(".png") else key.lower()

    def load_assets(self):
        if not os.path.isdir(self.asset_folder):
            return
        for filename in sorted(os.listdir(self.asset_folder)):
            path = os.path.join(self.asset_folder, filename)
            key = self._asset_key(filename)
            extension = filename.lower().split(".")[-1]
            try:
                if key.startswith("character_") and extension == "png":
                    sheet = pygame.image.load(path).convert_alpha()
                    if sheet.get_at((0, 0))[:3] == (255, 255, 255):
                        sheet.set_colorkey((255, 255, 255))
                    self.sprites[key] = sheet
                    character_name = key[len("character_"):].replace("_", " ").title()
                    self.characters.append(Character.from_sheet(character_name, sheet))
                elif key.startswith("background_") and extension in ("png", "jpg", "jpeg"):
                    image = pygame.image.load(path).convert()
                    self.backgrounds[key[len("background_"):]] = pygame.transform.smoothscale(image, self.screen_size)
                elif key.startswith("transition_") and extension in ("png", "jpg", "jpeg"):
                    image = pygame.image.load(path).convert()
                    transition_name = key.replace(" ", "_")
                    self.backgrounds[transition_name] = pygame.transform.smoothscale(
                        image, self.screen_size)
                elif extension in ("wav", "ogg", "mp3"):
                    audio_key = key.replace(" ", "_")
                    if audio_key == "game_loop_music":
                        self.music_tracks[audio_key] = path
                    else:
                        self.sounds[audio_key] = pygame.mixer.Sound(path)
            except (pygame.error, OSError, ValueError):
                continue
        self.characters.sort(key=lambda character: (character.name.lower() != "default", character.name.lower()))

    def get_sprite(self, name):
        return self.sprites.get(name)

    def get_background(self, name):
        return self.backgrounds.get(name)

    def get_sound(self, name):
        return self.sounds.get(name)

    def get_font(self, name="default", size=24):
        key = (name, size)
        if key not in self.fonts:
            self.fonts[key] = pygame.font.Font(name if os.path.isfile(name) else None, size)
        return self.fonts[key]
