from Configuration.results import CONTINUE, DIE, MOVE_TO_START
from Maze.cells.Cell import Cell
import random

class Trap(Cell):
    """
    Description of a cell where there is a trap
    If the player go into this cell, he has a chance to die,
    to return to the starting position or to continue
    """

    def __init__(self, x, y, type, id, p_die, p_restart):
        """
        Constructor needs a type, coordinates in the maze
        and an id
        """
        Cell.__init__(self, x, y, type, id, "R")
        self.p_die = p_die
        self.p_restart = p_restart

    def process(self, player):
        """
        Function that process the action of the cell
        when the player go into it
        """
        r = random.random()
        if r < self.p_die:
            return DIE
        if r < self.p_restart:
            return MOVE_TO_START
        return CONTINUE
