""" uncomment if python 2.7
#!/usr/bin/python2.7
# -*-coding:Latin-1 -*
"""

import sys
import json

################################### global ###################################

### probability
# probability to survive/die to an enemy E without a sword
enemyP_survive = 0.7
enemyP_die = 0.3

# probability die/bring to start/nothing happens on a trap R
trapP_start = 0.3
trapP_die = 0.1
trapP_null = 0.6
#trapP_die = str("%.3f" % (0.1/0.7))
#trapP_null = str("%.3f" % (0.6/0.7))

### rewards when landing in a cell
# treasure
treasureR_key = "100"
treasureR_noKey = "-1"
# key
keyR_noKey = "50"
keyR_key = "-1"
# sword
swordR_noSword = "25"
swordR_sword = "-1"
# enemy
enemyR_sword = "-1"
enemyR_noSwordSurvive = "-10"
enemyR_noSwordDie = "-500"
enemyR_noSword = "-250"
# trap
trapR_die = "-500"
trapR_null = "-10"
trapR = "-250"
# crack
crackR = "-500"
# empty cell
emptyR = "-1"
# starting position
startR_treasure = "1000"
startR_noTreasure = "-5"

################################### open files ###################################

f = open("../../data/mazes/"+sys.argv[1], 'r')
#print("../maze-master/data/mazes/"+sys.argv[1])
res = open("./models/"+sys.argv[1], 'w')

################################### get the maze ###################################

maze = list()
line = f.readline()
while line:
	maze.append(line[:-1])
	line = f.readline()
#print(maze)

################################### transform to MDP ###################################

##### S : states (pos, key?, treasure?, sword?)
##### A : actions {left, right, up, down}
##### T : transitions T: SxAxS -> [0,1]
##### 	T(s,a,s') = p
##### R : reward R: SxAxSxINT -> [0,1]
##### 	R(s,a,s',v) = probability to get reward v when s->s' with action a

states = []
actions = ["LEFT", "RIGHT", "UP", "DOWN"]
# {s : {a1 : {s1 : p1, s2 : p2, ..}, a2 : .. } }
transitions = {}
# {s : {a1 : {s1 : v1, s2 : v2, ..}, a2 : .. } }
rewards = {}


