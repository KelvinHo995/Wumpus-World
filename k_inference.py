from collections import defaultdict

class InferenceEngine:
    def unify(self, expr, fact, substitution={}):
        if expr[0] != fact[0]:
            return
        assign = substitution.copy()
        for var, const in zip(expr[1], fact[1]):
            if var not in assign:
                assign[var] = const
            elif assign[var] != const:
                return
        return assign

    def substitute(self, expr, substitution):
        return (expr[0], tuple(substitution.get(v, v) for v in expr[1]))

    def match_conditions(self, conditions, facts, index=0, current_subs={}):
        if index == len(conditions):
            return [current_subs]
        current = conditions[index]
        matches = []
        for fact in facts:
            next_subs = self.unify(current, fact, current_subs)
            if next_subs:
                matches += self.match_conditions(conditions, facts, index+1, next_subs)
        return matches

    def match(self, conditions, facts):
        num_match = defaultdict(int)
        for fact in facts:
            num_match[fact[0]] += 1
        sorted_conds = sorted(conditions, key=lambda c: num_match[c[0]])
        return self.match_conditions(sorted_conds, facts)

    def forward_chaining(self, rules, facts):
        inferred = set(facts)
        while True:
            new_facts = set()
            for rule in rules:
                matches = self.match(rule["if"], inferred)
                for subs in matches:
                    new_fact = self.substitute(rule["then"], subs)
                    if new_fact not in inferred and new_fact not in new_facts:
                        new_facts.add(new_fact)
            if not new_facts:
                break
            inferred.update(new_facts)
        return inferred
