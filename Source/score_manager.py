class ScoreManager:
    """Counts newly reached platforms and tracks this run's highest height."""

    def __init__(self, starting_y=0):
        self.starting_y = starting_y
        self.score = 0
        self.highest_height = 0
        self.last_scored_height = 0

    def update(self, player_y):
        self.highest_height = max(self.highest_height, max(0, int(self.starting_y - player_y)))
        self.last_scored_height = self.highest_height

    def platform_reached(self, platform):
        if not platform.reached:
            platform.reached = True
            self.score += 1
            return True
        return False

    def get_score(self):
        return self.score

    def get_high_score(self):
        return self.score

    def reset(self, starting_y=0):
        self.starting_y = starting_y
        self.score = 0
        self.highest_height = 0
        self.last_scored_height = 0
