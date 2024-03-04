import main

class TestResolves:

    def test_1(self):
        rules = [
            {'if': {'or': [93, 8, 57, 16]}, 'then': 101},
            {'if': {'not': [21, 15]}, 'then': 107},
            {'if': {'and': [100, 2]}, 'then': 102},
        ]
        facts = [93, 45, 44, 12]
        max_fact_value = 100
        validated_rules1, rules_with_100 = main.validate_rules_simple(rules)

        add_fact = main.resolve(facts, rules, max_fact_value, rules_with_100)
        facts.extend(add_fact)

        assert set(facts) == {93, 101, 45, 44, 12, 107}


    def test_100(self):
        rules = [
            {'if': {'and': [100, 44]}, 'then': 102},
            {'if': {'or': [93, 8, 57, 16]}, 'then': 101},
            {'if': {'not': [21, 15]}, 'then': 100},
        ]
        facts = [93, 45, 44, 12]

        facts.extend(main.resolve(facts, rules))

        assert set(facts) == {12, 44, 45, 93, 100, 101, 102}


    def test_not(self):
        rules = [
            {'if': {'or': [93, 8]}, 'then': 21},
            {'if': {'not': [21, 15]}, 'then': 100},
        ]
        facts = [93, 60]

        facts.extend(main.resolve(facts, rules))

        assert set(facts) == {93, 60, 21, 100}


    def test_not2(self):
        rules = [
            {'if': {'not': [1]}, 'then': 2},
            {'if': {'or': [2]}, 'then': 1},
        ]
        facts = [93, 60]

        facts.extend(main.resolve(facts, rules))

        assert set(facts) == {93, 60}


    def test_revers_not2(self):
        rules = [
            {'if': {'or': [2]}, 'then': 1},
            {'if': {'not': [1]}, 'then': 2},
        ]
        facts = [93, 60]

        facts.extend(main.resolve(facts, rules))

        assert set(facts) == {93, 60}


    def test_twice(self):
        rules = [
            {'if': {'and': [12, 44]}, 'then': 102},
            {'if': {'or': [93, 8]}, 'then': 102},
        ]
        facts = [93, 45, 44, 12]

        facts.extend(main.resolve(facts, rules))

        assert set(facts) == {93, 45, 44, 12, 102}  # not {93, 45, 44, 12, 102, 102}


def test_add_100_in_facts():
    rules = [
        {'if': {'or': [93, 8, 57, 16]}, 'then': 100},
    ]
    facts = [93, 45, 44, 12]
    facts_set = set(facts)

    facts_set = main.add_100_in_facts(facts_set, rules)

    assert facts_set == {93, 45, 44, 12, 100}
