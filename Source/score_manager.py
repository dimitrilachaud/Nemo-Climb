
class ScoreManager:
    """Tracks current-run height score; persistent records are out of MVP scope."""

    def __init__(self):
        self.score = 0
        self.highest_height = 0

    def update(self, player_y):
        self.highest_height = max(self.highest_height, int(-player_y))
        self.score = self.highest_height

    def get_score(self):
        return self.score

    def reset(self):
        self.score = 0
        self.highest_height = 0
