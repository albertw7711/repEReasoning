from sympy import *

TRIGS = [sin, cos, tan]
REC_TRIGS = [sec, csc, cot]
INV_TRIGS = [asin, acos, atan]
INV_REC_TRIGS = [asec, acsc, acot]

class Node:
    def __init__(self, p1, p2, rule, expr=None, children=None, level=0, sum_count=0, product_count=0, chain_count=0,
                 is_out=False, is_solved=False, deri=None):
        if children is None:
            children = []
        self.expr = expr
        self.level = level
        self.sum_count = sum_count
        self.product_count = product_count
        self.chain_count = chain_count
        self.p1 = p1
        self.p2 = p2
        self.rule = rule # 0: sum, 1: product, 2: chain
        self.children = children
        self.is_out = is_out
        self.is_solved = is_solved
        self.deri = deri
