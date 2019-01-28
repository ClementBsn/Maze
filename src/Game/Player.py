class Player():
	"""
	Class Player that defines the player of the maze
	with its coordinates x, y in the maze
	three booleans that equal True if it has the key, sword or the treasure
	"""

	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.key = False
		self.sword = False
		self.treasure = False

	def __str__(self):
		alphabet = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
		c = "Player at ("+str(alphabet[self.x])+", "+str(alphabet[self.y])+")"
		if(self.has_key()):
			c += ", key"
		if(self.has_sword()):
			c += ", sword"
		if(self.has_treasure()):
			c += ", treasure"
		return c + "\n"

	def set_position(self, x, y):
		"""
		Function to set the position of the player
		"""
		self.x = x
		self.y = y

	def has_key(self):
		"""
		Return a boolean to know if the player has the key
		"""
		return self.key

	def has_sword(self):
		"""
		Return a boolean to know if the player has the sword
		"""
		return self.sword

	def has_treasure(self):
		"""
		Return a boolean to know if the player has the treasure
		"""
		return self.treasure

	def gain_key(self):
		"""
		Set key to true because player gain the key
		"""
		self.key = True

	def gain_sword(self):
		"""
		Set sword to true because player gain the sword
		"""
		self.sword = True

	def gain_treasure(self):
		"""
		Set treasure to true because player gain the treasure
		"""
		self.treasure = True

	def loose_all_items(self):
		"""
		Player loose all of his items
		"""
		self.key = False
		self.sword = False
		self.treasure = False

	def get_next_move(self):
		"""
		Get next move as a human player
		"""
		k = input("Select action and then press enter :")
		if k == 'z':
			return self.x-1, self.y
		if k == 'q':
			return self.x, self.y-1
		if k == 'd':
			return self.x, self.y+1
		if k == 's':
			return self.x+1, self.y
		return -1, -1
