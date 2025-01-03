### Todo
- [ ] I split the main class into two classes: Game to handle the game logic, and GUI to handle the Tkinter elements, however other classes still need to access Game to use GUI's methods. The game is run through GUI. Is it possible to completely separate it?
- [ ] Find alternate solution to typewriter function with tkinter
- [ ] Find alternate solution to text colorization with tkinter
- [ ] Allow the player to change the text size and window? Scaling?
- [ ] See [text-based-adventure/TODO.md](https://github.com/frankiebry/text-based-adventure/blob/main/TODO.md) for tasks not related to the tkinter adaption.

### Ideas for changes/improvements
- [ ] Find a better theme than darkly? Or more stlying options to fit the dungeon crawler / rpg theme
- [ ] Create a widget for the map to be displayed in
- [ ] Create directional buttons and bind to arrow keys

### Bugs/Issues
- [ ]

### Cleaner Code
- [ ] Currently passing the game class into the monster class so the monster class can display messages. Change this so that messages are handled in game (the way you did with the inventory class) or create a new separate class for messages.
- [ ] Reorganize functions into a logical order