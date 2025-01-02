import sys
import time

def typewriter(message, speed):
    """
    Simulates typing out a message one character at a time with a specified speed.
    The intent is to create immersion and a sense of anticipation for the player.

    Args:
    message (str): The message to be typed out.
    speed (float): The delay (in seconds) between each character.

    The function outputs the message one character at a time, with a delay between each character to create a typewriter effect.
    If the character is a newline, it waits longer before continuing to the next line.
    """
    
    for char in message:
        # Write each character to the screen immediately without buffering
        sys.stdout.write(char)
        sys.stdout.flush() # Ensure the character is displayed immediately

        # Introduce a delay based on the character type
        if char != "\n":
            time.sleep(speed) # Normal delay for characters
        else:
            time.sleep(1) # Longer delay after a newline (to simulate a pause)
            
    sys.stdout.write("\n") # Ensure the final newline is printed after the message
    sys.stdout.flush() # Flush the final newline, forcing the output to be shown right away without buffering