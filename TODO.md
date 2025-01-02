### Todo
- [ ] Find alternate solution to typewriter function with tkinter
- [ ] Find alternate solution to text colorization with tkinter
- [ ] Allow the player to change the text size and window? Scaling?
- [ ] See [text-based-adventure/TODO.md](https://github.com/frankiebry/text-based-adventure/blob/main/TODO.md) for tasks not related to the tkinter adaption.

### Ideas for changes/improvements
- [ ] When monster attacks, it can do something else instead of end the game (lose metal detector, etc)
- [ ] Add roaming thief character?
- [ ] Add option to move 2 or 3 paces at once?
- [ ] Add combat and HP (change "caught" to "encounter")
- [ ] Make monster repellent cause the monster to stop chasing you for X amount of turns
- [ ] Add high score file using JSON and count score with gems at the end of each game
- [ ] Monster heads straight to the player's last known location when a torch is lit, unless it's 2 paces away.
- [ ] Add additional commands that display text but do nothing (e.g. "bang on door" -> "there is no response")
- [ ] Warning message when monster is near should not repeat, it should say something different to indicate the monster is chasing you.
- [ ] The "What do you want to do?: " line is very repetitive
- [ ] Convert this entire game into a graphical version

### Bugs/Issues
- [ ] The alt codes for the icons on the map are different sizes and make the map look wonky. Find a set that are all the same dimensions
- [ ] Metal detector doesn't seem to work properly sometimes. I'll be standing one tile next to the treasure and it's silent? But other playthroughs it works perfectly...
- [ ] The player, monster and treasure can stack, and the last icon that is drawn on the map will cover any icon drawn before it.
- [ ] Apparently if ANSI escape codes that set the text color explicitly are not reset with \033[0m, the terminal will continue applying the color to subsequent text, even after the program exits. The terminal has to be closed to fix this.
- [ ] The typewriter "stutters" when printing color text

### Cleaner Code
- [ ] All strings should use '' instead of ""? Or at least just be consistent
- [ ] Comment everything that doesn't have a clear purpose or needs to be explained?
- [ ] Find a more elegant solution to the following ~

Also this code block is used twice...
```Python
# Ask if the player wants to play again
if play_again():
    reset_game()  # Reset the game state
    continue  # Restart the game loop
else:
    typewriter("Thank you for playing!", 0.05)
    break
```