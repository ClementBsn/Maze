from Configuration.results import PORTAL_MOVE
from Maze.cells.Cell import Cell

class Portal(Cell):
    """
    Description of a cell that is a magic portal
    If the player go into this cell, he is teleported to another random cell
    (except wall)
    """

    def __init__(self, x, y, type, id):
        """
        Constructor needs a type, coordinates in the maze
        and an id
        """
        Cell.__init__(self, x, y, type, id, "P")

    def process(self, player):
        """
        Function that process the action of the cell
        when the player go into it
        """
        return PORTAL_MOVE
