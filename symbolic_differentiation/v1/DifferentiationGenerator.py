from sympy import *
from Generator import Generator
from objs import *
from copy import deepcopy
import numpy as np

class DifferentiationGenerator(Generator):
    ATTEMPT_LIMIT = 30
    NUM_FN_TYPE = 7
    NUM_WIDE_TYPE = 2
    ARG_WEIGHTS = [10, 1, 5, 3, 1, 2, 3, 4, 5, 2, 2, 0, 0]
    FN_WEIGHTS = [2, 2, 1, 1, 1, 2, 2]
    def __init__(self):
        self.generating_db = []

    def generate_theorem(self):
        pass

    def generate_theorem_native(self,
                         derivative_degree=1,
                         num_sum: int=1, product_depth: int=0, chain_depth: int=0,
                         is_poly=false, is_trig=false, is_rec_trig=false,
                         is_inv_trig=false, is_inv_rec_trig=false, is_exp=false, is_log=false,
                         is_product_wide=false, is_chain_wide=false,
                         is_batch: bool=false):
        fns = []
