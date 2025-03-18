

class SAT_QBF_Move:
    def __init__(self):
        self.move_registry = {
            "add_variable": self.add_variable,
            "add_clause": self.add_clause,
            "increase_clause_len": self.increase_clause_len,
            "extend_prefix": self.extend_prefix,
            "inject_reusable": self.inject_reusable,
            "shuffle_clauses": self.shuffle_clauses,
            "rename_vars": self.rename_vars,
        }

    def apply(self, formula, move_name):
        assert move_name in self.move_registry, f"Unknown move: {move_name}"
        return self.move_registry[move_name](formula)
    
    def add_variable(self, formula):
        """
        Example input output:

        Input formula:
        Variables: ['x1', 'x2']
        CNF: (x1 ∨ x2) ∧ (¬x1 ∨ x2)

        Output formula:
        Variables: ['x1', 'x2', 'x3']
        CNF: (x1 ∨ x2) ∧ (¬x1 ∨ x2) ∧ (¬x2 ∨ x3)
        """
        new_var = f"x{len(formula.variables) + 1}"
        new_vars = formula.variables + [new_var]

        new_prefix = formula.prefix + [('∃', new_var)] if formula.is_qbf else [('∃', v) for v in new_vars]

        new_clause = [
            random.choice(['', '¬']) + random.choice(new_vars),
            random.choice(['', '¬']) + new_var
        ]

        new_cnf = formula.cnf + [new_clause]
