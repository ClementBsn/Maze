from Configuration.results import MOVE_TO_START
from Maze.cells.Cell import Cell

class Wall(Cell):
    """
    Description of a cell that is a wall
    If the player go into a wall, he returns to the starting position
    """

    def __init__(self, x, y, type, id):
        """
        Constructor needs a type, coordinates in the maze
        and an id
        """
        Cell.__init__(self, x, y, type, id, "#")

    def process(self, player):
        """
        Function that process the action of the cell
        when the player go into it
        """
        return MOVE_TO_START
