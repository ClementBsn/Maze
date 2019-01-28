from Configuration.results import CONTINUE, DIE
from Maze.cells.Cell import Cell
import random

class Enemy(Cell):
	"""
	A Cell with an ennemy
	"""

	def __init__(self, x, y, type, id, p_enemy):
		""" Constructor """
		Cell.__init__(self, x, y, type, id, "E")
		self.p_enemy = p_enemy

	def process(self, player):
		"""
		Function that process the action of the cell
		when the player go into it
		"""
		if player.has_sword():
			return CONTINUE
		r = random.random()
		if r < self.p_enemy:
			return CONTINUE
		return DIE
