import json
import os


class HighScoreManager:
    """Loads and saves the best run score in the game's local data folder."""

    def __init__(self, file_path=None):
        root = os.path.dirname(os.path.dirname(__file__))
        self.file_path = file_path or os.path.join(root, "data", "high_score.json")
        self.high_score = self.load_high_score()

    def load_high_score(self):
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                return max(0, int(json.load(file).get("high_score", 0)))
        except (OSError, ValueError, TypeError, json.JSONDecodeError):
            return 0

    def save_high_score(self):
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        temporary_path = self.file_path + ".tmp"
        with open(temporary_path, "w", encoding="utf-8") as file:
            json.dump({"high_score": self.high_score}, file)
        os.replace(temporary_path, self.file_path)

    def update_high_score(self, score):
        if score > self.high_score:
            self.high_score = int(score)
            self.save_high_score()
        return self.high_score
