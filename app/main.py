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

def resolve(facts, rules, max_fact_value):
    result = []
    time_start = time()

    facts_set = set(facts)
    if len(facts_set) == max_fact_value + 1:
        #print("Easy")
        global easy_count
        global easy_time
        easy_count += 1
        for rule in rules:  # O(N)
            if 'and' in rule['if'].keys() or 'or' in rule['if'].keys():
                result.append(rule['then'])
        spend_time = time() - time_start
        #print("%d facts validated vs %d rules in %f seconds" % (len(facts), len(rules), spend_time))
        # print("Result is ", result)
        easy_time += spend_time
        return result

    else:
        print("Hard")
        global hard_count
        global hard_time
        hard_count += 1
        for rule in rules:
            if 'and' in rule['if'].keys():
                res = True
                for fact in rule['if']['and']:
                    if fact not in facts_set:
                        res = False
                        break


            elif 'or' in rule['if'].keys():
                res = False
                for fact in rule['if']['or']:
                    if fact in facts_set:
                        res = True
                        break

            elif 'not' in rule['if'].keys():
                res = True
                for fact in rule['if']['not']:
                    if fact in facts_set:
                        res = False
                        break

            else:
                raise TypeError

            if res: result.append(rule['then'])
        spend_time = time() - time_start
        #print("%d facts validated vs %d rules in %f seconds" % (len(facts), len(rules), spend_time))
        # print("Result is ", result)
        hard_time += spend_time
        return result


def generate_rules_and_facts(max_fact_value):
    time_start = time()
    N = 100000
    M = 1000
    log_oper_choice = ["and", "or", "not"]
    rules = generate_simple_rules(max_fact_value, 4, N, log_oper_choice)
    facts = generate_rand_facts(max_fact_value, M)
    #print("%d rules generated in %f seconds" % (N, time() - time_start))
    return rules, facts

# samples:
#print('simple_rules:', generate_simple_rules(100, 4, 5))
#print('random_rules:', generate_random_rules(100, 4, 5))
#print('stairway_rules:', generate_stairway_rules(100, 4, 5, ["or"]))
#print('ring_rules:', generate_ring_rules(100, 4, 5, ["or"]))

max_fact_value1 = 100
easy_time = 0
easy_count = 0
hard_time = 0
hard_count = 0

for i in range(200):

    # generate rules and facts and check time
    rules1, facts1 = generate_rules_and_facts(max_fact_value1)


    # load and validate rules
    # YOUR CODE HERE
    resolve(facts1, rules1, max_fact_value1)
    # check facts vs rules

print(easy_time/easy_count, hard_time/hard_count)

