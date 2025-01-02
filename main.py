from monster import Monster
from typewriter import typewriter
from settings import settings
from utils import calculate_distance
from commands import commands_dict 
from inventory import inventory

# Our main game class
class Game:
    def __init__(self):
        """Initialize the game by resetting to default settings."""
        self.reset_game() # Reset the game to its initial state with default settings

    def reset_game(self):
        """Reset the game to its initial state with default settings."""
        inventory.reset() # Reset player inventory to its default state
        settings.reset() # Reset the settings to their default values
        self.searched_positions = settings.DEFAULT_SEARCHED_POSITIONS
        self.player_position = settings.DEFAULT_PLAYER_POS
        self.key_position = settings.DEFAULT_KEY_POS
        self.exit_position = settings.DEFAULT_EXIT_POS
        self.monster = Monster(settings.DEFAULT_MONSTER_POS)

    def draw_map(self, show_key=False):
        """
        Draw the game map with the player, monster, and optionally the key.

        Args:
            show_key (bool): Whether to display the key on the map.
        """
        grid = [['⬚ ' for _ in range(settings.GRID_WIDTH)] for _ in range(settings.GRID_HEIGHT)]
        
        # Mark the spots the player has already dug on the map
        for pos in self.searched_positions: 
            x, y = pos
            grid[y][x] = '\033[96m⛝ \033[0m' # Use ANSI escape codes for colored text - Bright Cyan
        
        # Draw the player location on the map
        player_x, player_y = self.player_position
        grid[player_y][player_x] = '\033[92m♙ \033[0m' # Bright Green
        
        # Draw the monster location on the map
        monster_x, monster_y = self.monster.position
        grid[monster_y][monster_x] = '\033[91m♞ \033[0m' # Bright Red
        
        exit_x, exit_y = self.exit_position
        grid[exit_y][exit_x] = '⬕ ' # Default White
        
        # Draw the key if cheat is used and key is still on the map
        if show_key and self.key_position:
            key_x, key_y = self.key_position
            grid[key_y][key_x] = '\033[93m⚿ \033[0m' # Bright Yellow
        for row in grid: # Print the map row by row
            print(''.join(row))

    def light_torch(self):
        """Use a torch to reveal the map and display helpful information."""
        if inventory.has_item("torch"): # Check if the player has any torches left
            inventory.use_item("torch")  # Use one torch from inventory
            typewriter("You light a torch and check your map.", 0.05)
            print(' ')
            self.draw_map()
            print(' ')
            typewriter("\033[92m♙\033[0m - Your current location.", 0.05)
            typewriter("\033[96m⛝\033[0m - Spots where you've already dug.", 0.05)
            typewriter("\033[91m♞\033[0m - You see an ominous shadowy standing there.", 0.05)
            typewriter("⬕ - The exit is at this location.", 0.05)
    
            if inventory.items["torch"] == 1: # Handle singular vs. plural in the message.
                typewriter(f'The light has gone out. You have {inventory.items["torch"]} torch left', 0.05)
            else:
                typewriter(f'The light has gone out. You have {inventory.items["torch"]} torches left', 0.05)
        else:
            typewriter("You don't have any torches left", 0.05)

    def use_metal_detector(self):
        """Use the metal detector to get a hint about the key's location."""
        if inventory.has_item("metal detector"): # Check if the player has a metal detector:
            
            # Right now this code will always be executed, consider making the metal detector have limited uses
            # or make it a key item that is found from digging
            if self.key_position is None:
                typewriter("The metal detector is silent.", 0.05)
            else:
                distance = calculate_distance(self.player_position, self.key_position)
                if distance == 0:
                    typewriter("The metal detector is going wild!!", 0.05)
                elif distance == 1:
                    typewriter("The metal detector is beeping rapidly!", 0.05)
                elif distance == 2:
                    typewriter("The metal detector is slowly beeping.", 0.05)
                else:
                    typewriter("The metal detector is silent.", 0.05)

    def use_monster_repellent(self, monster):
        if inventory.has_item("monster repellent"):
            inventory.use_item("monster repellent")
            # Set the repellent effect on the monster
            monster.repellent_turns_left = 3
            typewriter("You used a \033[95mmonster repellent\033.", 0.05) # why doesn't the "." show up?
            typewriter("\033[95mYou hear a disgruntled growl as the sound of heavy footfalls fade away.\033[0m", 0.05)
        else:
            typewriter("You don't have any monster repellent.", 0.05)

    # TODO Can this be written more elegantly?
    def dig(self):
        """Handle the player digging at their current position."""
        if self.player_position in self.searched_positions: # Check if the player has already dug here
            typewriter("You have already dug here.", 0.05)
        else:
            self.searched_positions.append(self.player_position) # Mark the spot as searched
        
            if self.player_position == self.key_position: # Check if the player has found the key
                inventory.add_item("key", 1)  # Add the key to the inventory
                self.key_position = None  # Remove the key from the map
                typewriter("You found the \033[93mkey\033[0m!", 0.05)
                print(' ')
            else:
                inventory.find_random_item()

    # # Rewrite this entire thing
    # def display_commands(self):
    #     """Display the list of available commands to the player."""
    #     print(' ')
    #     typewriter("*****************", 0.02)
    #     typewriter("* Legal commands *", 0.02)
    #     typewriter("*****************", 0.02)
    #     print(' ')
    #     typewriter("MOVE NORTH", 0.02)
    #     typewriter("MOVE SOUTH", 0.02)
    #     typewriter("MOVE EAST", 0.02)
    #     typewriter("MOVE WEST", 0.02)
    #     typewriter("DIG HERE", 0.02)
    #     typewriter("USE A TORCH: check your map", 0.02)
    #     typewriter("SWEEP FOR KEY: use metal detector", 0.02)
    #     typewriter("UNLOCK DOOR: unlock the exit", 0.02)
    #     print(' ')

    def debug(self):
        """Display the full map, including the key's location (cheat/debug mode)."""
        print(' ')
        self.draw_map(show_key=True) # Show the key on the map
        print(' ')

    def welcome_screen(self):
        """Display the welcome screen and explain the rules for first timers."""
        response = input(
            "Welcome to Frankie's text based adventure game. Have you played this game before? (Y/N): "
        ).strip().lower()
        if response in ['n', 'no']:
            print(' ')
            typewriter('Here are the rules...', 0.05)
            print(' ')
            typewriter('You are in a dark cave and need to find the \033[93mkey\033[0m to the exit.', 0.05)
            typewriter('Each turn you can try to do one of the following:', 0.05)
            typewriter('* Move north, south, east or west', 0.05)
            typewriter('* Dig to find the \033[93mkey\033[0m. You may also find helpful items or treasure.', 0.05)
            typewriter('* Use an item from your inventory', 0.05)
            typewriter('* Check your inventory', 0.05)
            typewriter('* Try to unlock the exit.', 0.05)
            typewriter(
                'Beware, there is a \033[91mmonster\033[0m in the cave with you. '
                'Each turn the \033[91mmonster\033[0m will move one pace.',
                0.05
            )
            typewriter('Good luck!', 0.05)

    def play_again(self):
        """Prompt the player to decide whether to play again."""
        response = input("Do you want to play again? (Y/N): ").strip().lower()
        return response in ["y", "yes"]

    def run(self):
        """Run the main game loop, handling player commands and game logic."""
        self.welcome_screen()
        while True:
            print(' ')
            command = input("What do you want to do?: ").strip().lower()
            monster_should_move = True # Assume the monster will move on each turn by default

            # We are using a dictionary of lists to store the possible commands
            match command:
                case _ if command in commands_dict["up"]:
                    if self.player_position[1] > 0:
                        self.player_position = (self.player_position[0], self.player_position[1] - 1)
                        typewriter("You moved north.", 0.05)
                    else:
                        typewriter("The way is blocked.", 0.05)

                case _ if command in commands_dict["down"]:
                    if self.player_position[1] < settings.GRID_HEIGHT - 1:
                        self.player_position = (self.player_position[0], self.player_position[1] + 1)
                        typewriter("You moved south.", 0.05)
                    else:
                        typewriter("The way is blocked.", 0.05)

                case _ if command in commands_dict["right"]:
                    if self.player_position[0] < settings.GRID_WIDTH - 1:
                        self.player_position = (self.player_position[0] + 1, self.player_position[1])
                        typewriter("You moved east.", 0.05)
                    else:
                        typewriter("The way is blocked.", 0.05)

                case _ if command in commands_dict["left"]:
                    if self.player_position[0] > 0:
                        self.player_position = (self.player_position[0] - 1, self.player_position[1])
                        typewriter("You moved west.", 0.05)
                    else:
                        typewriter("The way is blocked.", 0.05)

                # TODO put this in it's own dig function?
                case _ if command in commands_dict["dig"]:
                    self.dig()

                case _ if command in commands_dict["inventory"]:
                    inventory.show_inventory()

                case _ if command in commands_dict["torch"]:
                    self.light_torch()

                case _ if command in commands_dict["sweep"]:
                    self.use_metal_detector()
                    
                case _ if command in commands_dict["repel"]:
                    self.use_monster_repellent(self.monster)
                    
                # Handle all this in a function?
                case _ if command in commands_dict["unlock"]:
                    if self.player_position == self.exit_position: # Check if the player is at the exit
                        if inventory.has_item("key"): # Check if the player has the key
                            # TODO inventory.use_item to remove key from inventory
                            typewriter("You unlock the door and escape!", 0.05)
                            print(' ')
                            if self.play_again():
                                self.reset_game()
                                continue
                            else:
                                typewriter("Thank you for playing!", 0.05)
                                break
                        else:
                            typewriter("The door is locked. You need the \033[93mkey\033[0m to open it.", 0.05)
                    else:
                        typewriter("There is nothing to unlock here.", 0.05)

                # # re-enable after the commands hints are re-written
                # case _ if command in commands_dict["help"]:
                #     self.display_commands()
                #     monster_should_move = False

                case _ if command in commands_dict["debug"]:
                    print(' ')
                    self.debug()
                    monster_should_move = False

                case _:
                    typewriter(f'I don\'t know what "{command}" means.', 0.05)
                    monster_should_move = False

            if monster_should_move:
                self.monster.move(self.player_position)
                if self.monster.check_if_caught(self.player_position):
                    print(' ')
                    typewriter(f'\033[91mYou were caught by the monster!\33[0m', 0.05)
                    print(' ')
                    if self.play_again():
                        self.reset_game()
                        continue
                    else:
                        typewriter('Thank you for playing!', 0.05)
                        break

        print(' ')
        typewriter("GAME OVER", 0.5)

# Run the game if this script is executed
if __name__ == '__main__':
    game = Game()
    game.run()