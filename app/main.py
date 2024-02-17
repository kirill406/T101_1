from random import choice, shuffle, randint
from time import time


def generate_simple_rules(code_max, n_max, n_generate, log_oper_choice=None):
    if log_oper_choice is None:
        log_oper_choice = ["and", "or", "not"]
    rules = []
    if n_max < 2:
        n_max = 2
    for j in range(0, n_generate):
        log_oper = choice(log_oper_choice)  # not means and-not (neither)
        n_items = randint(2, n_max)
        items = []
        for i in range(0, n_items):
            items.append(randint(1, code_max))
        rule = {
            'if': {
                log_oper: items
            },
            'then': code_max + j
        }
        rules.append(rule)
    shuffle(rules)
    return rules


def generate_stairway_rules(code_max, n_max, n_generate, log_oper_choice=None):
    if log_oper_choice is None:
        log_oper_choice = ["and", "or", "not"]
    rules = []
    if n_max < 2:
        n_max = 2
    for j in range(0, n_generate):
        log_oper = choice(log_oper_choice)  # not means and-not (neither)
        n_items = randint(2, n_max)
        items = []
        for i in range(0, n_items):
            items.append(i + j)
        rule = {
            'if': {
                log_oper: items
            },
            'then': i + j + 1
        }
        rules.append(rule)
    shuffle(rules)
    return rules


def generate_ring_rules(code_max, n_max, n_generate, log_oper_choice=None):
    if log_oper_choice is None:
        log_oper_choice = ["and", "or", "not"]
    rules = generate_stairway_rules(code_max, n_max, n_generate - 1, log_oper_choice)
    log_oper = choice(log_oper_choice)  # not means and-not (neither)
    if n_max < 2:
        n_max = 2
    n_items = randint(2, n_max)
    items = []
    for i in range(0, n_items):
        items.append(code_max - i)
    rule = {
        'if': {
            log_oper: items
        },
        'then': 0
    }
    rules.append(rule)
    shuffle(rules)
    return rules


def generate_random_rules(code_max, n_max, n_generate, log_oper_choice=None):
    if log_oper_choice is None:
        log_oper_choice = ["and", "or", "not"]
    rules = []
    if n_max < 2:
        n_max = 2
    for j in range(0, n_generate):

        log_oper = choice(log_oper_choice)  # not means and-not (neither)

        n_items = randint(2, n_max)
        items = []
        for i in range(0, n_items):
            items.append(randint(1, code_max))
        rule = {
            'if': {
                log_oper: items
            },
            'then': randint(1, code_max)
        }
        rules.append(rule)
    shuffle(rules)
    return rules


def generate_seq_facts(M):
    facts = list(range(0, M))
    shuffle(facts)
    return facts


def generate_rand_facts(code_max, facts_count):
    facts = []
    for i in range(0, facts_count):
        facts.append(randint(0, code_max))
    return facts


# samples:
#print('simple_rules:', generate_simple_rules(100, 4, 5))
#print('random_rules:', generate_random_rules(100, 4, 5))
#print('stairway_rules:', generate_stairway_rules(100, 4, 5, ["or"]))
#print('ring_rules:', generate_ring_rules(100, 4, 5, ["or"]))

# generate rules and facts and check time
time_start = time()
N = 100000
M = 1000
max_fact_value = 100
log_oper_choice = ["and", "or", "not"]
rules = generate_simple_rules(max_fact_value, 4, N, log_oper_choice)
facts = generate_rand_facts(max_fact_value, M)
result = []
print("%d rules generated in %f seconds" % (N, time() - time_start))

# load and validate rules
# YOUR CODE HERE

# check facts vs rules
time_start = time()

facts_set = set(facts)
if len(facts_set) == max_fact_value+1:
    for rule in rules: # O(N)
        if 'and' in rule['if'].keys() or 'or' in rule['if'].keys():
            result.append(rule['then'])
elif 1==2:
    list_and = []
    list_or = []
    list_not = []
    sorted_facts = sorted(facts)
    for rule in rules:
        if 'and' in rule['if'].keys():
            list_and.append(rule)
        elif 'or' in rule['if'].keys():
            list_or.append(rule)
        elif 'not' in rule['if'].keys():
            list_not.append(rule)
else:
    pass
# YOUR CODE HERE

print("%d facts validated vs %d rules in %f seconds" % (M, N, time() - time_start))
#print("Result is ", result)
