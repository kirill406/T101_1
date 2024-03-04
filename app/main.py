from random import choice, shuffle, randint
from time import time
import pprint


def generate_simple_rules(rules_max_fact_value, rules_item_max_count, rules_count, log_op_choice=None):
    if log_op_choice is None:
        log_op_choice = ["and", "or", "not"]
    rules = []
    if rules_item_max_count < 2:
        rules_item_max_count = 2
    for j in range(0, rules_count):
        log_op = choice(log_op_choice)  # not means and-not (neither)
        n_items = randint(2, rules_item_max_count)
        items = []
        for i in range(0, n_items):
            items.append(randint(1, rules_max_fact_value))  # [1...rules_max_fact_value]
        rule = {
            'if': {
                log_op: items
            },
            'then': rules_max_fact_value + j  # [rules_max_fact_value...rules_max_fact_value+rules_count-1]
        }
        rules.append(rule)
    shuffle(rules)
    return rules


def generate_stairway_rules(code_max, rules_item_max_count, n_generate, log_op_choice=None):
    if log_op_choice is None:
        log_op_choice = ["and", "or", "not"]
    rules = []
    if rules_item_max_count < 2:
        rules_item_max_count = 2
    for j in range(0, n_generate):
        log_op = choice(log_op_choice)  # not means and-not (neither)
        n_items = randint(2, rules_item_max_count)
        items = []
        for i in range(0, n_items):
            items.append(i + j)
        rule = {
            'if': {
                log_op: items
            },
            'then': i + j + 1  # 1:rules_item_max_count+n_generate
        }
        rules.append(rule)
    shuffle(rules)
    return rules


def generate_ring_rules(code_max, n_max, n_generate, log_op_choice=None):
    if log_op_choice is None:
        log_op_choice = ["and", "or", "not"]
    rules = generate_stairway_rules(code_max, n_max, n_generate - 1, log_op_choice)
    log_op = choice(log_op_choice)  # not means and-not (neither)
    if n_max < 2:
        n_max = 2
    n_items = randint(2, n_max)
    items = []
    for i in range(0, n_items):
        items.append(code_max - i)
    rule = {
        'if': {
            log_op: items
        },
        'then': 0
    }
    rules.append(rule)
    shuffle(rules)
    return rules


def generate_random_rules(code_max, n_max, n_generate, log_op_choice=None):
    if log_op_choice is None:
        log_op_choice = ["and", "or", "not"]
    rules = []
    if n_max < 2:
        n_max = 2
    for j in range(0, n_generate):

        log_op = choice(log_op_choice)  # not means and-not (neither)

        n_items = randint(2, n_max)
        items = []
        for i in range(0, n_items):
            items.append(randint(1, code_max))
        rule = {
            'if': {
                log_op: items
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


def generate_rand_facts(facts_max_value, facts_count):
    facts = []
    for i in range(0, facts_count):
        facts.append(randint(0, facts_max_value))
    return facts


# New functions


def check_rule(rule, facts_set):  # O(rules_item_max_count)
    if 'and' in rule['if'].keys():
        for fact in rule['if']['and']:
            if fact not in facts_set:
                return False
        return True

    elif 'or' in rule['if'].keys():
        for fact in rule['if']['or']:
            if fact in facts_set:
                return True
        return False

    elif 'not' in rule['if'].keys():
        for fact in rule['if']['not']:
            if fact in facts_set:
                return False
        return True

    else:
        raise KeyError


def one_rules_loop(rules, facts_set):  # O(rules*rules_item_max_count)
    added_facts = []
    for rule in rules:  # O(rules)
        if check_rule(rule, facts_set):  # O(rules_item_max_count)
            added_facts.append(rule['then'])
    return added_facts


def one_rules_loop_100(rules_100, facts_set):  # O(rules*rules_item_max_count)
    for rule in rules_100:  # O(rules_100)
        if check_rule(rule, facts_set):  # O(rules_item_max_count)
            return True
    return False


def add_100_in_facts(facts_set, rules_100):  # O(rules*rules_item_max_count)
    if 100 not in facts_set:
        if one_rules_loop_100(rules_100, facts_set):  # O(rules*rules_item_max_count)
            facts_set.add(100)
    return facts_set


def resolve1(facts, rules):
    for rule in rules:  # O(rules)
        if 'and' in rule['if'].keys() or 'or' in rule['if'].keys():
            facts.append(rule['then'])
    return facts


def resolve2(facts_set_with_100, rules):  # O(rules*rules_item_max_count)
    for rule in rules:  # O(rules)
        if check_rule(rule, facts_set_with_100): facts_set_with_100.add(rule['then'])  # O(rules_item_max_count)
    return facts_set_with_100


def resolve(facts, rules, max_fact_value, rules_100):
    facts_set = set(facts)  # O(facts)

    if len(facts_set) == max_fact_value + 1:
        return resolve1(facts, rules)  # O(rules)
    else:
        facts_set = add_100_in_facts(facts_set, rules_100)  # O(rules*rules_item_max_count)
        return resolve2(facts_set, rules)  # O(rules*rules_item_max_count)


def generate_rules_and_facts(rules_count, rules_max_fact_value, rules_item_count, facts_count, facts_max_value):
    generated_rules = generate_simple_rules(rules_max_fact_value, rules_item_count, rules_count)
    generated_facts = generate_rand_facts(facts_max_value, facts_count)
    return generated_rules, generated_facts


def validate_rules_simple(rules):
    rules_100 = []
    for rule in rules:
        if rule['then'] == 100:
            rules_100.append(rule)
    return rules, rules_100


#generate rules and facts and check time
time_start = time()
N = 20  # 100000
M = 10  # 1000
rules1 = generate_simple_rules(100, 4, N)
facts1 = generate_rand_facts(100, M)
pp = pprint.PrettyPrinter(indent=4)
print("%d rules generated in %f seconds" % (N,time()-time_start))
pp.pprint(rules1)
print(facts1)

#load and validate rules
# YOUR CODE HERE
validated_rules1, rules_with_100 = validate_rules_simple(rules1)

#check facts vs rules
time_start = time()

# YOUR CODE HERE
resolve2(facts1, validated_rules1)

print("%d facts validated vs %d rules in %f seconds" % (M,N,time()-time_start))

