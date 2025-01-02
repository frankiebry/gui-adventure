import random
from settings import settings
from utils import calculate_distance
from typewriter import typewriter

class Monster:
    def __init__(self, initial_position):
        """
        Initializes the Monster class with an initial position and the turn counter.
        
        Args:
        initial_position (tuple): The (x, y) coordinates of the monster's starting position.
        """
        self.position = initial_position
        self.repellent_turns_left = 0  # Track how many turns the repellent is active

    def random_move(self):
        """
        Moves the monster in a random direction (north, south, east, west) if the move is within bounds.
        If the monster tries to move out of bounds, another random direction is chosen.
        20% chance that the monster will not move.
        """
        directions = ["north", "south", "east", "west", "yawn"]
        while True:  # Loop until a valid move is made
            direction = random.choice(directions)
            
            if direction == "north" and self.position[1] > 0:
                self.position = (self.position[0], self.position[1] - 1)
                break
            elif direction == "south" and self.position[1] < settings.GRID_HEIGHT - 1:
                self.position = (self.position[0], self.position[1] + 1)
                break
            elif direction == "east" and self.position[0] < settings.GRID_WIDTH - 1:
                self.position = (self.position[0] + 1, self.position[1])
                break
            elif direction == "west" and self.position[0] > 0:
                self.position = (self.position[0] - 1, self.position[1])
                break
            elif direction == "yawn":
                typewriter("You hear a low yawn echoing in the distance.", 0.05)
                break

    def is_near_player(self, player_position):
        """
        Checks if the monster is within 2 steps of the player using Manhattan distance.
        
        Args:
        player_position (tuple): The (x, y) coordinates of the player's position.
        
        Returns:
        bool: True if the monster is within 2 steps of the player, otherwise False.
        """
        # Manhattan distance: sum of absolute differences in x and y
        distance = calculate_distance(self.position, player_position)
        return distance <= 2  # Monster chases the player if within 2 steps

    def chase_player(self, player_position):
        """
        Moves the monster one step towards the player's position.
        
        Args:
        player_position (tuple): The (x, y) coordinates of the player's position.
        """
        # Move towards the player horizontally or vertically
        if self.position[0] < player_position[0] and self.position[0] < settings.GRID_WIDTH - 1:
            self.position = (self.position[0] + 1, self.position[1])
        elif self.position[0] > player_position[0] and self.position[0] > 0:
            self.position = (self.position[0] - 1, self.position[1])
        elif self.position[1] < player_position[1] and self.position[1] < settings.GRID_HEIGHT - 1:
            self.position = (self.position[0], self.position[1] + 1)
        elif self.position[1] > player_position[1] and self.position[1] > 0:
            self.position = (self.position[0], self.position[1] - 1)

    # This is basically just the opposite of chase_player(). Can this code be less repetitive?
    def avoid_player(self, player_position):
        """
        Moves the monster one step away from the player's position.
        
        Args:
        player_position (tuple): The (x, y) coordinates of the player's position.
        """
        # Move away from the player horizontally or vertically
        if self.position[0] > player_position[0] and self.position[0] < settings.GRID_WIDTH - 1:
            self.position = (self.position[0] + 1, self.position[1])
        elif self.position[0] < player_position[0] and self.position[0] > 0:
            self.position = (self.position[0] - 1, self.position[1])
        elif self.position[1] > player_position[1] and self.position[1] < settings.GRID_HEIGHT - 1:
            self.position = (self.position[0], self.position[1] + 1)
        elif self.position[1] < player_position[1] and self.position[1] > 0:
            self.position = (self.position[0], self.position[1] - 1)

    def check_if_caught(self, player_position):
        """
        Checks if the monster has caught the player by comparing their positions.
        
        Args:
        player_position (tuple): The (x, y) coordinates of the player's position.
        
        Returns:
        bool: True if the monster has caught the player, otherwise False.
        """
        if self.repellent_turns_left > 0:
            return False
        return self.position == player_position
    
    def move(self, player_position):
        """
        Determines the monster's movement based on the turn count and its proximity to the player.
        The monster moves every two turns. If it's near the player, it chases the player; otherwise, it moves randomly.
        
        Args:
        player_position (tuple): The (x, y) coordinates of the player's position.
        """
        
        # If repellent is active, the monster avoids the player
        if self.repellent_turns_left > 0:
            self.repellent_turns_left -= 1
            self.avoid_player(player_position)
        # If the monster is close to the player and no repellent is active, it chases the player,
        elif self.is_near_player(player_position):
            typewriter("\033[91mYou hear a bloodcurdling howl as a foul stench fills the air.\033[0m", 0.05)
            self.chase_player(player_position)
        # else it moves randomly
        else:
            self.random_move()