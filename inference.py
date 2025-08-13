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

    def make_index(self, KB):
        """Convert a flat KB set into an indexed KB dict."""
        index = defaultdict(set)
        for pred, arg in KB:
            index[pred].add(arg)
        return index
    
    def add_fact(self, index, fact):
        """Add a single fact to the indexed KB."""
        pred, arg = fact
        index[pred].add(arg)

    def remove_fact(self, index, fact):
        """Remove a single fact from the indexed KB."""
        pred, arg = fact
        if arg in index[pred]:
            index[pred].remove(arg)
            if not index[pred]:  # clean up empty entries
                del index[pred]

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

        pred = current_condition[0]
        if pred not in facts:
            return []
        
        for args in facts[pred]:
            fact = (pred, args)
            next_subs = self.unify(current_condition, fact, current_subs)
            if next_subs:
                matches += self.match_conditions(conditions, facts, index + 1, next_subs)
        
        return matches
    
    def match(self, conditions, facts):
        """
        Returns all of the substitutions available for the conditions
        """
        num_match = defaultdict(int)
        for pred, args_set in facts.items():
            num_match[pred] = len(args_set)
        
        sorted_conditions = sorted(conditions, key=lambda condition: num_match[condition[0]])

        return self.match_conditions(sorted_conditions, facts)

    def forward_chaining(self, rules, inferred, deleted):
        seen = {(p, args) for p, s in inferred.items() for args in s}
        delta = {p: set(s) for p, s in inferred.items()}
        delta_preds = set(delta.keys())

        while delta:
            new_facts = set()
            to_remove = set()

            for rule in rules:
                premise = rule["if"]
                if "then" in rule:
                    consequence = rule["then"]
                else:
                    consequence = rule["remove"]

                if not any(lit[0] in delta_preds for lit in premise):
                    continue

                matches = self.match(premise, inferred)

                for substitution in matches:
                    new_literal = self.substitute(consequence, substitution)

                    if "remove" in rule:
                        if new_literal[0] in inferred and new_literal[1] in inferred[new_literal[0]]:
                            to_remove.add(new_literal)
                        elif new_literal in new_facts:
                            new_facts.discard(new_literal)
                    else:
                        if (
                            new_literal not in seen
                            and new_literal not in new_facts
                            and new_literal not in deleted
                            and new_literal not in to_remove
                        ):
                            new_facts.add(new_literal)

            if not new_facts and not to_remove:
                break
            
            for fact in to_remove:
                self.remove_fact(inferred, fact)
            deleted |= to_remove

            for fact in new_facts:
                self.add_fact(inferred, fact)
            seen |= new_facts

            delta = {}
            for pred, args in new_facts:
                delta.setdefault(pred, set()).add(args)
            delta_preds = set(delta.keys())

        return inferred

    def get_stench_tile(self, inferred):
        return inferred.get("Stench", set())

    def get_safe_tiles(self, inferred):
        walls = inferred.get("Wall", set())
        safe = inferred.get("Safe", set())
        return safe - walls

    def get_visited_tiles(self, inferred):
        return inferred.get("Visited", set())

    def get_frontier_tiles(self, visited_tiles, inferred):
        walls = inferred.get("Wall", set())
        frontier = set()
        for tile in visited_tiles:
            for dx, dy in [(0,1), (1,0), (0,-1), (-1,0)]:
                neighbor = (tile[0] + dx, tile[1] + dy)
                if neighbor not in visited_tiles and neighbor not in walls:
                    frontier.add(neighbor)
        return frontier
    
if __name__ == "__main__":
    facts = [
        ("PossiblePit", ("1", "1")),
        ("NoPit", ("1", "1"))
    ]

    engine = InferenceEngine()
    rules = engine.parse_rules("rules.json")
    print(engine.forward_chaining(rules, facts))