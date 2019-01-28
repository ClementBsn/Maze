from Configuration.results import DIE
from Maze.cells.Cell import Cell

class Cracks(Cell):
    """
    Description of a cell that is a cracks
    If the player go into this cell, he dies
    """

    def __init__(self, x, y, type, id):
        """ Constructor """
        Cell.__init__(self, x, y, type, id, "C")

    def process(self, player):
        """
        Function that process the action of the cell
        when the player go into it
        """
        return DIE
