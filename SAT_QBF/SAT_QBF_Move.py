

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

        return SAT_QBF_Formula(
            variables=new_vars,
            prefix=new_prefix,
            cnf=new_cnf,
            parents=[formula],
            is_qbf=formula.is_qbf
        )
    
    def add_clause(self, formula):
        """
        Example input output:

        Input:
        CNF: (x1 ∨ x2) ∧ (¬x1 ∨ x2)


        Output:
        CNF: (x1 ∨ x2) ∧ (¬x1 ∨ x2) ∧ (¬x1 ∨ ¬x2)
        """
        vars_ = formula.variables
        assert len(vars_) > 1
        # ensure distinct vars
        v1, v2 = random.sample(vars_, 2)`

        clause = [
            random.choice(['', '¬']) + v1,
            random.choice(['', '¬']) + v2
        ]

        new_cnf = formula.cnf + [clause]

        return SAT_QBF_Formula(
            variables=formula.variables,
            prefix=formula.prefix,
            cnf=new_cnf,
            parents=[formula],
            is_qbf=formula.is_qbf
        )

    def increase_clause_len(self, formula):
        """
        Example input output:

        Input:
        CNF: (x1 ∨ x2) ∧ (¬x1 ∨ x2) 

        Output:
        (x1 ∨ x2 ∨ x2) ∧ (¬x1 ∨ x2 ∨ ¬x1)
        """
        new_cnf = []
        vars_ = formula.variables

        for clause in formula.cnf:
            # Extract vars used (strip negation)
            used_vars = {lit.strip('¬') for lit in clause}

            # Find variables not already in clause
            available_vars = [v for v in vars_ if v not in used_vars]
