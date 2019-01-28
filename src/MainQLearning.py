import argparse
import os

from Resolution.QLearning.QLearning import QLearning
from Maze.Maze import Maze

data_path = "../data/mazes/"
qtables_path = "../data/qtables/"

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
        else:
            print("Please specify a maze !")
            return
    else:
        m = Maze()
        m.load_maze(data_path+maze)

    if(os.path.isfile(qtables_path+maze)):
        train = False
        q = QLearning(filename=data_path+maze, savefile=qtables_path+maze, generate=False, maze=m)
    else:
        train = True
        q = QLearning(filename=data_path+maze, savefile=qtables_path+maze, generate=True, maze=m)

    if(train):
        print('Training starts')
        q.learning()
    else:
        while(True):
            w = input("Do you want to retrain ? (y/n) : ")
            if(w == 'y'):
                print('Training starts')
                q.learning()
                break
            if(w == 'n'):
                break
            print("Wrong instruction !")

    q.show_policy()

parser = argparse.ArgumentParser()
parser.add_argument('-m', '--maze',
                    help="The name of the maze you want to play in the maze/data/mazes, default = "" and a maze will be generated",
                    default="")
args = parser.parse_args()

maze = args.maze

main(maze)
