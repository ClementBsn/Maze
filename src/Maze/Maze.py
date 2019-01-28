from Maze.cells import Cracks, Empty, Enemy, Key, Platform, Portal, Start, Sword, Trap, Treasure, Wall
from Configuration.types import *
from Configuration.config import CONFIG
import random
import re

class Maze():
	"""
	Class of the maze
	"""

	def __init__(self):
		self.lines = 0						# number of lines
		self.columns = 0					# number of columns
		self.maze = None					# the matrix of the cells of the maze
		self.start_position = (0,0)			# the coordinates of the start cell
		self.key_position = (0,0)			# the coordinates of the start cell
		self.treasure_position = (0,0)		# the coordinates of the start cell
		self.sword_position = (0,0)			# the coordinates of the start cell

	def load_maze(self, filename):
		"""
		Function that loads a maze from a file
		"""
		i = 0
		self.maze = list()
		id = 0
		f = open(filename, 'r')
		for l in f:
			line = list()
			for j in range(len(l)):
				if l[j] != '\n':
					line.append(self.convert(l[j], i, j, id))
					id += 1
			self.maze.append(line)
			i += 1

		self.columns = len(self.maze[0])
		self.lines = len(self.maze)

		f.close()

	def save_maze(self, filename):
		"""
		Function that saves a maze as a file given the name
		"""
		f = open(filename, 'w')
		m = ""
		for i in range(self.lines):
			for j in range(self.columns):
				m += self.maze[i][j].symbole
			m += "\n"

		f.write(m)
		f.close()

	def init_random_maze(self, nb_lines, nb_columns, filename):
		"""
		Function that initialize class Maze with a randomly generated maze of size nb_lines*nb_columns
		with a checking of its feasability and then save it at filename
		"""
		self.lines = nb_lines
		self.columns = nb_columns

		while(True):
			new_maze = self.generate_maze(nb_lines, nb_columns)
			if(self.is_winnable(new_maze)):
				break

		self.maze = self.convert_maze(new_maze)
		self.save_maze(filename)

	def generate_maze(self, nb_lines, nb_columns):
		"""
		Function that creates a new maze given the number of lines and columns
		"""
		new_maze = list()
		free_cells = list()
		# initialize maze with empty cells
		for i in range(nb_lines):
			l = list()
			for j in range(nb_columns):
				l.append("_")
				free_cells.append((i,j))
			new_maze.append(l)

		# put treasure on left-up corner of the maze
		new_maze[0][0] = "T"
		free_cells.remove((0,0))
		self.treasure_position = (0,0)

		# put start position on right-down corner of the maze
		new_maze[nb_lines-1][nb_columns-1] = "o"
		free_cells.remove((nb_lines-1,nb_columns-1))
		self.start_position = (nb_lines-1,nb_columns-1)

		# put sword and the key randomly in the maze
		for c in ["S", "K"]:
			while(True):
				x = int(random.random() * nb_lines)
				y = int(random.random() * nb_columns)
				if((x,y) in free_cells):
					break
			new_maze[x][y] = c
			if(c == "S"):
				self.sword_position = (x,y)
			else:
				self.key_position = (x,y)
			free_cells.remove((x,y))

		"""
		# put 23% of walls, put 8% of enemies, put 11% of traps
		# put 5% of cracks, put 5% of portal and put 13% of platform
		t = nb_lines * nb_columns
		for c, p in [("#", int(0.23*t)), ("E", int(0.08*t)), ("R", int(0.11*t)), ("C", int(0.05*t)), ("P", int(0.05*t)), ("-", int(0.13*t))]:
			for k in range(p):
				while(True):
					x = int(random.random() * nb_lines)
					y = int(random.random() * nb_columns)
					if((x,y) in free_cells):
						break
				new_maze[x][y] = c
				free_cells.remove((x,y))
		"""

		# for every cell, select a random type
		for i,j in free_cells:
			r = random.random()
			if(r >= 0.75):
				new_maze[i][j] = '#'
				continue
			if(r >= 0.70):
				new_maze[i][j] = 'C'
				continue
			if(r >= 0.65):
				new_maze[i][j] = 'P'
				continue
			if(r >= 0.55):
				new_maze[i][j] = 'E'
				continue
			if(r >= 0.43):
				new_maze[i][j] = 'R'
				continue
			if(r >= 0.30):
				new_maze[i][j] = '-'
				continue

		return new_maze

	def is_winnable(self, maze):
		"""
		Return true if it is possible to win the maze, returns false if not
		"""
		x, y = self.start_position
		n = self.get_neighbors(x, y)
		for i,j in n:
			if(maze[i][j] == 'C' or maze[i][j] == '#'):
				n.remove([i,j])
		if(not(self.to_key(maze, [(x,y)], n))):
			return False

		x, y = self.key_position
		n = self.get_neighbors(x, y)
		for i,j in n:
			if(maze[i][j] == "C" or maze[i][j] == "#"):
				n.remove([i,j])
		if(not(self.to_treasure(maze, [(x,y)], n))):
			return False

		x, y = self.treasure_position
		n = self.get_neighbors(x, y)
		for i,j in n:
			if(maze[i][j] == "C"):
				n.remove([i,j])
		return self.to_start(maze, [(x,y)], n)

	def to_key(self, maze, seen, last_add):
		"""
		Returns True if there is a way from the start to the key
		"""
		add = list()
		for x, y in last_add:
			n = self.get_neighbors(x, y)
			for i,j in n:
				if(maze[i][j] == "K"):
					return True
				if(not((i,j) in seen+last_add+add)):
					if(maze[i][j] != "C" and maze[i][j] != "#"):
						add.append((i,j))
		if(add == list()):
			return False
		return self.to_key(maze, seen+last_add, add)

	def to_treasure(self, maze, seen, last_add):
		"""
		Returns True if there is a way from the key to the start
		"""
		add = list()
		for x, y in last_add:
			n = self.get_neighbors(x, y)
			for i,j in n:
				if(maze[i][j] == "T"):
					return True
				if(not((i,j) in seen+last_add+add)):
					if(maze[i][j] != "C" and maze[i][j] != "#"):
						add.append((i,j))
		if(add == list()):
			return False
		return self.to_treasure(maze, seen+last_add, add)

	def to_start(self, maze, seen, last_add):
		"""
		Returns True if there is a way from the treasure to the start
		"""
		add = list()
		for x, y in last_add:
			n = self.get_neighbors(x, y)
			for i,j in n:
				if(maze[i][j] == "o" or maze[i][j] == "#"):
					return True
				if(not((i,j) in seen+last_add+add)):
					if(maze[i][j] != "C"):
						add.append((i,j))
		if(add == list()):
			return False
		return self.to_start(maze, seen+last_add, add)

	def convert_maze(self, new_maze):
		"""
		Function that converts a matrix of char into a matrix of Cell
		"""
		m = list()
		id = 0
		for i in range(self.lines):
			l = list()
			for j in range(self.columns):
				l.append(self.convert(new_maze[i][j], i, j, id))
			m.append(l)
			id += 1

		return m

	def print_maze(self, x = 0, y = 0):
		"""
		Function to display the maze on the terminal and
		show the player at position $
		"""
		alphabet = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
		m = "  "
		for j in range(self.columns):
			m += alphabet[j]
		m += "\n +"
		for j in range(self.columns):
			m += "-"
		m += "+\n"
		for i in range(self.lines):
			m += str(alphabet[i])+"|"
			for j in range(self.columns):
				if((i,j) == (x,y)):
					m += "$"
				else:
					m += self.maze[i][j].symbole
			m += "|\n"

		m += " +"
		for j in range(self.columns):
			m += "-"
		m += "+"
		m = re.sub(r"[_]", ' ', m)
		return m

	def convert(self, c, x, y, id):
		"""
		Return the class of the room at (x, y) represented by the char c
		"""
		if c == 'o':
			self.start_position = (x, y)
			return Start.Start(x, y, START, id)
		if c == '_':
			return Empty.Empty(x, y, EMPTY, id)
		if c == '#':
			return Wall.Wall(x, y, WALL, id)
		if c == 'E':
			return Enemy.Enemy(x, y, ENEMY, id, CONFIG["enemy"]["p_enemy"])
		if c == 'R':
			return Trap.Trap(x, y, TRAP, id, CONFIG["trap"]["p_die"], CONFIG["trap"]["p_restart"])
		if c == 'C':
			return Cracks.Cracks(x, y, CRACKS, id)
		if c == 'T':
			self.treasure_position = (x, y)
			return Treasure.Treasure(x, y, TREASURE, id)
		if c == 'S':
			self.sword_position = (x, y)
			return Sword.Sword(x, y, SWORD, id)
		if c == 'K':
			self.key_position = (x, y)
			return Key.Key(x, y, KEY, id)
		if c == 'P':
			return Portal.Portal(x, y, PORTAL, id)
		if c == '-':
			return Platform.Platform(x, y, PLATFORM, id)

	def get_consequence_move(self, player, x, y, show=False):
		"""
		Process the room and return the consequence of the room
		"""
		if(show):
			print("Moving to "+ str(self.maze[x][y]))
		return self.maze[x][y].process(player)

	def get_neighbors(self, x, y):
		"""
		Return the coordinates of the 4 cells around the room at (x,y)
		if they are in the maze
		"""
		l = list()
		for i, j in [[-1, 0], [1, 0], [0, -1], [0, 1]]:
			if(self.in_maze(x, y, i, j)):
				l.append([x+i, y+j])
		return l

	def get_neighbors_with_directions(self, x, y):
		"""
		Return the coordinates of the 4 cells around the room at (x,y)
		if they are in the maze with the direction to go into from (x,y)
		"""
		l = list()
		for i, j, dir in [[-1, 0, 'UP'], [1, 0, 'DOWN'], [0, -1, 'LEFT'], [0, 1, 'RIGHT']]:
			if(self.in_maze(x, y, i, j)):
				l.append([(x+i, y+j), dir])
		return l

	def get_cells_not_walls(self, x, y):
		"""
		Returns the coordinates of all the rooms except the walls
		"""
		l = list()
		for i in range(self.lines):
			for j in range(self.columns):
				if(self.maze[i][j].type != WALL):
					l.append([i, j])
		return l

	def in_maze(self, x, y, i, j):
		"""
		Return true if the cell (x+i, y+j) is in the maze and Returns
		false if not
		"""
		if(x+i >= 0 and x+i < self.lines and y+j >= 0 and y+j < self.columns):
			return True
		return False

	def portal_movement(self, x, y):
		"""
		Returns the new coordinates of the player after enter in a magical portal
		"""
		cells = self.get_cells_not_walls(x, y)
		new_x, new_y = cells[random.randint(0, len(cells) - 1)]
		return new_x, new_y

	def platform_movement(self, x, y):
		"""
		Returns the new coordinates of the player after enter in a platform
		"""
		neighbors = self.get_neighbors(x, y)
		new_x, new_y = neighbors[random.randint(0, len(neighbors) - 1)]
		return new_x, new_y
