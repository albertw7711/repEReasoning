

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

            # If all vars are used already, we can't increase clause length
            if not available_vars:
                new_cnf.append(clause)
                continue

            # Choose one unused var and random negation
            new_var = random.choice(available_vars)
            new_lit = random.choice(['', '¬']) + new_var

            # Append and shuffle (optional)
            new_clause = clause + [new_lit]
            random.shuffle(new_clause)
            new_cnf.append(new_clause)

        return SAT_QBF_Formula(
            variables=formula.variables,
            prefix=formula.prefix,
            cnf=new_cnf,
            parents=[formula],
            is_qbf=formula.is_qbf
        )
    
    def inject_reusable(self, formula, reusable):
        """
        Input output example:

        Input
        # Original formula
        ∃ x1 ∃ x2 : (x1 ∨ ¬x2)

        # Reusable component
        ∀ x ∃ y : (¬x ∨ y) ∧ (x ∨ ¬y)

        Output
        ∃ x1 ∃ x2 ∀ x3 ∃ x4 : 
        (x1 ∨ ¬x2) ∧ (¬x3 ∨ x4) ∧ (x3 ∨ ¬x4)
        """
        # Step 1: Create new variable names
        existing_vars = set(formula.variables)
        mapping = {}
        new_vars = []

        for old_var in reusable.variables:
            base = old_var.strip('x') if old_var.startswith('x') else old_var
            new_var = f"x{len(existing_vars) + len(mapping) + 1}"
            mapping[old_var] = new_var
            new_vars.append(new_var)

        # Step 2: Rename reusable CNF
        renamed_cnf = []
        for clause in reusable.cnf:
            renamed_clause = []
            for lit in clause:
                is_neg = lit.startswith('¬')
                var = lit.strip('¬')
                renamed_lit = ('¬' if is_neg else '') + mapping[var]
                renamed_clause.append(renamed_lit)
            renamed_cnf.append(renamed_clause)

        # Step 3: Rename reusable prefix
        renamed_prefix = [(q, mapping[v]) for q, v in reusable.prefix]

        # Step 4: Merge
        new_vars_all = formula.variables + new_vars
        new_cnf = formula.cnf + renamed_cnf
        new_prefix = formula.prefix + renamed_prefix

