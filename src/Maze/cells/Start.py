from Configuration.results import CONTINUE, WIN_MAZE
from Maze.cells.Cell import Cell

class Start(Cell):
    """
    Description of a cell that is the starting position of the maze
    If the player go into this cell with the treasure,
    he win and leave the maze
    """

    def __init__(self, x, y, type, id):
        """
        Constructor needs a type, coordinates in the maze
        and an id
        """
        Cell.__init__(self, x, y, type, id, "o")

    def process(self, player):
        """
        Function that process the action of the cell
        when the player go into it
        """
        if player.has_treasure():
            return WIN_MAZE
        return CONTINUE
