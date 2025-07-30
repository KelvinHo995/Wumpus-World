from collections import defaultdict

class InferenceEngine:
    def __init__(self):
        pass

    def unify(self, expression, fact, substitution={}):
        if expression[0] != fact[0]:
            return
        assign = substitution.copy()
        for var, const in zip(expression[1], fact[1]):
            if var not in assign:
                assign[var] = const
            elif assign[var] != const:
                return
        return assign

    def substitute(self, expression, substitution):
        return (expression[0], tuple(substitution.get(var, var) for var in expression[1]))

    def match_conditions(self, conditions, facts, index=0, current_subs={}):
        if index == len(conditions):
            return [current_subs]
        current_condition = conditions[index]
        matches = []
        for fact in facts:
            next_subs = self.unify(current_condition, fact, current_subs)
            if next_subs:
                matches += self.match_conditions(conditions, facts, index + 1, next_subs)
        return matches

    def match(self, conditions, facts):
        num_match = defaultdict(int)
        for fact in facts:
            num_match[fact[0]] += 1
        sorted_conditions = sorted(conditions, key=lambda condition: num_match[condition[0]])
        return self.match_conditions(sorted_conditions, facts)

    def forward_chaining(self, rules, facts):
        inferred = set(facts)
        while True:
            new_facts = set()
            for rule in rules:
                premise = rule["if"]
                consequence = rule["then"]
                matches = self.match(premise, inferred)
                for substitution in matches:
                    new_fact = self.substitute(consequence, substitution)
                    if new_fact not in inferred and new_fact not in new_facts:
                        new_facts.add(new_fact)
            if not new_facts:
                break
            inferred.update(new_facts)
        return inferred
