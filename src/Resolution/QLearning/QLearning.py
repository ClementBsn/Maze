import json
import random
import time
import sys
import numpy as np

from Maze.Maze import Maze
from Resolution.QLearning.Agent import Agent
from Configuration.types import *
from Configuration.results import *
from Resolution.QLearning.DistributedRandomNumberGenerator import DRNG

class QLearning():
    """
    Class of the QLearning algorithm, it returns a way through the maze to victory
    """
    def __init__(self, filename, savefile, generate, maze,
                 alpha=0.9, gamma=0.2, nbMaxGames=4000, nbMaxMoves=200):
        self.filename = filename                        # the name of the maze (path to load)
        self.savefile = savefile                        # the name to save
        self.maze = maze                                # the maze

        # Agent start at (0,0)
        x, y = self.maze.start_position
        self.agent = Agent(x, y)

        # generate indicate if we want to learn a new Agent for the maze or use a Agent that exists
        if(generate):
            self.qtable = self.initialize_QTable()
            self.save_Q()
        else:
            self.qtable = self.load_Q()

        # the parameters of the algorithm
        self.alpha = alpha                  # alpha is The learning rate
        self.gamma = gamma                  # gamma is the discount factor
        self.nbMaxMoves = nbMaxMoves        # nbMaxMoves is the number max of moves that the Agent can do per game
        self.nbMaxGames = nbMaxGames        # nbMaxGames is the number of games that the Agent will play in the maze

    def learning(self):
        """
        The function that make the Agent learn
        """
        nb_games = 0
        # The Agent will move in the maze for nbMaxGames games
        while(nb_games < self.nbMaxGames):
            print("Game "+str(nb_games)+" of "+str(self.nbMaxGames))
            nb_moves = 0
            # limit of moves in the maze
            while(nb_moves < self.nbMaxMoves):
                # position of the agent
                x, y = self.agent.x, self.agent.y
                # the stats as hasKey, hasSword and hasTreasure
                k,s,t = self.agent.get_agent_stats()

                # the agent select a cell to move
                goto, direction = self.get_next_move_softmax(x, y, k, s, t, self.get_t(nb_moves))

                goto_x, goto_y = goto

                # get the consequence of the new cell the Agent came to
                result = self.maze.get_consequence_move(self.agent, goto_x, goto_y)

                next_x, next_y = goto_x, goto_y
                # if PLATFORM or PORTAL then the Agent is moved to another cell
                while(result == PLATFORM_MOVE or result == PORTAL_MOVE):
                    next_x, next_y = self.get_next_position(result, next_x, next_y)
                    result = self.maze.get_consequence_move(self.agent, next_x, next_y)

                # get the final position of the Agent
                next_x, next_y = self.get_next_position(result, next_x, next_y)

                # get the reward
                reward = self.get_reward(result)

                # update the qvalue (a high qvalue means that the Agent should go to this cell)
                self.update_qvalue(x, y, k, s, t, direction, next_x, next_y, reward)

                # process the consequence of the cell
                end_game = self.process_consequence(result, next_x, next_y)

                if(end_game):
                    nb_moves = self.nbMaxMoves + 2
                nb_moves += 1

            self.save_Q()
            self.restart_game()
            nb_games += 1

    def show_policy(self):
        """
        Function that shows how the agent moves in the maze to solve it
        """
        alphabet = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
        end_game = False
        states = list()
        print("Start of showing QLearning policy")
        print("q : backward")
        print("d : forward")

        print("Loading policy")
        while(not end_game):
            x, y = self.agent.x, self.agent.y
            k,s,t = self.agent.get_agent_stats()
            goto, direction = self.get_next_move_greedy(x, y, k, s, t)
            goto_x, goto_y = goto

            states.append([x, y, k, s, t, goto_x, goto_y, direction])

            result = self.maze.get_consequence_move(self.agent, goto_x, goto_y)

            next_x, next_y = goto_x, goto_y
            while(result == PLATFORM_MOVE or result == PORTAL_MOVE):
                next_x, next_y = self.get_next_position(result, next_x, next_y)
                result = self.maze.get_consequence_move(self.agent, next_x, next_y)

            next_x, next_y = self.get_next_position(result, next_x, next_y)

            end_game = self.process_consequence(result, next_x, next_y)

        x, y = self.agent.x, self.agent.y
        k,s,t = self.agent.get_agent_stats()

        states.append([x, y, k, s, t, None, None, None])

        i = 0
        max_i = len(states)-1
        while(True):
            x, y, k, s, t, goto_x, goto_y, direction = states[i]
            self.agent.set_position(x,y)
            self.agent.set_agent_stats(k, s, t)
            c = "########## STATE : "+str(i)+" ##########\n"
            c += str(self.agent)+"\n"
            c += str(self.maze.print_maze(x,y))+"\n\n"
            if(direction != None):
                c += str(direction)+" -> ("+str(alphabet[goto_x])+", "+str(alphabet[goto_y])+")\n"
                for dir in self.qtable[self.coord_to_string(x,y,k,s,t)].keys():
                    qv = self.qtable[self.coord_to_string(x,y,k,s,t)][dir][1]
                    c += str(dir)+" : "+str(qv)+"\t|"
                c += "\n"
            sys.stdout.write(c)
            sys.stdout.flush()

            if(i == max_i):
                print("End")
                while(True):
                    w = input("Stop here ? (y/n) : ")
                    if(w == 'y'):
                        return
                    if(w == 'n'):
                        break
                    print("Wrong instruction !")

            while(True):
                w = input("backward or forward ? (q/d) : ")
                if(w == 'q'):
                    if(i == 0):
                        print("Can't go backward")
                        continue
                    i -= 1
                    break
                if(w == 'd'):
                    if(i == max_i):
                        print("Can't go forward")
                        while(True):
                            w = input("Stop here ? (y/n) : ")
                            if(w == 'y'):
                                return
                            if(w == 'n'):
                                break
                            print("Wrong instruction !")
                        break
                    i += 1
                    break
                print("Wrong instruction !")

    def restart_game(self):
        x, y = self.maze.start_position
        self.agent.set_position(x,y)
        self.agent.loose_all_items()

    def get_t(self, k):
        if(k < 10):
            return 1.0
        if(k < 25):
            return 0.8
        if(k < 4000):
            return 20.0 / k
        return 0.5

    def get_next_move_softmax(self, x, y, k, s, t, explo):
        """
        Returns the action that has the maximum qvalue in cell (x,y)
        with a softmax
        """
        qtable_cell = self.qtable[self.coord_to_string(x, y, k, s, t)]
        softmax_values = list()
        softmax_sum = 0
        moves = list()

        for dir in qtable_cell.keys():
            e = np.exp(qtable_cell[dir][1] / explo)
            softmax_values.append(e)
            softmax_sum += e
            moves.append(dir)

        drng = DRNG()

        for i in range(len(softmax_values)):
            drng.add_number(i, softmax_values[i] / softmax_sum)

        next_move = drng.get_DRB()

        return qtable_cell[moves[next_move]][0], moves[next_move]

    def get_next_move_greedy(self, x, y, k, s, t):
        """
        Returns the action that has the maximum qvalue in cell (x,y)
        """
        qtable_cell = self.qtable[self.coord_to_string(x, y, k, s, t)]
        next_moves = list()
        qvalue_next_move = -float('Inf')

        for dir in qtable_cell.keys():
            dest = qtable_cell[dir]

            if(dest[1] == qvalue_next_move):
                next_moves.append([dest[0], dir])

            if(dest[1] > qvalue_next_move):
                next_moves = [[dest[0], dir]]
                qvalue_next_move = dest[1]

        r = random.randint(0, len(next_moves) - 1)
        return next_moves[r][0], next_moves[r][1]

    def get_next_position(self, result, x, y):
        """
        Returns the next position if the agent go in room (x, y)
        """
        if(result == PORTAL_MOVE):
            return self.maze.portal_movement(x,y)
        if(result == PLATFORM_MOVE):
            return self.maze.platform_movement(x,y)
        if(result == MOVE_TO_START or result == DIE):
            return self.maze.start_position
        return x, y


    def process_consequence(self, result, x, y):
        """
        Process the consequences to the Agent, and make it go to (x,y)
        """
        self.agent.set_position(x,y)

        if(result == WIN_MAZE or result == DIE):
            self.agent.loose_all_items()
            return True
        if(result == GAIN_TREASURE):
            self.agent.gain_treasure()
        if(result == GAIN_KEY):
            self.agent.gain_key()
        if(result == GAIN_SWORD):
            self.agent.gain_sword()
        if(result == MOVE_TO_START and self.agent.has_treasure()):
            self.agent.loose_all_items()
            return True
        return False

    def get_max_qvalue(self, x, y, k, s, t , qv):
        """
        Returns the max of the qvalues in every direction of cell (x,y)
        """
        qtable_cell = self.qtable[self.coord_to_string(x, y, k, s, t)]
        max_qvalue = 0

        for dir in qtable_cell.keys():
            dest = qtable_cell[dir]

            if(dest[1] - qv > max_qvalue):
                max_qvalue = dest[1] - qv

        return max_qvalue

    def get_reward(self, result):
        if(result == DIE):
            return -50
        if(result == WIN_MAZE):
            return 40
        if(result == GAIN_KEY):
            return 20
        if(result == GAIN_SWORD):
            return 15
        if(result == GAIN_TREASURE):
            return 30
        if(result == MOVE_TO_START):
            if(self.agent.has_treasure()):
                return 40
            return -20
        return -1

    def update_qvalue(self, x, y, k, s, t, a, x_dest, y_dest, reward):
        """
        Updates the qvalue of cell (x,y) when action a is selected and arrives
        in (x_dest, y_dest) with reward
        """
        qvalue = self.qtable[self.coord_to_string(x, y, k, s, t)][a][1]
        new_qvalue = (1.0-self.alpha) * qvalue + self.alpha * (reward + self.gamma * self.get_max_qvalue(x_dest, y_dest, k, s, t, qvalue))
        self.qtable[self.coord_to_string(x, y, k, s, t)][a][1] = new_qvalue

    def save_Q(self):
        """
        Save the QTable in savefile
        """
        file = open(self.savefile, 'w')
        file.write("QTABLE\n")
        file.write(json.dumps(self.qtable) + "\n")

    def load_Q(self):
        """
        Load the QTable writen in savefile
        """
        file = open(self.savefile, 'r')
        s = file.read()
        temp = s.split('\n')
        if(temp == ['']):
            return self.initialize_QTable()
        return json.loads(temp[1])

    def coord_to_string(self, x, y, k, s, t):
        """
        Returns a string of the coordinates given
        """
        return str(x) +" "+str(y)+" "+str(k)+" "+str(s)+" "+str(t)

    def string_to_coord(self, s):
        """
        Returns x and y from a string of coordinates
        """
        l = s.split()
        return int(l[0]), int(l[1]), int(l[2]), int(l[3]), int(l[4])

    def initialize_QTable(self):
        """
        Returns an initialization of the QTable for the maze
        """
        m = self.maze
        qtable = dict()

        for x in range(m.lines):
            for y in range(m.columns):
                cell = m.maze[x][y]

                if(cell.type == PLATFORM or cell.type == CRACKS or cell.type == PORTAL or cell.type == WALL):
                    continue
                for k in [0,1]:
                    for s in [0,1]:
                        for t in [0,1]:
                            new_d = dict()
                            for coord, dir in m.get_neighbors_with_directions(x,y):
                                new_d[dir] = [coord, 0.0]
                            qtable[self.coord_to_string(x,y,k,s,t)] = new_d

        return qtable
