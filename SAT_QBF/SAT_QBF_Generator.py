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
