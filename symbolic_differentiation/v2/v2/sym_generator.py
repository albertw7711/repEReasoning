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
        self.generating_db.append(gen_level0)
        self.output_db.append(out_level0)

    def generate_curriculum(self):
        current_level = 1
        while current_level < self.level_max:
            gen_levelc = []
            if current_level % 2 == 0:
                if current_level & (current_level-1) == 0:
                    num_product = floor(0.6 * self.section_length*2)
                    num_chain = floor(0.3 * self.section_length*2)
                    num_sum = self.section_length*2 - num_product - num_chain
                else:
                    num_product = 0
                    num_chain = floor(0.5 * self.section_length*2)
                    num_sum = self.section_length*2 - num_chain
                while num_sum > 0:
                    p1_level = random.randint(0, current_level-1)
                    p2_level = current_level-1 - p1_level
                    p1 = random.choice(self.generating_db[p1_level])
                    p2 = random.choice(self.generating_db[p2_level])
                    node = Node.create(p1, p2, 0)
                    if (node.product_count > self.product_max) or (node.chain_count > self.chain_max):
                        continue
                    gen_levelc.append(node)
                    num_sum -= 1
                while num_product > 0:
                    p1_level = random.randint(0, int(math.log(current_level, 2))-1)
                    p2_level = int(math.log(current_level, 2))-1 - p1_level
                    p1 = random.choice(self.generating_db[p1_level])
                    p2 = random.choice(self.generating_db[p2_level])
                    node = Node.create(p1, p2, 1)
                    if (node.product_count > self.product_max) or (node.chain_count > self.chain_max):
                        continue
                    gen_levelc.append(node)
                    num_product -= 1
                while num_chain > 0:
                    p1_level = 0
                    p2_level = int(current_level/2)-1
                    p1 = random.choice(self.generating_db[p1_level])
                    while not p1.expr.is_Function:
                        p1 = random.choice(self.generating_db[p1_level])
                    p2 = random.choice(self.generating_db[p2_level])
                    node = Node.create(p1, p2, 2)
                    if (node.product_count > self.product_max) or (node.chain_count > self.chain_max):
                        continue
                    gen_levelc.append(node)
                    num_chain -= 1
                random.shuffle(gen_levelc)
            else:
                num_sum = self.section_length*2
                while num_sum > 0:
                    p1_level = random.randint(0, current_level-1)
                    p2_level = current_level-1 - p1_level
                    p1 = random.choice(self.generating_db[p1_level])
                    p2 = random.choice(self.generating_db[p2_level])
                    node = Node.create(p1, p2, 0)
                    if (node.product_count > self.product_max) or (node.chain_count > self.chain_max):
                        continue
                    gen_levelc.append(node)
                    num_sum -= 1

            out_levelc = random.sample(gen_levelc, k=self.section_length)
            for node in out_levelc:
                node.is_out = True
            self.generating_db.append(gen_levelc)
            self.output_db.append(out_levelc)
            current_level += 1

    def print_curriculum(self):
        for level in self.output_db:
            for node in level:
                print(node.expr)
            print("")
            print("######")
            print("")

if __name__ == '__main__':
    generator = SymDifferentiationGenerator(product_max=2, chain_max=2, section_length=5,
                                            is_poly=true, is_trig=true, is_exp=true)
    generator.generate_curriculum()
    generator.print_curriculum()
