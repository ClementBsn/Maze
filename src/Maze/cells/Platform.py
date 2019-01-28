from Configuration.results import PLATFORM_MOVE
from Maze.cells.Cell import Cell

class Platform(Cell):
    """
    Description of a cell that is a moving platform
    If the player go into this cell, the pavement is moving
    andd the player is forced to move to a another cell next to it
    at random
    """

    def __init__(self, x, y, type, id):
        """
        Constructor needs a type, coordinates in the maze
        and an id
        """
        Cell.__init__(self, x, y, type, id, "-")

    def process(self, player):
        """
        Function that process the action of the cell
        when the player go into it
        """
        return PLATFORM_MOVE
