import main


class TestValidators:

    def test_base(self):
        rules_in = [
            {'if': {'or': [93, 8, 57, 16]}, 'then': 101},
            {'if': {'not': [21, 15]}, 'then': 107},
            {'if': {'and': [100, 2]}, 'then': 102},
        ]
        rules_out = [
            {'if': {'or': [93, 8, 57, 16]}, 'then': 101},
            {'if': {'not': [21, 15]}, 'then': 107},
            {'if': {'and': [100, 2]}, 'then': 102},
        ]

        validated_rules = main.validate_rules(rules_in)

        assert rules_out == validated_rules


    def test_not_contradiction(self):
        rules_in = [
            {'if': {'not': [1, 2, 3]}, 'then': 1},
        ]
        rules_out = []

        validated_rules = main.validate_rules(rules_in)

        assert rules_out == validated_rules


    def test_not_contradiction1(self):
        rules_in = [
            {'if': {'not': [1, 5]}, 'then': 2},
            {'if': {'not': [2, 6]}, 'then': 3},
            {'if': {'not': [3, 7]}, 'then': 1},
        ]
        rules_out = []

        validated_rules = main.validate_rules(rules_in)

        assert rules_out == validated_rules


    def test_not_contradiction2(self):
        rules_in = [
            {'if': {'not': [1, 5]}, 'then': 2},
            {'if': {'not': [2, 6]}, 'then': 3},
        ]
        rules_out = []

        validated_rules = main.validate_rules(rules_in)

        assert rules_out == validated_rules


    def test_not_contradiction3(self):
        rules_in = [
            {'if': {'not': [1, 5]}, 'then': 2},
            {'if': {'not': [2, 6]}, 'then': 3},
        ]
        rules_out = []

        validated_rules = main.validate_rules(rules_in)

        assert rules_out == validated_rules


    def test_not_contradiction4(self):
        rules_in = [
            {'if': {'or': [1, 5]}, 'then': 2},
            {'if': {'not': [2, 6]}, 'then': 3},
        ]
        rules_out = []

        validated_rules = main.validate_rules(rules_in)

        assert rules_out == validated_rules


    def test_and_contradiction(self):
        rules_in = [
            {'if': {'and': [1, 2, 3]}, 'then': 1},
        ]
        rules_out = []

        validated_rules = main.validate_rules(rules_in)

        assert rules_out == validated_rules


    def test_not2(self):
        rules_in = [
            {'if': {'or': [2, 5]}, 'then': 1},
            {'if': {'not': [1, 6]}, 'then': 2},
        ]
        rules_out = []

        validated_rules = main.validate_rules(rules_in)

        assert rules_out == validated_rules


    def test_reverse_not2(self):
        rules_in = [
            {'if': {'not': [1, 6]}, 'then': 2},
            {'if': {'or': [2, 5]}, 'then': 1},
        ]
        rules_out = []

        validated_rules = main.validate_rules(rules_in)

        assert rules_out == validated_rules



class TestResolves:

    def test_1(self):
        rules = [
            {'if': {'or': [93, 8, 57, 16]}, 'then': 101},
            {'if': {'not': [21, 15]}, 'then': 107},
            {'if': {'and': [100, 2]}, 'then': 102},
        ]
        facts = [93, 45, 44, 12]
        max_fact_value = 100

        validated_rules = main.validate_rules(rules)

        add_fact = main.resolve(facts, validated_rules, max_fact_value)
        facts.extend(add_fact)

        assert set(facts) == {93, 101, 45, 44, 12, 107}

