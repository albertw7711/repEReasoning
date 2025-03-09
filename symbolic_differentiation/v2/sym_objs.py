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


    @staticmethod
    def create(p1, p2, rule):
        node = Node(p1=p1, p2=p2, rule=rule)
        node.sum_count = p1.sum_count + p2.sum_count
        node.product_count = p1.product_count + p2.product_count
        node.chain_count = p1.chain_count + p2.chain_count
        match rule:
            case 0:
                node.expr = Add(p1.expr, p2.expr, evaluate=False)
                node.level = p1.level + p2.level + 1
            case 1:
                node.expr = Mul(p1.expr, p2.expr, evaluate=False)
