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


def resolve2(facts_set_with_100, rules, rules_100=None):  # O(rules*rules_item_max_count)
    if not (rules_100 is None) and 100 not in facts_set_with_100: # добавить проверку по всем правилам
        facts_set_with_100 = add_100_in_facts(facts_set_with_100, rules_100)  # O(rules*rules_item_max_count)
    if type(facts_set_with_100) is list:
        facts_set_with_100 = set(facts_set_with_100)
    for rule in rules:  # O(rules)
        if check_rule(rule, facts_set_with_100): facts_set_with_100.add(rule['then'])  # O(rules_item_max_count)
    return facts_set_with_100


def resolve(facts, rules, max_fact_value, rules_100):
    facts_set = set(facts)  # O(facts)

    if len(facts_set) == max_fact_value + 1:
        #print("r1")
        return resolve1(facts, rules)  # O(rules)
    else:
        #print("r2")
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


def separate_rules(rules):
    not_dict = {}
    and_dict = {}
    or_dict = {}
    for rule in rules:  # O(rules)
        #print(rule)
        if 'and' in rule['if'].keys():
            #print(rule['then'], rule['if'], rule['then'] in and_dict)
            if rule['then'] in and_dict:
                and_dict[rule['then']].append(rule['if']['and'])
            else:
                and_dict[rule['then']] = [rule['if']['and']]
        elif 'or' in rule['if'].keys():
            #print(rule['then'], rule['if'], rule['then'] in or_dict)
            if rule['then'] in or_dict:
                or_dict[rule['then']].append(rule['if']['or'])
            else:
                or_dict[rule['then']] = [rule['if']['or']]
        elif 'not' in rule['if'].keys():
            #print(rule['then'], rule['if'], rule['then'] in not_dict)
            if rule['then'] in not_dict:
                not_dict[rule['then']].append(rule['if']['not'])
            else:
                not_dict[rule['then']] = [rule['if']['not']]
        else:
            raise KeyError
    return not_dict, and_dict, or_dict


def validate_sep_rules_not(not_dict, and_dict, or_dict):
    pp.pprint(not_dict)
    pp.pprint(or_dict)
    lag_rules = []
    for not_then in not_dict:
        for or_then in or_dict:
            for or_items in or_dict[or_then]:
                for or_item in or_items:
                    if or_item == not_then:
                        for not_items in not_dict[not_then]:
                            for not_item in not_items:
                                #print("!", or_then, not_then, not_item)
                                pass
    for not_then in not_dict:
        for not_then2 in not_dict:
            for not_items in not_dict[not_then2]:
                if not_then in not_items:
                    #print("!!!", not_dict[not_then], not_dict[not_then2])
                    pass

def validate_rules_not(rules):
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
            #print(comb)
            #print(comb_ind)
            for short_item in short:
                if comb_item[1] == short_item[0]:
                    if [comb_item[0], short_item[1]] not in comb:
                        ind = comb_ind[comb.index(comb_item)] + indexes[short.index(short_item)]
                        #print("ind", ind, type(ind))
                        if comb_item[0] == short_item[1]:
                            #print(wrong_rules, ind)
                            wrong_rules.update(ind)
                        else:
                            comb.append([comb_item[0], short_item[1]])
                            comb_ind.append(ind)
    slwr = sorted(list(wrong_rules))
    for revers_index_slwr in range(len(slwr) - 1, -1, -1):
        rules.remove(rules[slwr[revers_index_slwr]])
    return rules

"""
1 -> 2
2 -> 1

not 1 -> 2, not 2 -> 3, not 3 -> 1

1 or not 1
циклы исключить
порядок правил не влияет на факты!
"""

#generate rules and facts and check time
time_start = time()
N = 20  # 100000
M = 10  # 1000
#rules1 = generate_simple_rules(100, 4, N)
rules1 = [
            #{'if': {'or': [2]}, 'then': 1},
            {'if': {'not': [1, 24]}, 'then': 2},
            {'if': {'not': [2, 24]}, 'then': 3},
            {'if': {'not': [33, 234]}, 'then': 5},
            {'if': {'not': [3, 24]}, 'then': 1},
            #{'if': {'and': [12, 44]}, 'then': 102},
            #{'if': {'and': [93, 8]}, 'then': 102},
]
facts1 = generate_rand_facts(100, M)

pp = pprint.PrettyPrinter(indent=4)
print("%d rules generated in %f seconds" % (N,time()-time_start))
pp.pprint(rules1)
print(facts1)

#load and validate rules
# YOUR CODE HERE
validated_rules1, rules_with_100 = validate_rules_simple(rules1)

not_dict, and_dict, or_dict = separate_rules(rules1)

rules1 = validate_rules_not(rules1)


#pp.pprint(and_dict)

#check facts vs rules
time_start = time()

# YOUR CODE HERE
resolve(facts1, validated_rules1, 100, rules_with_100)

print("%d facts validated vs %d rules in %f seconds" % (M,N,time()-time_start))
