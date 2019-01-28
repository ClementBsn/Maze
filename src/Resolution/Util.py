import sys
import json
from string import Template

state_template = Template("($cell $key $treasure $sword)")

# S = [s, s2, ..] 
# s = [cell, key?, treasure?, sword?]
states = []
# A = ["LEFT", "RIGHT", "UP", "DOWN"]
actions = []
# T = {cell : {a1 : {new_cell1 : p1, new_cell2 : p2, ..}, a2 : .. } }
transitions = {}
# R = {s : {a1 : {s1 : v1, s2 : v2, ..}, a2 : .. } }
# s = '(cell, k?, t?, s?)'
rewards = {}
# weight of the maze
w = 0

############################## get data ##############################
with open("./data/"+sys.argv[1], 'r') as file:
	s = file.read()
	temp = s.split('\n')
	states = json.loads(temp[1])
	actions = json.loads(temp[3])
	transitions = json.loads(temp[5])
	rewards = json.loads(temp[7])
	w = json.loads(temp[9])

############################## functions ##############################

def get_data():
	return states, actions, transitions, rewards, w

### convert list s [c, k?, t?, s?] to string '(c k t s)'
def convert_list_to_state(s):
	return state_template.substitute(cell=s[0], key=s[1], treasure=s[2], sword=s[3])
def convert_to_state(c, k, t, s):
	return state_template.substitute(cell=c, key=k, treasure=t, sword=s)

### return c,k,t,s from state str_s = '(c k t s)'
def convert_state_to_list(str_s):
	cell,kts = str_s.split(" ", 1)
	return [int(cell[1:]), int(kts[0]), int(kts[2]), int(kts[4])]
# print(convert_state_to_list('(66 1 1 1)'))

### replace k, t, s of str_s2 with value from s
def complete_state(s,str_s2):
	res = str_s2.replace("k",str(s[1]), 1)
	res = res.replace("t",str(s[2]), 1)
	res = res.replace("s",str(s[3]), 1)
	return res
#print(complete_state([4,1,2,3], "(4 k t s)"))

### get the reward R(s,a,s'=(cell,k,t,s))
def get_reward(s,a,cell):
	ce = s[0]
	ke = s[1]
	tr = s[2]
	sw = s[3]
	for i in [convert_to_state(ce, 'k', 't', sw), convert_to_state(ce, 'k', tr, 's'), convert_to_state(ce, ke, 't', 's'), convert_to_state(ce, 'k', 't', 's')]:
		if i in rewards and a in rewards[i]:
			for j,r in rewards[i][a].items():
				if ( ("("+cell) in j):
					return j,r