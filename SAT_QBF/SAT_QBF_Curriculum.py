class SAT_QBF_Formula:
    def __init__(self, variables, prefix, cnf, parents=[], is_qbf=True):
        self.variables = variables # ['x1', 'x2', ...]
        self.prefix = prefix # [('∃', 'x1'), ('∀', 'x2'), ...]
        self.cnf = cnf # List of clauses, e.g. [['x1', '¬x2'], ...]
        self.parents = parents
        self.is_qbf = is_qbf

        if is_qbf:
            self.prefix = prefix if prefix else [('∃', v) for v in variables]
        else:
            self.prefix = [('∃', v) for v in variables]  # SAT default
    
    def to_str(self):
        """
        example return: ∃ x1 ∃ x2 : (x1 ∨ x2) ∧ (¬x1 ∨ x2)
        """
        matrix_str = " ∧ ".join(["(" + " ∨ ".join(clause) + ")" for clause in self.cnf])
        
        if self.is_qbf:
            prefix_str = " ".join([f"{q} {v}" for q, v in self.prefix])
            return f"{prefix_str} : {matrix_str}"
        else:
