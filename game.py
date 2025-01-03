# game.py
import random
import tkinter as tk
from monster import Monster
from settings import settings
from utils import calculate_distance
from commands import commands_dict 
from inventory import inventory

class Game:
    def __init__(self, gui):
        # print(f"gui type: {type(gui)}")  # Check the type of gui
        # print(f"gui attributes: {dir(gui)}")  # List the attributes of gui
        
        """Initialize the game by resetting to default settings."""
        self.gui = gui
        self.reset_game() # Reset the game to its initial state with default settings
        self.awaiting_play_again = False  # Track if waiting for a play-again response

        # Display a welcome message
        self.gui.display_message("You find yourself in a dark cave...\n")

    def reset_game(self):
        """Reset the game to its initial state with default settings."""
        inventory.reset() # Reset player inventory to its default state
        settings.reset() # Reset the settings to their default values
        self.searched_positions = settings.DEFAULT_SEARCHED_POSITIONS
        self.player_position = settings.DEFAULT_PLAYER_POS
        self.key_position = settings.DEFAULT_KEY_POS
        self.exit_position = settings.DEFAULT_EXIT_POS
        self.monster = Monster(settings.DEFAULT_MONSTER_POS, self.gui)

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
            grid[y][x] = '⛝ '
        
        # Draw the player location on the map
        player_x, player_y = self.player_position
        grid[player_y][player_x] = '♙ '
        
        # Draw the monster location on the map
        monster_x, monster_y = self.monster.position
        grid[monster_y][monster_x] = '♞ '
        
        exit_x, exit_y = self.exit_position
        grid[exit_y][exit_x] = '⬕ '
        
        # Draw the key if cheat is used and key is still on the map
        if show_key and self.key_position:
            key_x, key_y = self.key_position
            grid[key_y][key_x] = '⚿ '
        return '\n'.join(''.join(row) for row in grid) # draw the map row by row into a single string and return

    # Figure out how to implement this function with multiple returns and nested if statement
    def light_torch(self):
        """Use a torch to reveal the map and display helpful information."""
        if inventory.has_item("torch"): # Check if the player has any torches left
            inventory.use_item("torch")  # Use one torch from inventory
            self.gui.display_message("You light a torch and check your map.")
            self.gui.display_message(' ')
            self.gui.display_message(self.draw_map()) # putting this here for now because the return statement comes after
            self.gui.display_message(' ')
            self.gui.display_message('♙ - You are here.')
            self.gui.display_message('⛝ - Spots where you\'ve already dug.')
            self.gui.display_message('♞ - The MONSTER.')
            self.gui.display_message('⬕ - The exit.')
    
            if inventory.items["torch"] == 1: # Handle singular vs. plural in the message.
                return f'The light has gone out. You have {inventory.items["torch"]} torch left'
            else:
                return f'The light has gone out. You have {inventory.items["torch"]} torches left'
        else:
            return "You don't have any torches left"

    def use_metal_detector(self):
        """Use the metal detector to get a hint about the key's location."""
        if inventory.has_item("metal detector"): # Check if the player has a metal detector:
            
            # Right now this code will always be executed, consider making the metal detector have limited uses
            # or make it a key item that is found from digging
            if self.key_position is None:
                return "The metal detector is silent."
            else:
                distance = calculate_distance(self.player_position, self.key_position)
                if distance == 0:
                    return "The metal detector is going wild!!"
                elif distance == 1:
                    return "The metal detector is beeping rapidly!"
                elif distance == 2:
                    return "The metal detector is slowly beeping."
                else:
                    return "The metal detector is silent."

    # Figure out how to handle multiple returns to display message
    def use_monster_repellent(self, monster):
        if inventory.has_item("monster repellent"):
            inventory.use_item("monster repellent")
            # Set the repellent effect on the monster
            monster.repellent_turns_left = 3
            self.gui.display_message('You used a monster repellent.')
            self.gui.display_message(' ')
            return 'You hear a disgruntled growl as the sound of heavy footfalls fade away.'
        else:
            return 'You don\'t have any monster repellent.'

    def dig(self):
        """Handle the player digging at their current position."""
        if self.player_position in self.searched_positions: # Check if the player has already dug here
            return "You have already dug here."
        else:
            self.searched_positions.append(self.player_position) # Mark the spot as searched
        
            if self.player_position == self.key_position: # Check if the player has found the key
                inventory.add_item("key", 1)  # Add the key to the inventory
                self.key_position = None  # Remove the key from the map
                return "You found the key!"
            else:
                # We call inventory.find_random_item() and it returns the result here for us to display
                return inventory.find_random_item()

    # Handle play again after return? Can anything happen after the return statement?
    def unlock_door(self):
        """Handle the unlock action."""
        if self.player_position == self.exit_position:  # Check if the player is at the exit
            if inventory.has_item("key"):  # Check if the player has the key
                inventory.use_item("key")  # Remove the key from inventory
                self.gui.display_message('You unlock the door and escape!')
                return self.play_again()  # Ask the player if they want to play again.
            else:
                return "The door is locked. You need the key to open it."
        else:
            return "There is nothing to unlock here."

    def move_player(self, direction):
        match direction:
            case "up":
                if self.player_position[1] > 0:
                    self.player_position = (self.player_position[0], self.player_position[1] - 1)
                    return "You move north."
                else:
                    return "The way is blocked."
            case "down":
                if self.player_position[1] < settings.GRID_HEIGHT - 1:
                    self.player_position = (self.player_position[0], self.player_position[1] + 1)
                    return "You move south."
                else:
                    return "The way is blocked."
            case "left":
                if self.player_position[0] > 0:
                    self.player_position = (self.player_position[0] - 1, self.player_position[1])
                    return "You move west."
                else:
                    return "The way is blocked."
            case "right":
                if self.player_position[0] < settings.GRID_WIDTH - 1:
                    self.player_position = (self.player_position[0] + 1, self.player_position[1])
                    return "You move east."
                else:
                    return "The way is blocked."

    def show_hints(self):
        """Display helpful hints to the player."""
        hints = [
            "Try checking your inventory.",
            "You could check your map, if you could see...",
            "The metal detector might help you find something.",
            "You can use torches to light your way.",
            "The monster doesn't like the smell of repellent.",
            "You can use the shovel to dig for treasure.",
            "You can use a key to unlock a door.",
            "You can move north, south, east, or west.",
        ]
        return random.choice(hints)
        
    def cheat(self):
        """Display inventory and the full map, including the key's location (cheat mode)."""
        # return display_message(' ')
        self.draw_map(show_key=True) # Show the key on the map
        inventory_messages = inventory.show_inventory()  # Get inventory messages
        for message in inventory_messages:
            return message  # Display each message
        return  ' '

    def play_again(self):
        """Ask the player if they want to play again."""
        self.awaiting_play_again = True  # Set the flag to indicate we're awaiting a response
        return "Do you want to play again? (Y/N)"

    def run(self, player_input):
        """Handle player input."""

        if not player_input:
            return

        self.gui.display_message(f"> {player_input}")

        # Check if we're awaiting a play-again response
        if self.awaiting_play_again:
            if player_input in ["y", "yes"]:
                self.awaiting_play_again = False  # Reset the flag
                self.reset_game()
                self.gui.message_box.config(state=tk.NORMAL)  # Enable editing of the message box
                self.gui.message_box.delete(1.0, tk.END)  # Clear all previous messages
                self.gui.message_box.config(state=tk.DISABLED)  # Disable editing again
                self.gui.display_message("You find yourself in a dark cave. Type your commands below.\n")
            elif player_input in ["n", "no"]:
                self.awaiting_play_again = False  # Reset the flag
                self.gui.display_message("Thank you for playing!")
                self.gui.window.quit()  # Exit the game
            else:
                self.gui.display_message("Please answer 'Y' or 'N'.")
            return

        # Window exits before message is displayed. Do I really want this part anyway?
        if player_input in commands_dict["quit"]:
            self.gui.display_message("Thanks for playing!")
            self.gui.window.quit()
            return

        # Process the command through the game logic
        monster_should_move = True

        match player_input:
            case _ if player_input in commands_dict["up"]:
                self.gui.display_message(self.move_player("up"))
            case _ if player_input in commands_dict["down"]:
                self.gui.display_message(self.move_player("down"))
            case _ if player_input in commands_dict["left"]:
                self.gui.display_message(self.move_player("left"))
            case _ if player_input in commands_dict["right"]:
                self.gui.display_message(self.move_player("right"))
            case _ if player_input in commands_dict["dig"]:
                self.gui.display_message(self.dig())
            case _ if player_input in commands_dict["torch"]:
                self.gui.display_message(self.light_torch())
            case _ if player_input in commands_dict["sweep"]:
                self.gui.display_message(self.use_metal_detector())
            case _ if player_input in commands_dict["repel"]:
                self.gui.display_message(self.use_monster_repellent(self.monster))
            case _ if player_input in commands_dict["inventory"]:
                inventory_messages = inventory.show_inventory()  # Get inventory messages
                for message in inventory_messages:
                    self.gui.display_message(message)  # Display each message
            case _ if player_input in commands_dict["unlock"]:
                self.gui.display_message(self.unlock_door())
            case _ if player_input in commands_dict["help"]:
                self.gui.display_message(self.show_hints())
            case _ if player_input in commands_dict["cheat"]:
                self.gui.display_message(self.cheat())
                monster_should_move = False
            case _:
                self.gui.display_message(f"I don't know what '{player_input}' means.")
                monster_should_move = False
        self.gui.display_message(' ') # print blank line after every command

        if monster_should_move:
            self.monster.move(self.player_position)
            if self.monster.check_if_caught(self.player_position):
                self.gui.display_message("You were caught by the monster!")
                self.gui.display_message(self.play_again())  # Ask the player if they want to play again
