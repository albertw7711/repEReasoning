from sympy import *
from sym_objs import *
import random
import math

class SymDifferentiationGenerator:
    def __init__(self, product_max=2**30, chain_max=2**30,
                 section_length=10,
                 is_poly=false, is_trig=false, is_rec_trig=false,
                 is_inv_trig=false, is_inv_rec_trig=false, is_exp=false, is_log=false,
                 symbol=symbols("x")
                 ):
        self.product_max = product_max
        self.chain_max = chain_max
        self.level_max = 2**(math.ceil(1.5*product_max))
        self.section_length = section_length

        self.fns = []
        if is_trig:
            self.fns.extend(TRIGS)
        if is_rec_trig:
            self.fns.extend(REC_TRIGS)
        if is_inv_trig:
            self.fns.extend(INV_TRIGS)
        if is_inv_rec_trig:
            self.fns.extend(INV_REC_TRIGS)
        if is_exp:
            self.fns.append(exp)
        if is_log:
            self.fns.append(log)
        if is_poly:
            self.fns.append(symbol)
        self.fns = [f(symbol) if f.is_Function else f for f in self.fns]
        self.symbol = symbol

        self.generating_db = []
        self.output_db = []
        self.db_init()

    def db_init(self):
        gen_level0 = []
        for _ in range(2**self.section_length):
            fn = random.choice(self.fns)
            if isinstance(fn, Symbol):
                fn = fn ** random.randint(-100, 100)
            deri = diff(fn, self.symbol)
            node = Node(p1=None, p2=None, rule=None, expr=fn, deri=deri)
            gen_level0.append(node)
        out_level0 = random.sample(gen_level0, k=self.section_length)
        for node in out_level0:
            node.is_out = True
            node.is_solved = True
        self.generating_db.append(gen_level0)
        self.output_db.append(out_level0)

    def generate_curriculum(self):
        current_level = 1
        while current_level < self.level_max:
            gen_levelc = []
