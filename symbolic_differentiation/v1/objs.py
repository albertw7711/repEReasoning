from __future__ import annotations
from itertools import combinations
from typing import Optional, List
from enum import Enum
from sympy import *
from Utils import Utils
import random
from copy import deepcopy
from math import ceil

class ReverseDifferentiatingRuleType(Enum):
    SUM = 0,
    PRODUCT = 1,
    WIDE_PRODUCT = 2,
    CHAIN = 3,
    WIDE_CHAIN = 4,
TRIGS = [sin, cos, tan]
REC_TRIGS = [sec, csc, cot]
INV_TRIGS = [asin, acos, atan]
INV_REC_TRIGS = [asec, acsc, acot]

RULE_WEIGHTS = [1] * 5
class DifferentiatingRule:
    def __init__(self, rule_type: ReverseDifferentiatingRuleType,
                 weight: int, fns=None, is_poly: bool=false, is_reuse: bool=False):
        if fns is None:
            fns = []
        self.rule_type = rule_type
        self.weight = weight
        self.fns = fns
        self.is_poly = is_poly
        self.is_reuse = is_reuse


    def sum_apply_native(self, parent):
        if self.is_poly:
            self.fns[-1] = parent.symbol ** random.randint(1, 10)
        term_new = random.choice(self.fns)
        if isinstance(term_new, DifferentiableEquationNode):
            print()
        if isinstance(term_new, FunctionClass):
            term_new = term_new(parent.symbol)
        # term_new *= Utils.generate_random_nonzero_fraction()

        child = deepcopy(parent)
        child.sum_depth += 1
        child.expression.append(term_new)
        child.rule = self
        child.difficulty += self.weight
        child.parent = parent
        parent.children.append(child)
        return child

    def sum_apply_reuse(self, parent):
        node_new = random.choice(self.fns)
        for i in range(len(node_new.expression)):
            pass
            # node_new.expression[i] *= Utils.generate_random_nonzero_fraction()
        child = deepcopy(parent)
        child.sum_depth += node_new.sum_depth
        if node_new.product_depth > child.product_depth:
            child.product_depth = node_new.product_depth
            child.product_term = len(child.expression) + node_new.product_term
        child.chain_depth = max(child.chain_depth, node_new.chain_depth)
        for expr1 in node_new.expression:
            if isinstance(expr1, DifferentiableEquationNode):
                print()
        child.expression.extend(node_new.expression)
        child.rule = self
        child.difficulty += self.weight
        child.parent = parent
        parent.children.append(child)
        return child

    def product_apply(self, parent, is_wide=false):
        child_product_term = parent.product_term
        child_product_depth = parent.product_depth
        if is_wide:
            child_product_depth = -1
            child_product_term = random.choice(range(len(parent.expression)))
        else:
            if child_product_term == -1:
                child_product_term = random.choice(range(len(parent.expression)))
        if self.is_poly:
            self.fns[-1] = parent.symbol ** random.randint(1, 10)
        mult_new = random.choice(self.fns)
        if isinstance(mult_new, FunctionClass):
            mult_new = mult_new(parent.symbol)
        # mult_new *= Utils.generate_random_nonzero_fraction()
        child_expression = deepcopy(parent.expression)
        child_expression[child_product_term] *= mult_new
        child_product_depth += 1
        child_rule = self
        child_difficulty = parent.difficulty + child_rule.weight
        child = deepcopy(parent)
        child.expression = child_expression
        child.parent = parent
        child.rule = child_rule
        child.difficulty = child_difficulty
