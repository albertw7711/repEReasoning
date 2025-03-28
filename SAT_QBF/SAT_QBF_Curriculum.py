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
            return matrix_str  # omit prefix for SAT
    
    def print_expression(self,):
        expression_str = self.to_str()
        print(expression_str)
    
    def count_alternations(self, prefix):
        """
        Count the number of quantifier alternations in a QBF prefix.
        
        Example:
        Input: [('∃', 'x1'), ('∃', 'x2'), ('∀', 'x3'), ('∃', 'x4')]
        Output: 2  (∃ → ∀, ∀ → ∃)
        """
        if not prefix:
            return 0

        count = 0
        prev_q = prefix[0][0]
        
        for q, _ in prefix[1:]:
            if q != prev_q:
                count += 1
                prev_q = q

        return count

    def get_hardness(self):
        return {
            "num_vars": len(self.variables),
            "num_clauses": len(self.cnf),
            "clause_len_avg": round(sum(len(c) for c in self.cnf) / len(self.cnf)),
            "alt_depth": self.count_alternations(self.prefix),
            "num_subformulas": len(self.parents)
        }

class SAT_QBF_Curriculum:
    def __init__(self,):
        self.derivation_tree = []
    
    def append_node(self, formula):
        self.derivation_tree.append(formula)
    
    def print_curriculum_tree(self):
        for i, formula in enumerate(self.derivation_tree):
            print(f"\nFormula {i}:")
            formula.print_expression()
            print("Hardness:", formula.get_hardness())


class ReusableComponent:
    def __init__(self, name, variables, prefix, cnf, is_qbf=True):
        self.name = name
        self.variables = variables
        self.prefix = prefix
        self.cnf = cnf
        self.is_qbf = is_qbf


# And in your generator:
