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
        child.product_term = child_product_term
        child.product_depth = child_product_depth
        parent.children.append(child)
        return child

    def chain_apply(self, parent, is_wide=false):
        if is_wide:
            num_inner = random.randint(1, max(1, ceil(len(parent.expression)/2)))
            inner_terms_indexes = random.sample(range(max(1, len(parent.expression)-1)), num_inner)
        else:
            num_inner = len(parent.expression)
            inner_terms_indexes = range(len(parent.expression))
        inner_terms = [parent.expression[i] for i in inner_terms_indexes]
        other_terms = [term for term in parent.expression if term not in inner_terms]
        if parent.product_term != -1:
            parent_product_term = parent.expression[parent.product_term]
        else:
            parent_product_term = None
        sum_inner = Add(*inner_terms)
        # sum_inner *= Utils.generate_random_nonzero_fraction()
        if self.is_poly:
            self.fns[-1] = parent.symbol ** random.randint(1, 10)
        f = random.choice(self.fns)
        if isinstance(f, FunctionClass):
            f = f(sum_inner)
        child = deepcopy(parent)
        child.expression = other_terms
        child.expression.append(f)
        child.rule = self
        child.difficulty += self.weight
        if parent.product_term in inner_terms_indexes:
            child.product_term = len(child.expression)-1
        else:
            if parent.product_term != -1:
                child.product_term = child.expression.index(parent_product_term)
        child.parent = parent
        parent.children.append(child)
        return child

    def apply(self, parent):
        if not parent.expression:
            if self.is_reuse:
                return self.sum_apply_reuse(parent)
            else:
                return self.sum_apply_native(parent)
        match self.rule_type:
            case ReverseDifferentiatingRuleType.SUM:
                if self.is_reuse:
                    return self.sum_apply_reuse(parent)
                else:
                    return self.sum_apply_native(parent)
            case ReverseDifferentiatingRuleType.PRODUCT:
                return self.product_apply(parent)
            case ReverseDifferentiatingRuleType.WIDE_PRODUCT:
                return self.product_apply(parent, true)
            case ReverseDifferentiatingRuleType.CHAIN:
                return self.chain_apply(parent)
            case ReverseDifferentiatingRuleType.WIDE_CHAIN:
                return self.chain_apply(parent, true)
            case _:
                return None

class DifferentiableEquationNode:
    def __init__(self,
                 expression: List[Expr],
                 parent: Optional["DifferentiableEquationNode"],
                 rule: Optional["DifferentiatingRule"],
                 difficulty: int,
                 symbol: Symbol,
                 product_term=-1,
                 product_depth=0,
                 chain_depth=0,
                 sum_depth=0,
                 derivative_degree=1,
                 children=Optional[list["DifferentiableEquationNode"]]):
        self.expression = expression
        self.parent = parent
        self.rule = rule
        self.children = children or []
        self.difficulty = difficulty
        self.symbol = symbol
        self.product_term = product_term
        self.product_depth = product_depth
        self.chain_depth = chain_depth
        self.sum_depth = sum_depth
        self.derivative_degree = derivative_degree


if __name__ == '__main__':
    test_node = DifferentiableEquationNode(
        expression=[],
        parent=None,
        rule=None,
        difficulty=0,
        symbol=Symbol('x'),
        product_term=-1,
        product_depth=0,
        children=[]
    )
    """
    product_rule = DifferentiatingRule(ReverseDifferentiatingRuleType.PRODUCT, RULE_WEIGHTS[
        ReverseDifferentiatingRuleType.PRODUCT.value[0]])
    child_node1 = product_rule.apply(test_node)
    child_node2 = product_rule.apply(child_node1)
    child_node3 = product_rule.apply(child_node2)
    child_node4 = product_rule.apply(child_node3)
    child_node4 = product_rule.sum_apply(child_node4)
    child_node5 = product_rule.apply(child_node4)
    child_node6 = product_rule.apply(child_node5)
    """
    """
    chain_rule = DifferentiatingRule(ReverseDifferentiatingRuleType.CHAIN, RULE_WEIGHTS[
        ReverseDifferentiatingRuleType.CHAIN.value[0]])
    child_node1 = chain_rule.sum_apply(test_node)
    child_node2 = chain_rule.sum_apply(child_node1)
    child_node3 = chain_rule.sum_apply(child_node2)
