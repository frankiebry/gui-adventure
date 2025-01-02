def calculate_distance(pos1, pos2):
    """
    Calculate the Manhattan distance between two positions.
    This function is used by both the game class and the monster class.

    Args:
        pos1 (tuple): The (x, y) coordinates of the first position.
        pos2 (tuple): The (x, y) coordinates of the second position.

    Returns:
        int: The Manhattan distance between the two positions.
    """
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])