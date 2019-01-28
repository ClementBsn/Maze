import sys
import json

from Game.Game import Game
from Maze.Maze import Maze

data_path = "../data/mazes/"
policy_path = "./Resolution/data/" + sys.argv[2] + "IterationRes_" + sys.argv[1]

with open(policy_path) as file:
	policy = json.load(file)
	# print(policy['(0 0 0 0)'])

m = Maze()
m.load_maze(data_path + sys.argv[1])
g = Game(m)
g.play_a_game(policy)
