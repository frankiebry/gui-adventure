# TODO strip "?" from possible commands

commands_dict = {
    "up": [
        "go north", "move north", "go up", "move up"
    ],
    "down": [
        "go south", "move south", "go down", "move down"
    ],
    "right": [
        "go east", "move east", "go right", "move right"
    ],
    "left": [
        "go west", "move west", "go left", "move left"
    ],
    "dig": [
        "dig", "dig for treasure", "dig here", "look for treasure", 
        "look for treasure here", "search", "search here", "search for treasure",
        "use shovel", "use shovel here", "use my shovel", "use my shovel here",
        "use the shovel", "use the shovel here", "use the shovel to dig",
    ],
    "inventory": [
        "check inventory", "show inventory", "view inventory", "view my inventory",
        "what do i have", "what do i have?", "what's in my inventory", "what's in my inventory?"
        "check my items", "check my items?", "check items", "check items?"
    ],
    "torch": [
        "light torch", "light a torch", "use torch", "use a torch", "look around", "light my torch",
        "where am i?", "where am i", "i don't know where i am", "check map", 
        "check my map", "look at map", "look at my map", "use map", "use my map"
    ],
    "sweep": [
        "sweep", "sweep for treasure", "sweep here", "sweep for treasure here", 
        "use metal detector", "use metal detector here", "use detector", "use my metal detector",
        "use detector here", "use the metal detector", "use the metal detector here", 
        "detect treasure", "check if treasure is near", "check if treasure is near here", 
        "check for treasure", "check for treasure here", "check for treasure nearby", 
        "check if the treasure is near"
    ],
    "repel": [
        "use monster repellent", "use repellent", "use repellent here", "use monster repellent here",
        "use my monster repellent", "use my repellent", "use my repellent here", "use my monster repellent here",
        "use a monster repellent", "use a repellent", "use a repellent here", "use a monster repellent here",
        "use the monster repellent", "use the repellent", "use the repellent here", "use the monster repellent here",
        "spray repellent", "spray monster repellent", "spray repellent here", "spray monster repellent here",
    ],
    "unlock": [
        "unlock the door", "open the door", "use the key", "use key",
        "unlock door", "open door", "use key here", "use the key here",
        "unlock the door here", "open the door here", "open the exit",
        "unlock the exit", "use the key on the door", "use the key on the exit",
    ],
    "help": [
        "help", "commands", "options", "i don't know what to do", "what can i do", 
        "what can i do?", "what do i do", "what do i do?"
    ],
    "debug": [
        "cheat", "debug"
    ]
}