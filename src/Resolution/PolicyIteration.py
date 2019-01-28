# from string import Template
# import json

from Util import *
import numpy as np


############################## variables ##############################

#theta = 0.01 # threshold
max_it = int(sys.argv[2])
gamma = 0.8 # gamma -> 0 <=> future action less important than current action

states, actions, transitions, rewards, w = get_data()

############################## functions ##############################

# transitions =
#	{"cell1" : 
# 		{"action1" : {newcell1 : p1, newcell2 : p2},
# 		"action2" : ...,
# 		}
# 	"cell2" : ..
# 	}

# rewards = 
# 	{'(cell k? t? s?)' :
# 		{"action1" : {'(newcell1 k1? t1? s1?)' : v1},
# 		"action2" : ...,
# 		}
# 	'(cell2 k2? t2? s2?)' : ...
# 	}


# Vpi+1 (s) = Es' [ T(s,pi(s),s') * ( R(s,pi(s),s') + gamma*Vpi(s') ) ]
# convergence Vpi = Es' [ ..... Vpi ]
# sum_matrR = Es' [ T * R ]
# matrL = T*gamma

### get new matrice matrL and matrR and sum_matrR with policy p
def it_matrice(p):
	temp_matrL = np.zeros((size, size))
	# matrR = np.zeros((size, size))
	temp_sum_matrR = np.zeros(size)

	### for each states[i]
	for i in range(len(states)):
		a = p[i]
		T = transitions[str(states[i][0])]
		# print(states[i], T)

		### for each states s' possible when doing action a
		for temp_c, temp_p in T[a].items():
			### get str_s2 = '(temp_c k t s)' and the associate reward R(states[i], a, s2) 
			str_s2,temp_r = get_reward(states[i], a, temp_c)
			# print(states[i])
			# print(temp_c)
			# print(str_s2, r)
			### replace '(_ k t s)' by the value of states[i]
			temp_s2 = complete_state(states[i], str_s2)
			# print(temp_s2)
			temp_s2 = convert_state_to_list(temp_s2)
			# print(temp_s2)

			temp_index = states.index(temp_s2)
			# print(states.index(temp_s2))
			# matrR[i][temp_index] = temp_p * temp_r
			temp_matrL[i][temp_index] += temp_p * gamma
			### !!! - sum_matrR !!!
			temp_sum_matrR[i] -= temp_p * temp_r
		# 	print(i,temp_index)
		# 	print(matrL[i][temp_index])
		# 	print(sum_matrR[i])
		# 	print("")
		# print("##################################")
	return temp_matrL, temp_sum_matrR

### get new policy pi(s) <- argmax_a Es' [T(s,a,s') * ( R(s,a,s') + gamma*values(s') )]
def update_policy(values):
	res_policy = [None] * (size)

	### for every states[i]
	for i in range(len(states)):
		res_action = old_policy[i] #None
		res_value = values[i] #-99999
		for temp_action, newcell_and_proba in transitions[str(states[i][0])].items():
			temp_a = temp_action
			temp_v = 0
			# print(temp_action, newcell_and_proba)

			### for every s'
			for newcell, proba in newcell_and_proba.items():
				str_s2, r = get_reward(states[i],temp_action, newcell)
				s2 = complete_state(states[i], str_s2)
				# print(s2)
				s2 = convert_state_to_list(s2)
				# print(s2)
				temp_index = states.index(s2)
				# print(values[temp_index])
				temp_v += proba * (r + ( gamma * values[temp_index] ))
			# 	print(temp_v)
			# print(temp_v, res_value)
			# print("##########")
			if (temp_v > res_value):
				res_action = temp_a
				res_value = temp_v

		res_policy[i] = res_action

		# print(values[i])
		# print(res_action, res_value)
		# print("######")

	# print(res_policy)
	return res_policy

def diff (l1, l2):
	cpt = 0
	for i in range(len(l1)):
		if l1[i] != l2[i]:
			cpt += 1
	return cpt

############################## policy iteration ##############################

size = len(states)
### array [ [-1].size ]
# matr_m1 = np.zeros(size)
# for i in range(len(matr_m1)):
# 	matr_m1[i] = -1
# print(matr_m1)

### initiate the matrice L and R 
matrL = np.zeros((size, size))
# matrR = np.zeros((size, size))
sum_matrR = np.zeros(size)

### initiate Vi and Vi+1
old_Vi = np.zeros(size)
current_Vi = np.zeros(size)

# Vi+1 = matrL * Vi + sum_matrR

### initiate the policy p with the any action possible for every states
### policy = list of action, index of this list = index states
### => policy[i] = action for the state states[i]
old_policy = []
current_policy = [None] * (size)
# print(len(current_policy))
for i in range(len(states)):
	# print(states[i])
	# print(transitions[str(states[i][0])])
	for a in transitions[str(states[i][0])].keys():
		current_policy[i] = a
		# print(a)
		# print(current_policy[i])

old_policy = current_policy.copy()
# print(current_policy)

# print(states[57])
# print(current_policy[57])
# print(current_policy)



### iterate : get the matrices matrL and sum_matrR from the current policy
# it_matrice(current_policy)
# print(matrL[511][503])
# #print(matrR[502][510])

# current_Vi = np.linalg.lstsq(matrL, sum_matrR, rcond=None)[0]
# print(current_Vi)

# print(np.array_equal(current_Vi, old_Vi))
same_policy = False
cpt_it = 0

while (not same_policy and cpt_it < max_it):
	### count it
	cpt_it += 1

	# matrL = np.zeros((size, size))
	# # matrR = np.zeros((size, size))
	# sum_matrR = np.zeros(size)
	
	### iterate
	### new matrices
	matrL, sum_matrR = it_matrice(current_policy)

	### calculate values Vi = matrL * Vi + sum_matrR
	old_Vi = current_Vi.copy()
	# !!! matrL * Vi = sum_matrR /////faux
	# current_Vi = np.linalg.lstsq(matrL, sum_matrR, rcond=None)[0]
	# print(matrL)
	# print(sum_matrR)
	# print(current_Vi)
	# print("###")

	### calculate matrice -sum_matrR = matrL' * Vi
	for i in range(len(matrL)):
		matrL[i][i] -= 1

	# print(matrL)
	# print(sum_matrR)
	# print("")
	current_Vi = np.linalg.lstsq(matrL, sum_matrR, rcond=None)[0]
	# print(current_Vi)


	### calculate best policy
	old_policy = current_policy.copy()
	current_policy = update_policy(old_Vi)
	print(diff(current_policy,old_policy))

	### same_policy = True if old_policy = current_policy
	same_policy = (old_policy == current_policy)
	# same_policy = diff(current_policy, old_policy) < threshold

# print(current_policy)
print("Resolution en: " + str(cpt_it) + " iteration!")

res = {}
for i in range(len(states)):
	res[convert_list_to_state(states[i])] = current_policy[i]

with open("./data/PolicyIterationRes_"+sys.argv[1], 'w') as file:
	file.write(json.dumps(res))
