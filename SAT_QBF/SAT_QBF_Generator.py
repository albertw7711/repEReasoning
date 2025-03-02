import sys
import random

sys.path.append('../')
from Generator import Generator

class SAT_QBF_Generator(Generator):
    def __init__(self, is_qbf=True):
        self.is_qbf = is_qbf
    
    def generate_clause(self, variables, length=2):
