import random

class Inventory:
    def __init__(self):
        """Initialize the player's inventory with default items."""
        self.reset()

    def reset(self):
        """Reset the inventory to its default state."""
        self.items = {
            "map": 1,    # Start with a map (make this a key item?)
            "metal detector": 1, # Start with a metal detector
            "monster repellent": 1, # Start with one monster repellent
            "shovel": 1, # Start with a shovel (make this a key item?)
            "torch": 3,  # Start with 3 torches
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
            return "There is nothing here."
        elif 6 <= roll <= 10: # Torch: 25% chance
            self.add_item("torch", 1)
            return "You found a torch!"
        elif 11 <= roll <= 15:  # Monster Repellent: 25% chance
            self.add_item("monster repellent", 1)
            return "You found some monster repellent!"
        elif 16 <= roll <= 17:  # Ruby: 7.5% chance
            self.add_item("ruby", 1)
            return "You found a ruby"
        elif 18 <= roll <= 19:  # Emerald: 7.5% chance
            self.add_item("emerald", 1)
            return "You found an emerald!"
        elif roll == 20:  # Diamond: 5% chance
            self.add_item("diamond", 1)
            return "You found a diamond!"

    def use_item(self, item):
        """Use an item from the inventory, if available."""
        if self.items.get(item, 0) > 0: # Second argument is the default value if item is not found
            self.items[item] -= 1

    def has_item(self, item):
        """Check if the player has a specific item."""
        return self.items.get(item, 0) > 0

    # TODO Pluralize item names if the quantity is greater than 1
    def show_inventory(self):
        """Return messages representing the player's inventory."""
        if not self.items:
            return ["Your inventory is empty."]
        else:
            messages = ["You check the contents of your backpack..."]
            for item, count in self.items.items(): # rename the "items" dict to "backpack" or something, this is confusing
                messages.append(f"{item}: {count}")
            return messages
    
# Create a single instance of the Inventory class
inventory = Inventory()