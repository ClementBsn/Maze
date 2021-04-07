import random

from Game.Player import Player
from Configuration.results import *

class Game():
	"""
	Class Game is the class that plays the game
	The rules of each rooms are defined here
	"""

	def __init__(self, maze):
		"""
		Constructor of the class Game with arguments:
	 		- the maze, by loading it from its filename
			- the palyer that starts at position 0,0
		"""
		self.maze = maze 					# the maze
		x, y = self.maze.start_position		# the start position to set the player
		self.player = Player(x, y)			# the class of the player

	def play_a_game(self, policy = None):
		"""
		Function that plays a game
		"""
		print("Welcome to the Maze\n\nthe moves are:\nz = UP\nq = LEFT\ns = DOWN\nd = RIGHT\n\n")
		next_x = None
		next_y = None

		# boolean to know when the game ends
		continue_game = True

		print(self.maze.print_maze(self.player.x, self.player.y))

		### if a policy is selected, show the action
		if (policy):
			temp_c = str(self.player.x * self.maze.columns + self.player.y)
			temp_k = str(int(self.player.key))
			temp_t = str(int(self.player.treasure))
			temp_s = str(int(self.player.sword))
			current_state = "(" + temp_c + " " + temp_k + " " + temp_t + " " + temp_s + ")"
			# print(current_state)
			print("policy: " + policy[current_state])

		# while the game continues
		while(continue_game):
			# play a move
			continue_game, res, next_x, next_y = self.play_a_move(next_x, next_y)
			print("\n#############################\n")
			print(self.maze.print_maze(self.player.x, self.player.y))

			### if a policy is selected, show the action
			if (policy):
				temp_c = str(self.player.x * self.maze.columns + self.player.y)
				temp_k = str(int(self.player.key))
				temp_t = str(int(self.player.treasure))
				temp_s = str(int(self.player.sword))
				current_state = "(" + temp_c + " " + temp_k + " " + temp_t + " " + temp_s + ")"
				# print(current_state)
				print("policy: " + policy[current_state])

		# print the result
		if(res == "loose"):
			print("\n#######################\n# YOU DEAD, YOU LOOSE #\n#######################\n")
		else:
			print("\n#############\n# YOU WON ! #\n#############\n")


	def play_a_move(self, next_x, next_y):
		"""
		Function that plays a move in the game
		"""
		print(self.player)
		if(next_x == None or next_y == None):
			# get the next move of the player
			x, y = self.player.get_next_move()
			while(self.maze.in_maze(x, y, 0, 0) == False):
				print("WRONG MOVE")
				x, y = self.player.get_next_move()
			# the player get into a new room, we load the consequences of this room
			result = self.maze.get_consequence_move(self.player, x, y, show=True)
			# process the consequences of the new room
			return self.process_consequence(result, x, y)

		result = self.maze.get_consequence_move(self.player, next_x, next_y, show=True)
		# process the consequences of the new room
		return self.process_consequence(result, next_x, next_y)

	def process_consequence(self, result, x, y):
		"""
		Function that process the consequences of a room when the player get into it
		"""
		# switch case between all the consequences listed in results.py
		self.player.set_position(x, y)

		# if nothing happen
		if result == CONTINUE:
			# the game continue
			return True, "", None, None

		# if the player die
		if result == DIE:
			# the game ends with the player loosing the game
			return False, "loose", None, None

		# if the player move into a magical portal
		if result == PORTAL_MOVE:
			# the player is directly moved in a neighbor room at the next step
			new_x, new_y = self.maze.portal_movement(x, y)
			return True, "", new_x, new_y

		# if the player move into a platform
		if result == PLATFORM_MOVE:
			# the player is directly moved in a neighbor room at the next step
			new_x, new_y = self.maze.platform_movement(x, y)
			return True, "", new_x, new_y

		# if the player is in the room where there is the key
		if result == GAIN_KEY:
			# he gets the key
			self.player.gain_key()
			return True, "", None, None

		# if the player is in the room with the sword
		if result == GAIN_SWORD:
			# he gets the sword
			self.player.gain_sword()
			return True, "", None, None

		# if the player is in the room with the treasure
		if result == GAIN_TREASURE:
			# he gets the treasure
			self.player.gain_treasure()
			return True, "", None, None

		# if the player must go to start position
		if result == MOVE_TO_START:
			if(self.player.has_treasure()):
				new_x, new_y = self.maze.start_position
				self.player.set_position(new_x, new_y)
				return False, "win", None, None
			new_x, new_y = self.maze.start_position
			self.player.set_position(new_x, new_y)
			return True, "", None, None

		# if the player wins
		if result == WIN_MAZE:
			return False, "win", None, None
