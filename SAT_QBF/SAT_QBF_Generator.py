import sys
import random

sys.path.append('../')
from Generator import Generator

class SAT_QBF_Generator(Generator):
    def __init__(self, is_qbf=True):
        self.is_qbf = is_qbf
    
    def generate_clause(self, variables, length=2):
        return [
            random.choice(['', '¬']) + random.choice(variables)
            for _ in range(length)
        ]

    def generate_cnf(self, variables, num_clauses=2, clause_len=2):
        return [self.generate_clause(variables, clause_len) for _ in range(num_clauses)]

    def create_base_formula(self,):
        variables = ["x1", "x2"]
        if self.is_qbf:
            # Simple QBF prefix: ∃ x1 ∃ x2
            prefix = [('∃', 'x1'), ('∃', 'x2')]
        else:
            # For SAT, use existential-only prefix (∃ for all vars, even if unused)
            prefix = [('∃', v) for v in variables]

        # Small CNF
        cnf = self.generate_cnf(variables, num_clauses=2, clause_len=2)
        return SAT_QBF_Formula(
            variables=variables,
            prefix=prefix,
            cnf=cnf,
            parents=[],
            is_qbf=self.is_qbf
        )

    
    def generate_theorem(self):
        pass
    
    def generate_curriculum(self, n_formulas, max_hardness):
        curriculum = SAT_QBF_Curriculum()
        generated_hashes = set()

        # Step 1: Base formula
        current = self.create_base_formula()
        curriculum.append_node(current)
        generated_hashes.add(current.to_str())

        # Step 2: Climb phase — reach max_hardness
        while current.get_hardness() != max_hardness:
            moves = valid_moves(current.get_hardness(), max_hardness)
            if not moves:
                break  # can't increase further
            move = random.choice(moves)
            next_formula = apply_move(current, move)

            # check for uniqueness
            if next_formula.to_str() in generated_hashes:
                continue

            curriculum.append_node(next_formula)
            generated_hashes.add(next_formula.to_str())
            current = next_formula

            if len(curriculum.derivation_tree) == n_formulas:
                return curriculum

        # Step 3: Explore phase — stay at max hardness
        while len(curriculum.derivation_tree) < n_formulas:
            move = random.choice(["shuffle_clauses", "inject_alt_subformula", "rename_vars"])  # lateral moves
            candidate = apply_move(current, move)

            if candidate.to_str() in generated_hashes:
                continue
            if candidate.get_hardness() != max_hardness:
                continue

            curriculum.append_node(candidate)
            generated_hashes.add(candidate.to_str())

        return curriculum

    
    def generate_problem_prompt(self):
