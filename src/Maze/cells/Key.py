from Configuration.results import CONTINUE, GAIN_KEY
from Maze.cells.Cell import Cell

class Key(Cell):
    """
    Description of a cell where there is the golden key
    If the player go into this cell, he collects the golden key
    with this key he can open the treasure
    """

    def __init__(self, x, y, type, id):
        """
        Constructor needs a type, coordinates in the maze
        and an id
        """
        Cell.__init__(self, x, y, type, id, "K")

    def process(self, player):
        """
        Function that process the action of the cell
        when the player go into it
        """
        if player.has_key():
            return CONTINUE
        return GAIN_KEY
