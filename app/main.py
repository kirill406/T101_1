import time
import random

def generate_simple_rules(code_max, n_max, n_generate, log_oper_choice =["and"," or","not"]):
	rules = []
	for j in range (0, n_generate):
		log_oper = random.choice(log_oper_choice) #not means and-not (neither)
		if n_max < 2:
			n_max = 2
		n_items = random.randint(2, n_max)
		items = []
		for i in range(0, n_items):
			items.append(random.randint(1, code_max))
		rule = {
			'if': {log_oper: items},
			'then ':code_max+j
		}
		rules.append(rule)
	random.shuffle(rules)
	return (rules)

def generate_seq_facts(M) :
	facts = list(range (0,M))
	random.shuffle(facts)
	return facts

def generate_rand_facts(code_max, M):
	facts = []
	for i in range(0,M):
		facts.append(random.randint(0, code_max) )
	return facts

#generate rules and facts and check time
time_start = time.time()
N = 100000
M = 1000
rules = generate_simple_rules(100, 4, N)
facts = generate_rand_facts(100, M)
print("%d rules generated in %f seconds" % (N, time.time()-time_start))
#load and validate rules
# YOUR CODE HERE
print(rules[:2])
#check facts vs rules
time_start = time.time()
# YOUR CODE HERE
print("%d facts validated vs %d rules in %f seconds" % (M, N, time.time()-time_start))
