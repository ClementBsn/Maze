from Util import *

############################## variables ##############################

states, actions, transitions, rewards, _ = get_data()


theta = 0.01 # threshold
gamma = 0.99 # gamma -> 0 <=> future action less important than current action


### V(s) = max_a E [ (R(s,a,s2) + gamma*Vp(s2)) * T(s,a,s2) ]
def it():
	### for each states
	for s in states:		
		### T = {'a' : {'cell2':t}, ..} all the transition from state s
		T = transitions[str(s[0])]
		# print(T)
		res = current_v[convert_list_to_state(s)]

		### for each action a
		for a,state_and_proba in T.items():
			# print(state_and_proba)
			temp_v = 0
			for cell2,t in state_and_proba.items():
				### get reward s2,r = R(s,a,s2)
				s2,r = get_reward(s,a,cell2)
				# print(s, cell2)
				# # print(s2, r)
				# print(s,s2)
				# print(complete_state(s,s2))
				# print(old_v[complete_state(s,s2)])
				temp_v += t*(r+ gamma*old_v[complete_state(s,s2)][0])
				# print(temp_v)

			if temp_v > res[0]:
				res = (temp_v, a)

		# update values
		current_v[convert_list_to_state(s)] = res
	# print(old_v)
	# print(current_v)

### return true if for each states s, |currentv(s) - oldv(s)| >= threshold theta
def continue_it(oldv, currentv):
	for s in states:
		str_s = convert_list_to_state(s)
		if (abs(currentv[str_s][0] - oldv[str_s][0]) >= theta):
			print(abs(currentv[str_s][0] - oldv[str_s][0]))
			# print(str_s)
			# print(currentv[str_s])
			# print(oldv[str_s])
			return True
	return False


############################## value iteration ##############################

### initiate the values to 0
### v = {state : value, ..}
# old_v = {}
# current_v = {}
# for s in states:
# 	old_v[convert_list_to_state(s)] = 0
# 	current_v[convert_list_to_state(s)] = 0

### initiate the values from any action for each states
### v = {state : (value, action), ..}
old_v = {}
current_v = {}
for s in states:
	### T = {'a' : {'cell2':t}, ..} all the transition from state s
	T = transitions[str(s[0])]
	temp_a = ""
	temp_c = ""
	for a,dic in T.items():
		for c in dic.keys():
			temp_a = a
			temp_c = c

	s2, r = get_reward(s, a, c)
	current_v[convert_list_to_state(s)] = (r,a)

old_v = current_v.copy()
# print(current_v)

### first it
nb_it = 1
it()
# print(old_v)
# print("################")
# print(current_v)
# print(continue_it(old_v,current_v))

while(continue_it(old_v, current_v)):
	### count + 1
	# print("iteration: " + str(nb_it))
	nb_it += 1

	### update old value
	old_v = current_v.copy()

	### iterate
	it()
	# print(current_v)
	# print(continue_it(old_v, current_v))

# print(current_v)
print("Resoluion en: " + str(nb_it) + " iterations!")

res = {}
for st,v_a in current_v.items():
	res[st] = v_a[1]

with open("./data/ValueIterationRes_"+sys.argv[1], 'w') as file:
	file.write(json.dumps(res))