if maze:
	h = len(maze)
	w = len(maze[0])
	# list of position that is not a wall nor a portal, used when move to a magic portal
	pos_can_teleport = []
	# starting position
	start = []
	for i in range(h):
		for j in range(w):
			# cant teleport to a wall
			# !!! cant teleport to a portal or plateform #
			if maze[i][j] != '#' and maze[i][j] != '-' and maze[i][j] != 'P':
				pos_can_teleport.append([i,j])
			if maze[i][j] == 'o':
				start = [i,j]

	#print(len(pos_can_teleport))
	#print(pos_can_teleport)
	#print(start)




	### functions ###

	# return list of (ni,nj) neighbouring cells of (i,j)
	def get_neighbouring_cell(i,j, ci=-1, cj=-1):
		res = []
		if i != 0:
			res.append([i-1,j])
			if j != 0:
				res.append([i-1,j-1])
			if j != w-1:
				res.append([i-1,j+1])
		if i != h-1:
			res.append([i+1,j])
			if j != 0:
				res.append([i+1,j-1])
			if j != w-1:
				res.append([i+1,j+1])
		if j != 0:
			res.append([i, j-1])
		if j != w-1:
			res.append([i, j+1])

		if (ci != -1 and cj != -1):
			res.remove([ci,cj])

		# !!! cant move to a portal or plateform
		# for (ni, nj) in res:
		# 	if maze[ni][nj] == "P" or maze[ni][nj] == "-":
		# 		res.remove([ni,nj])
		# print(res)
		for (ni, nj) in res:
			# print(ni,nj)
			if maze[ni][nj] == "P":
				res.remove([ni,nj])
			if maze[ni][nj] == "-":
				# print("-")
				res.remove([ni,nj])
				res += get_neighbouring_cell(ni, nj, i, j)

		#

		return res

	#print (get_neighbouring_cell(5,5))

	# write every States possibles for a cell of the maze
	# S : (pos, key?, treasure?, sword?)
	def generate_states(i,j):
		res.write("S: ("+str(w*i + j)+" 0 0 0)\n")
		res.write("S: ("+str(w*i + j)+" 0 0 1)\n")
		res.write("S: ("+str(w*i + j)+" 0 1 0)\n")
		res.write("S: ("+str(w*i + j)+" 0 1 1)\n")
		res.write("S: ("+str(w*i + j)+" 1 0 0)\n")
		res.write("S: ("+str(w*i + j)+" 1 0 1)\n")
		res.write("S: ("+str(w*i + j)+" 1 1 0)\n")
		res.write("S: ("+str(w*i + j)+" 1 1 1)\n")

		cell = w*i + j
		states.append((cell, 0, 0, 0))
		states.append((cell, 0, 0, 1))
		states.append((cell, 0, 1, 0))
		states.append((cell, 0, 1, 1))
		states.append((cell, 1, 0, 0))
		states.append((cell, 1, 0, 1))
		states.append((cell, 1, 1, 0))
		states.append((cell, 1, 1, 1))

	# write Transition T(s,a,s') = p ( s<- actual_pos, s' <- (newi, newj) )
	def write_transitions(actual_pos, a, newi, newj, p):
		new_pos = str(w*newi + newj)
		new_cell_type = maze[newi][newj]

		tr_s = "(" + actual_pos + " k t s)"

		# moving to a moving plateform
		if (new_cell_type == "-"):
			n_cells = get_neighbouring_cell(newi,newj)
			probability = 1/len(n_cells)
			for (temp_i,temp_j) in n_cells:
				write_transitions(actual_pos, a, temp_i, temp_j, probability)

		# moving to a magic portal
		elif (new_cell_type == "P"):
			probability = 1/len(pos_can_teleport)
			for (temp_i,temp_j) in pos_can_teleport:
				write_transitions(actual_pos, a, temp_i, temp_j, probability)

		# moving to a wall
		elif (new_cell_type == "#"):
			res.write("T: (" + actual_pos + " k t s), " + a + ", (" + str(w*start[0] + start[1]) + " k t s) = " + str(p) + "\n")
			write_rewards(actual_pos, a, start[0], start[1])

			#tr_s2 = "(" + str(w*start[0] + start[1]) + " k t s)"
			#add_transition(tr_s, tr_s2, a, p)
			s2 = str(w*start[0] + start[1])
			add_transition(actual_pos, s2, a, p)

		# moving to a trap
		elif (new_cell_type == "R"):
			res.write("T: (" + actual_pos + " k t s), " + a + ", (" + str(w*start[0] + start[1]) + " k t s) = " + str( p * trapP_start ) + "\n")
			write_rewards(actual_pos, a, start[0], start[1])
			#tr_s2 = "(" + str(w*start[0] + start[1]) + " k t s)"
			#add_transition(tr_s, tr_s2, a, p * trapP_start)
			s2 = str(w*start[0] + start[1])
			add_transition(actual_pos, s2, a, p * trapP_start)

			res.write("T: (" + actual_pos + " k t s), " + a + ", (" + new_pos + " k t s) = " + str( p * (trapP_null + trapP_die) ) + "\n")
			write_rewards(actual_pos, a, newi, newj)
			#tr_s2 = "(" + new_pos + " k t s)"
			#add_transition(tr_s, tr_s2, a, p * (trapP_null + trapP_die))
			s2 = new_pos
			add_transition(actual_pos, s2, a, p * (trapP_null + trapP_die))

		# moving to any other cell
		else:
			res.write("T: (" + actual_pos + " k t s), " + a + ", (" + new_pos + " k t s) = " + str(p) + "\n")
			write_rewards(actual_pos, a, newi, newj)

			#tr_s2 = "(" + new_pos + " k t s)"
			#add_transition(tr_s, tr_s2, a, p)
			s2 = new_pos
			add_transition(actual_pos, s2, a, p)


	# write Rewards R(s,a,s',v) = p ( s<- actual_pos, s' <- (newi, newj) )
	def write_rewards(actual_pos, a, newi, newj):
		new_pos = str(w*newi + newj)
		new_cell_type = maze[newi][newj]

		# reward treasure
		if new_cell_type == "T":
			res.write("R: (" + actual_pos + " 0 t s), " + a + ", (" + new_pos + " 0 t s), " + treasureR_noKey + ") = 1\n")
			res.write("R: (" + actual_pos + " 1 t s), " + a + ", (" + new_pos + " 1 t s), " + treasureR_key + ") = 1\n")

			tr_s = "(" + actual_pos + " 0 t s)"
			tr_s2 = "(" + new_pos + " 0 t s)"
			add_reward(tr_s, tr_s2, a, treasureR_noKey)
			tr_s = "(" + actual_pos + " 1 t s)"
			tr_s2 = "(" + new_pos + " 1 t s)"
			add_reward(tr_s, tr_s2, a, treasureR_key)

		# reward key
		if new_cell_type == "K":
			res.write("R: (" + actual_pos + " 0 t s), " + a + ", (" + new_pos + " 1 t s), " + keyR_noKey + ") = 1\n")
			res.write("R: (" + actual_pos + " 1 t s), " + a + ", (" + new_pos + " 1 t s), " + keyR_key + ") = 1\n")

			tr_s = "(" + actual_pos + " 0 t s)"
			tr_s2 = "(" + new_pos + " 1 t s)"
			add_reward(tr_s, tr_s2, a, keyR_noKey)
			tr_s = "(" + actual_pos + " 1 t s)"
			add_reward(tr_s, tr_s2, a, keyR_key)

		# reward sword
		if new_cell_type == "S":
			res.write("R: (" + actual_pos + " k t 0), " + a + ", (" + new_pos + " k t 1), " + swordR_noSword + ") = 1\n")
			res.write("R: (" + actual_pos + " k t 1), " + a + ", (" + new_pos + " k t 1), " + swordR_sword + ") = 1\n")

			tr_s = "(" + actual_pos + " k t 0)"
			tr_s2 = "(" + new_pos + " k t 1)"
			add_reward(tr_s, tr_s2, a, swordR_noSword)
			tr_s = "(" + actual_pos + " k t 1)"
			add_reward(tr_s, tr_s2, a, swordR_sword)

		# reward enemy
		if new_cell_type == "E":
			res.write("R: (" + actual_pos + " k t 0), " + a + ", (" + new_pos + " k t 0), " + enemyR_noSwordSurvive + ") = " + str(enemyP_survive) + "\n")
			res.write("R: (" + actual_pos + " k t 0), " + a + ", (" + new_pos + " k t 0), " + enemyR_noSwordDie + ") = " + str(enemyP_die) + "\n")
			res.write("R: (" + actual_pos + " k t 1), " + a + ", (" + new_pos + " k t 1), " + enemyR_sword + ") = 1\n")

			tr_s = "(" + actual_pos + " k t 0)"
			tr_s2 = "(" + new_pos + " k t 0)"
			add_reward(tr_s, tr_s2, a, enemyR_noSword) ### survive & die
			tr_s = "(" + actual_pos + " k t 1)"
			tr_s2 = "(" + new_pos + " k t 1)"
			add_reward(tr_s, tr_s2, a, enemyR_sword)

		# reward trap
		if new_cell_type == "R":
			res.write("R: (" + actual_pos + " k t s), " + a + ", (" + new_pos + " k t s), " + trapR_die + ") = " + str(trapP_die/(trapP_die+trapP_null)) + "\n")
			res.write("R: (" + actual_pos + " k t s), " + a + ", (" + new_pos + " k t s), " + trapR_null + ") = " + str(trapP_null/(trapP_die+trapP_null)) + "\n")

			tr_s = "(" + actual_pos + " k t s)"
			tr_s2 = "(" + new_pos + " k t s)"
			add_reward(tr_s, tr_s2, a, trapR) ### survive & die

		# reward crack
		if new_cell_type == "C":
			res.write("R: (" + actual_pos + " k t s), " + a + ", (" + new_pos + " k t s), " + crackR + ") = 1\n")

			tr_s = "(" + actual_pos + " k t s)"
			tr_s2 = "(" + new_pos + " k t s)"
			add_reward(tr_s, tr_s2, a, crackR)

		# reward empty cell
		if new_cell_type == "_":
			res.write("R: (" + actual_pos + " k t s), " + a + ", (" + new_pos + " k t s), " + emptyR + ") = 1\n")

			tr_s = "(" + actual_pos + " k t s)"
			tr_s2 = "(" + new_pos + " k t s)"
			add_reward(tr_s, tr_s2, a, emptyR)

		# reward starting position
		if new_cell_type == "o":
			res.write("R: (" + actual_pos + " k 0 s), " + a + ", (" + new_pos + " k 0 s), " + startR_noTreasure + ") = 1\n")
			res.write("R: (" + actual_pos + " k 1 s), " + a + ", (" + new_pos + " k 1 s), " + startR_treasure + ") = 1\n")

			tr_s = "(" + actual_pos + " k 0 s)"
			tr_s2 = "(" + new_pos + " k 0 s)"
			add_reward(tr_s, tr_s2, a, startR_noTreasure)
			tr_s = "(" + actual_pos + " k 1 s)"
			tr_s2 = "(" + new_pos + " k 1 s)"
			add_reward(tr_s, tr_s2, a, startR_treasure)

	# add transition to the dictionary transitions
	def add_transition(s, s2, a, p):
		if (s not in transitions):
			transitions[s] = {a : {s2 : p}}
		elif(a not in transitions[s]):
			transitions[s][a] = {s2 : p}
		elif (s2 in transitions[s][a]):
			transitions[s][a][s2] += p
		else:
			transitions[s][a][s2] = p

	# add reward to the dictionary rewards
	def add_reward(s, s2, a, v):
		v = int(v)
		if (s not in rewards):
			rewards[s] = {a : {s2 : v}}
		elif(a not in rewards[s]):
			rewards[s][a] = {s2 : v}
		else:
			rewards[s][a][s2] = v

	# Move: action a from pos (i,j)
	def move(i,j,a):
		actual_pos = str(w*i + j)

		### MOVE
		res.write("// action: " + a + ", ")
		new_i = i
		new_j = j
		if (a == "DOWN"):
			new_i += 1
		if (a == "UP"):
			new_i -= 1
		if (a == "LEFT"):
			new_j -= 1
		if (a == "RIGHT"):
			new_j += 1

		### TRANSITIONS (+ REWARDS)
		res.write ("new pos: (" + str(w*new_i+new_j) + "), ")
		res.write ("cell type: " + maze[new_i][new_j] + "\n")

		write_transitions(actual_pos, a, new_i, new_j, 1)


	for i in range(h):
			for j in range(w):

				# STATES
				generate_states(i,j)

				# TRANSITIONS + REWARD

				# can move up
				if (i != 0):
					move(i,j,"UP")

				# can move down
				if (i != h-1):
					move(i,j,"DOWN")

				# can move to the left
				if (j != 0):
					move(i,j,"LEFT")

				# can move to the right
				if (j != w-1):
					move(i,j,"RIGHT")

#print (states)
#print (transitions)
#print (rewards)
data = open("../Resolution/data/"+sys.argv[1], 'w')
data.write("### STATES ###\n")
data.write(json.dumps(states) + "\n")

data.write("### ACTIONS ###\n")
data.write(json.dumps(actions) + "\n")

data.write("### TRANSITIONS ###\n")
data.write(json.dumps(transitions) + "\n")

data.write("### REWARDS ###\n")
data.write(json.dumps(rewards) + "\n")

data.write("### MAZE DATA ###\n")
data.write(json.dumps(w) + "\n")
