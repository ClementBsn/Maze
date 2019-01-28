from Configuration.results import CONTINUE
from Maze.cells.Cell import Cell

class Empty(Cell):
    """
    An Empty Cell
    """

    def __init__(self, x, y, type, id):
        """ Constructor """
        Cell.__init__(self, x, y, type, id, "_")

    def process(self, player):
        """
        Function that process the action of the cell
        when the player go into it
        """
        return CONTINUE
