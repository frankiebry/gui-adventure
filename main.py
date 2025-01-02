import tkinter as tk
import ttkbootstrap as ttk
from monster import Monster
from settings import settings
from utils import calculate_distance
from commands import commands_dict 
from inventory import inventory

class Game:
    def __init__(self, root):
        """Initialize the game by resetting to default settings."""
        self.reset_game() # Reset the game to its initial state with default settings
        
        self.root = root
        self.root.title("Text Adventure")
        self.root.geometry("1020x768")  # Set the window size
        
        # Define a common font
        font = ("Terminal", 20)

        # Create the large text box for game messages
        self.message_box = tk.Text(root, height=20, width=60, font=font, state=tk.DISABLED, wrap=tk.WORD)
        self.message_box.pack(pady=10)

        # Create the smaller text box for player input
        self.input_box = tk.Entry(root, width=60, font=font)
        self.input_box.pack(pady=10)
        self.input_box.bind("<Return>", self.process_input)  # Bind the Enter key to process_input

        # Display a welcome message
        self.display_message("You find yourself in a dark cave. Type your commands below.\n")

    def reset_game(self):
        """Reset the game to its initial state with default settings."""
        inventory.reset() # Reset player inventory to its default state
        settings.reset() # Reset the settings to their default values
        self.searched_positions = settings.DEFAULT_SEARCHED_POSITIONS
        self.player_position = settings.DEFAULT_PLAYER_POS
        self.key_position = settings.DEFAULT_KEY_POS
        self.exit_position = settings.DEFAULT_EXIT_POS
        self.monster = Monster(settings.DEFAULT_MONSTER_POS, self)

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
        for row in grid: # draw the map row by row
            self.display_message(''.join(row))

    def light_torch(self):
        """Use a torch to reveal the map and display helpful information."""
        if inventory.has_item("torch"): # Check if the player has any torches left
            inventory.use_item("torch")  # Use one torch from inventory
            self.display_message("You light a torch and check your map.")
            self.display_message(' ')
            self.draw_map()
            self.display_message(' ')
            self.display_message("♙ - Your current location.")
            self.display_message("⛝ - Spots where you've already dug.")
            self.display_message("♞ - You see an ominous shadowy standing there.")
            self.display_message("⬕ - The exit is at this location.")
    
            if inventory.items["torch"] == 1: # Handle singular vs. plural in the message.
                self.display_message(f'The light has gone out. You have {inventory.items["torch"]} torch left')
            else:
                self.display_message(f'The light has gone out. You have {inventory.items["torch"]} torches left')
        else:
            self.display_message("You don't have any torches left")

    def use_metal_detector(self):
        """Use the metal detector to get a hint about the key's location."""
        if inventory.has_item("metal detector"): # Check if the player has a metal detector:
            
            # Right now this code will always be executed, consider making the metal detector have limited uses
            # or make it a key item that is found from digging
            if self.key_position is None:
                self.display_message("The metal detector is silent.")
            else:
                distance = calculate_distance(self.player_position, self.key_position)
                if distance == 0:
                    self.display_message("The metal detector is going wild!!")
                elif distance == 1:
                    self.display_message("The metal detector is beeping rapidly!")
                elif distance == 2:
                    self.display_message("The metal detector is slowly beeping.")
                else:
                    self.display_message("The metal detector is silent.")

    def use_monster_repellent(self, monster):
        if inventory.has_item("monster repellent"):
            inventory.use_item("monster repellent")
            # Set the repellent effect on the monster
            monster.repellent_turns_left = 3
            self.display_message("You used a monster repellent.")
            self.display_message("You hear a disgruntled growl as the sound of heavy footfalls fade away.")
        else:
            self.display_message("You don't have any monster repellent.")

    def dig(self):
        """Handle the player digging at their current position."""
        if self.player_position in self.searched_positions: # Check if the player has already dug here
            self.display_message("You have already dug here.")
        else:
            self.searched_positions.append(self.player_position) # Mark the spot as searched
        
            if self.player_position == self.key_position: # Check if the player has found the key
                inventory.add_item("key", 1)  # Add the key to the inventory
                self.key_position = None  # Remove the key from the map
                self.display_message("You found the key!")
                self.display_message(' ')
            else:
                # We call inventory.find_random_item() and it returns the result here for us to display
                self.display_message(inventory.find_random_item())

    def player_move(self, direction):
        match direction:
            case "up":
                if self.player_position[1] > 0:
                    self.player_position = (self.player_position[0], self.player_position[1] - 1)
                    self.display_message("You move north.")
                else:
                    self.display_message("The way is blocked.")
            case "down":
                if self.player_position[1] < settings.GRID_HEIGHT - 1:
                    self.player_position = (self.player_position[0], self.player_position[1] + 1)
                    self.display_message("You move south.")
                else:
                    self.display_message("The way is blocked.")
            case "left":
                if self.player_position[0] > 0:
                    self.player_position = (self.player_position[0] - 1, self.player_position[1])
                    self.display_message("You move west.")
                else:
                    self.display_message("The way is blocked.")
            case "right":
                if self.player_position[0] < settings.GRID_WIDTH - 1:
                    self.player_position = (self.player_position[0] + 1, self.player_position[1])
                    self.display_message("You move east.")
                else:
                    self.display_message("The way is blocked.")

    def debug(self):
        """Display the full map, including the key's location (cheat/debug mode)."""
        self.display_message(' ')
        self.draw_map(show_key=True) # Show the key on the map
        self.display_message(' ')

    def play_again(self):
        """Prompt the player to decide whether to play again."""
        player_input = input("Do you want to play again? (Y/N): ").strip().lower()
        return player_input in ["y", "yes"]

    def display_message(self, message):
        """Display a message in the message box."""
        self.message_box.config(state=tk.NORMAL)  # Enable editing
        self.message_box.insert(tk.END, message + "\n")  # Add the message
        self.message_box.config(state=tk.DISABLED)  # Disable editing
        self.message_box.see(tk.END)  # Scroll to the bottom

    def process_input(self, event): # Why is event needed?
        """Handle player input from the input box."""
        player_input = self.input_box.get().strip()
        self.input_box.delete(0, tk.END)  # Clear the input box

        if not player_input:
            return

        self.display_message(f"> {player_input}")

        if player_input in commands_dict["quit"]:
            self.display_message("Thanks for playing!")
            self.root.quit()
            return

        # Process the command through the game logic
        monster_should_move = True

        match player_input:
            case _ if player_input in commands_dict["up"]:
                self.player_move("up")
            case _ if player_input in commands_dict["down"]:
                self.player_move("down")
            case _ if player_input in commands_dict["left"]:
                self.player_move("left")
            case _ if player_input in commands_dict["right"]:
                self.player_move("right")
            case _ if player_input in commands_dict["dig"]:
                self.display_message("You dig where you are currently standing.")
                self.dig()
            case _ if player_input in commands_dict["torch"]:
                self.light_torch()
                self.display_message("You light a torch.")
            case _ if player_input in commands_dict["sweep"]:
                self.display_message("You use the metal detector.")
                self.use_metal_detector()
            case _ if player_input in commands_dict["repel"]:
                self.use_monster_repellent(self.monster)
            case _ if player_input in commands_dict["inventory"]:
                inventory_messages = inventory.show_inventory()  # Get inventory messages
                for message in inventory_messages:
                    self.display_message(message)  # Display each message
            case _ if player_input in commands_dict["debug"]:
                self.debug()
                self.display_message("Debug map revealed.")
                monster_should_move = False
            case _:
                self.display_message(f"I don't know what '{player_input}' means.")
                monster_should_move = False

        if monster_should_move:
            self.monster.move(self.player_position)
            if self.monster.check_if_caught(self.player_position):
                self.display_message("You were caught by the monster!")
                self.reset_game()
                self.display_message("Game reset.")


# Run the GUI
root = ttk.Window(themename='darkly')
game = Game(root)
root.mainloop()
