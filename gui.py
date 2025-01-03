# gui.py
import tkinter as tk
import ttkbootstrap as ttk
import style

class GUI:
    def __init__(self, window):
        """
        Initialize the GUI and connect it to the Game class.
        Args:
            window (ttk.Window): The root Tkinter window.
        """
        self.window = window
        self.window.title("GUI Adventure")
        self.window.geometry("1020x600")

        self.message_box = tk.Text(window, height=20, width=60, font=style.game_font, state=tk.DISABLED, wrap=tk.WORD)
        self.message_box.pack(pady=(20, 10))

        self.command_frame = ttk.Frame(master=window)
        self.command_frame.pack(pady=10)

        self.commands_label = ttk.Label(master=self.command_frame, text='Type your commands here:', font=style.game_font)
        self.commands_label.pack(side='left', pady=10)

        self.input_box = tk.Entry(master=self.command_frame, width=35, font=style.game_font)
        self.input_box.pack(side='left', pady=10)
        self.input_box.bind("<Return>", self.handle_input)

        from game import Game
        self.game = Game(self)  # Connect to the game class

    def display_message(self, message):
        self.message_box.config(state=tk.NORMAL)
        self.message_box.insert(tk.END, message + "\n")
        self.message_box.config(state=tk.DISABLED)
        self.message_box.see(tk.END)

    def handle_input(self, event):
        player_input = self.input_box.get().strip()
        self.input_box.delete(0, tk.END)
        self.game.run(player_input)

    def quit(self):
        self.window.quit()