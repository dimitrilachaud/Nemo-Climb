import os
import pygame


class AssetManager:
    """Optional asset loading helpers; the MVP runs with drawn placeholders."""

    def __init__(self, asset_folder=None):
        self.asset_folder = asset_folder or os.path.join(os.path.dirname(os.path.dirname(__file__)), "Assets")
        self.sprites = {}
        self.backgrounds = {}

    def load_assets(self):
        """Load PNG/JPG assets from Assets when present; missing art is allowed."""
        if not os.path.isdir(self.asset_folder):
            return
        for filename in os.listdir(self.asset_folder):
            path = os.path.join(self.asset_folder, filename)
            key, extension = os.path.splitext(filename)
            try:
                if extension.lower() in (".png", ".jpg", ".jpeg"):
                    image = pygame.image.load(path).convert_alpha()
                    self.sprites[key] = image
            except pygame.error:
                continue

    def get_sprite(self, name):
        return self.sprites.get(name)

    def get_background(self, name):
        return self.backgrounds.get(name)
