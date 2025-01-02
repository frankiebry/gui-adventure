import random
from typewriter import typewriter

class Inventory:
    def __init__(self):
        """Initialize the player's inventory with default items."""
        self.reset()

    def reset(self):
        """Reset the inventory to its default state."""
        self.items = {
            "torch": 3,  # Start with 3 torches
            "key": 0,    # Start with no key
            "monster repellent": 1, # Start with one monster repellent
            "shovel": 1, # Start with a shovel (make this a key item?)
            "map": 1,    # Start with a map (make this a key item?)
            "metal detector": 1, # Start with a metal detector
        }

    def add_item(self, item, count=1):
        """Add an item to the inventory."""
        if item in self.items:
            self.items[item] += count
        else:
            self.items[item] = count

    def find_random_item(self):
        """Roll virtual dice and add items to player inventory based on luck."""
        roll = random.randint(1, 20)  # Simulate a D20 roll (integer between 1 and 20)
    
        if 1 <= roll <= 5:  # Nothing: 25% chance
            typewriter("There is nothing here.", 0.05)
        elif 6 <= roll <= 10: # Torch: 25% chance
            self.add_item("torch", 1)
            typewriter("You found a torch!", 0.05)
        elif 11 <= roll <= 15:  # Monster Repellent: 25% chance
            self.add_item("monster repellent", 1)
            typewriter("You found some \033[95mmonster repellent\033[0m!", 0.05)
        elif 16 <= roll <= 17:  # Ruby: 7.5% chance
            self.add_item("ruby", 1)
            typewriter("You found a \033[91mruby\033[0m!", 0.05)
        elif 18 <= roll <= 19:  # Emerald: 7.5% chance
            self.add_item("emerald", 1)
            typewriter("You found an \033[92memerald\033[0m!", 0.05)
        elif roll == 20:  # Diamond: 5% chance
            self.add_item("diamond", 1)
            typewriter("You found a \033[96mdiamond\033[0m!", 0.05)

    def use_item(self, item):
        """Use an item from the inventory, if available."""
        if self.items.get(item, 0) > 0: # Second argument is the default value if item is not found
            self.items[item] -= 1

    def has_item(self, item):
        """Check if the player has a specific item."""
        return self.items.get(item, 0) > 0

    # TODO Pluralize item names if the quantity is greater than 1
    def show_inventory(self):
        """Display the contents of the player's inventory."""
        if not self.items:
            print("Your inventory is empty.")
        else:
            print("You check the contents of your backpack...")
            for item, quantity in self.items.items():
                print(f"- {item.capitalize()}: {quantity}")
    
# Create a single instance of the Inventory class
inventory = Inventory()