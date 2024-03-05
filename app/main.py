from random import choice, shuffle, randint
from time import time


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


# MY CODE HERE

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


def resolve1(facts, rules):
    for rule in rules:  # O(rules)
        if 'and' in rule['if'].keys() or 'or' in rule['if'].keys():
            facts.append(rule['then'])
    return facts


def resolve2(facts_set, rules):  # O(rules*rules_item_max_count)
    if type(facts_set) is list:
        facts_set = set(facts_set)
    for rule in rules:  # O(rules)
        if check_rule(rule, facts_set): facts_set.add(rule['then'])  # O(rules_item_max_count)
    return facts_set


def resolve(facts, rules, max_fact_value):  # O(rules*rules_item_max_count+facts)
    facts_set = set(facts)  # O(facts)

    if len(facts_set) == max_fact_value + 1:
        return resolve1(facts, rules)  # O(rules)
    else:
        return resolve2(facts_set, rules)  # O(rules*rules_item_max_count)


def generate_rules_and_facts(rules_count, rules_max_fact_value, rules_item_count, facts_count, facts_max_value):
    generated_rules = generate_simple_rules(rules_max_fact_value, rules_item_count, rules_count)
    generated_facts = generate_rand_facts(facts_max_value, facts_count)
    return generated_rules, generated_facts


def separate_rules(rules):
    not_dict = {}
    and_dict = {}
    or_dict = {}
    for rule in rules:  # O(rules)
        if 'and' in rule['if'].keys():
            if rule['then'] in and_dict:
                and_dict[rule['then']].append(rule['if']['and'])
            else:
                and_dict[rule['then']] = [rule['if']['and']]
        elif 'or' in rule['if'].keys():
            if rule['then'] in or_dict:
                or_dict[rule['then']].append(rule['if']['or'])
            else:
                or_dict[rule['then']] = [rule['if']['or']]
        elif 'not' in rule['if'].keys():
            if rule['then'] in not_dict:
                not_dict[rule['then']].append(rule['if']['not'])
            else:
                not_dict[rule['then']] = [rule['if']['not']]
        else:
            raise KeyError
    return not_dict, and_dict, or_dict


def inferences(rules):
    inferences_list = []
    for rule in rules:  # O(rules)
        inferences_list.append(rule['then'])
    return inferences_list


def validate_dependence(rules, wrong_rules=None):  # O(rules^3)
    if wrong_rules is None:
        wrong_rules = set()
    inferences_list = inferences(rules)  # O(rules)
    for rule in rules:  # O(rules)
        if 'and' in rule['if'].keys():
            for item in rule['if']['and']:  # O(rules_item_count)
                if item in inferences_list:  # O(rules)
                    wrong_rules.add(rules.index(rule))  # O(rules)
                    wrong_rules.add(inferences_list.index(item))  # O(rules)

        elif 'not' in rule['if'].keys():
            for item in rule['if']['not']:  # O(rules_item_count)
                if item in inferences_list:  # O(rules)
                    wrong_rules.add(rules.index(rule))  # O(rules)
                    wrong_rules.add(inferences_list.index(item))  # O(rules)

    return wrong_rules


def validate_rules_not(rules, wrong_rules=None):
    if wrong_rules is None:
        wrong_rules = set()
    short = []
    indexes = []
    for rule in rules:
        if 'not' in rule['if'].keys():
            for i in rule['if']['not']:
                short.append([i, rule['then']])
                indexes.append([rules.index(rule)])
    comb = short
    comb_ind = indexes
    for i in range(0, len(short)):
        for comb_item in comb:
            for short_item in short:
                if comb_item[1] == short_item[0]:
                    if [comb_item[0], short_item[1]] not in comb:
                        ind = comb_ind[comb.index(comb_item)] + indexes[short.index(short_item)]
                        if comb_item[0] == short_item[1]:
                            wrong_rules.update(ind)
                        else:
                            comb.append([comb_item[0], short_item[1]])
                            comb_ind.append(ind)
    return wrong_rules


def deletion_rules(rules, wrong_rules):  # O(NlogN) N=wrong_rules
    revers_sorted_list_wrong_rules = sorted(list(wrong_rules))[::-1]  # O(NlogN)
    for index in revers_sorted_list_wrong_rules:  # O(N)
        rules.pop(index)
    return rules


def validate_rules(rules):  # O(rules^3)
    wrong_rules = validate_dependence(rules)  # O(rules^3)
    rules = deletion_rules(rules, wrong_rules)  # O(NlogN) N=wrong_rules
    return rules


#generate rules and facts and check time
N = 100000
M = 1000
time_start = time()
rules1 = generate_simple_rules(100, 4, N)

print("%d rules generated in %f seconds" % (N, time()-time_start))

facts1 = generate_rand_facts(100, M)

#load and validate rules
time_start = time()

# YOUR CODE HERE
validated_rules1 = validate_rules(rules1)  # O(rules^3)

print("%d rules validated in %f seconds" % (N, time()-time_start))

#check facts vs rules
time_start = time()

# YOUR CODE HERE
facts1 = resolve(facts1, validated_rules1, 100)  # O(facts + rules*rules_item_max_count)

print("%d facts validated vs %d rules in %f seconds" % (M,N,time()-time_start))
