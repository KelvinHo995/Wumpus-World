from collections import defaultdict
import json

class InferenceEngine:
    def __init__(self):
        pass
    
    def parse_rules(self, path):
        with open(path) as f:
            raw = json.load(f)
        
        parsed_rules = []

        for rule in raw:
            parsed_if = [(pred[0], tuple(pred[1])) for pred in rule["if"]]
            if "then" in rule:
                parsed_then = (rule["then"][0], tuple(rule["then"][1]))
                parsed_rules.append({
                    "if": parsed_if,
                    "then": parsed_then
                })
            else:
                parsed_remove = (rule["remove"][0], tuple(rule["remove"][1]))
                parsed_rules.append({
                    "if": parsed_if,
                    "remove": parsed_remove
                })

        return parsed_rules

    def unify(self, expression, fact, substitution={}):
        if expression[0] != fact[0]:
            return
        
        assign = substitution.copy()

        for var, const in zip(expression[1], fact[1]):
            if var not in assign: # Not assigned yet
                assign[var] = const
            elif assign[var] != const: # If var is already assigned then check if var is assigned to const, if not then conflict
                return
            
        return assign
    
    def substitute(self, expression, substitution):
        """
        Substitute the substitution into the expression
        Returns the expression with the variables substituted/stays the same if no change
        """
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
        """
        Returns all of the substitutions available for the conditions
        """
        num_match = defaultdict(int)
        for fact in facts:
            num_match[fact[0]] += 1
        
        sorted_conditions = sorted(conditions, key=lambda condition: num_match[condition[0]])

        return self.match_conditions(sorted_conditions, facts)

    def forward_chaining(self, rules, facts):
        inferred = set(facts)

        while True:
            new_facts = set()
            to_remove = set()
            changed = False

            for rule in rules:
                premise = rule["if"]
                if "then" in rule:
                    consequence = rule["then"]
                else:
                    consequence = rule["remove"]

                matches = self.match(premise, inferred)

                for substitution in matches:
                    new_literal = self.substitute(consequence, substitution)
        
                    if "remove" in rule:
                        if new_literal in inferred:
                            to_remove.add(new_literal)
                            changed = True
                        elif new_literal in new_facts:
                            new_facts.discard(new_literal)
                            changed = True
                    elif new_literal not in inferred and new_literal not in new_facts:
                        new_facts.add(new_literal)
                        changed = True

            if not changed:
                break

            inferred -= to_remove
            inferred |= new_facts

        return inferred

    def get_safe_tiles(self, inferred):
        return set(tuple(map(int, fact[1])) for fact in inferred if fact[0] == "Safe")

    def get_visited_tiles(self, inferred):
        return set(tuple(map(int, fact[1])) for fact in inferred if fact[0] == "Visited")

    def get_unsafe_tiles(self, inferred, visited_tiles=None):
        if visited_tiles is None:
            visited_tiles = self.get_visited_tiles(inferred)
            


if __name__ == "__main__":
    facts = [
        ("PossiblePit", ("1", "1")),
        ("NoPit", ("1", "1"))
    ]

    engine = InferenceEngine()
    rules = engine.parse_rules("rules.json")
    print(engine.forward_chaining(rules, facts))