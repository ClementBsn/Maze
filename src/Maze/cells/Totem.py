from Configuration.results import CONTINUE, GAIN_TOTEM
from Maze.cells.Cell import Cell

class Totem(Cell):
    """
    Description of a cell where there is a magic sword
    If the player go into this cell, he collects the magic sword
    with this sword, he defeats all ennemies
    """

    def __init__(self, x, y, type, id):
        """
        Constructor needs a type, coordinates in the maze
        and an id
        """
        Cell.__init__(self, x, y, type, id, "S")

    def process(self, player):
        """
        Function that process the action of the cell
        when the player go into it
        """
        if player.has_sword():
            return CONTINUE
        return GAIN_SWORD
