from Configuration.results import CONTINUE, GAIN_TREASURE
from Maze.cells.Cell import Cell

class Treasure(Cell):
    """
    Description of a cell where there is a treasure
    If the player go into this cell with the golden key,
    he can collect the treasure
    """

    def __init__(self, x, y, type, id):
        """
        Constructor needs a type, coordinates in the maze
        and an id
        """
        Cell.__init__(self, x, y, type, id, "T")

    def process(self, player):
        """
        Function that process the action of the cell
        when the player go into it
        """
        if player.has_key():
            if player.has_treasure():
                return CONTINUE
            return GAIN_TREASURE
        return CONTINUE
