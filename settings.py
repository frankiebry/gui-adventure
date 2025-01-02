import random

class Settings:
    def __init__(self):
        self.reset()

    def reset(self):
        """
        Resets all settings to their initial random state, including when the game starts.
        Change any initial settings here
        """
        self.GRID_WIDTH = random.randint(4, 8) # The map will not be larger than 8x8
        self.GRID_HEIGHT = random.randint(4, 8)
        # self.DEFAULT_NUM_OF_TORCHES = 3
        self.DEFAULT_SEARCHED_POSITIONS = []
        self.DEFAULT_PLAYER_POS = self.randomize_position()
        self.DEFAULT_KEY_POS = self.randomize_position()
        self.DEFAULT_EXIT_POS = self.randomize_position()
        self.DEFAULT_MONSTER_POS = self.randomize_position()

    def randomize_position(self):
        """Generate a random position within the grid."""
        return (random.randint(0, self.GRID_WIDTH - 1), random.randint(0, self.GRID_HEIGHT - 1))

# Create a single instance of the Settings class
settings = Settings()