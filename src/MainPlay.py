import argparse

from Game.Game import Game
from Maze.Maze import Maze

data_path = "../data/mazes/"

def main(maze):
    if(maze == ""):
        generate = input("No maze specified.\nDo you want to generate one ? (y/n) : ")
        if(generate == 'y'):
            m = Maze()
            while(True):
                filename = input("Enter the name of the maze without path and .txt : ")
                nb_lines = int(input("Enter the number of lines : "))
                nb_columns = int(input("Enter the number of columns : "))
                if(nb_lines > 0 and nb_columns > 0):
                    break
                else:
                    print("Informations incorrect with the size of the maze !")
            maze = filename+'.txt'
            m.init_random_maze(nb_lines, nb_columns, data_path+maze)
            print("The maze was succesfully generated !")
            g = Game(m)
            g.play_a_game()
        else:
            print("Please specify a maze !")
            return
    else:
        m = Maze()
        m.load_maze(data_path+maze)
        g = Game(m)
        g.play_a_game()
        return

parser = argparse.ArgumentParser()
parser.add_argument('-m', '--maze',
                    help="The name of the maze you want to play in the maze/data/mazes, default = ""\nPriority over generate",
                    default="")
args = parser.parse_args()

maze = args.maze

main(maze)
