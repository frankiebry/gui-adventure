import tkinter as tk
import ttkbootstrap as ttk
from monster import Monster
from typewriter import typewriter
from settings import settings
from utils import calculate_distance
from commands import commands_dict 
from inventory import inventory

class Game:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Text-Based Game")

        # Create the large text box for game messages
        self.message_box = tk.Text(root, height=20, width=50, state=tk.DISABLED, wrap=tk.WORD)
        self.message_box.pack(pady=10)

        # Create the smaller text box for player input
        self.input_box = tk.Entry(root, width=50)
        self.input_box.pack(pady=10)
        self.input_box.bind("<Return>", self.process_input)  # Bind the Enter key to process_input

        # Display a welcome message
        self.display_message("Welcome to the game! Type your commands below.\n")

    def display_message(self, message):
        """Display a message in the message box."""
        self.message_box.config(state=tk.NORMAL)  # Enable editing
        self.message_box.insert(tk.END, message + "\n")  # Add the message
        self.message_box.config(state=tk.DISABLED)  # Disable editing
        # self.message_box.see(tk.END)  # Scroll to the bottom

    def process_input(self, event):
        """Handle player input from the input box."""
        player_input = self.input_box.get().strip()
        self.input_box.delete(0, tk.END)  # Clear the input box

        if not player_input:
            return

        # Display the player's command
        # self.display_message(f"You typed: {player_input}")

        # Example game logic
        if player_input.lower() in ["look", "search"]:
            self.display_message("You look around and see nothing but darkness.")
        elif player_input.lower() in ["help"]:
            self.display_message("Available commands: look, search, quit")
        elif player_input.lower() in ["quit", "exit"]:
            self.display_message("Thanks for playing!")
            self.root.quit()  # Close the game
        else:
            self.display_message(f"I don't understand '{player_input}'.")


# Run the GUI
root = ttk.Window(themename= 'darkly')
game = Game(root)
root.mainloop()
