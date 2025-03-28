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
        if is_trig:
            fns.extend(deepcopy(TRIGS))
        if is_rec_trig:
            fns.extend(deepcopy(REC_TRIGS))
        if is_inv_trig:
            fns.extend(deepcopy(INV_TRIGS))
        if is_inv_rec_trig:
            fns.extend(deepcopy(INV_REC_TRIGS))
        if is_exp:
            fns.append(exp)
        if is_log:
            fns.append(log)
        if is_poly:
            fns.append(Symbol('x'))
        sum_rule = DifferentiatingRule(ReverseDifferentiatingRuleType.SUM, RULE_WEIGHTS[
            ReverseDifferentiatingRuleType.SUM.value[0]], fns, is_poly)
        if is_product_wide:
            product_rule = DifferentiatingRule(ReverseDifferentiatingRuleType.WIDE_PRODUCT,
                                               RULE_WEIGHTS[
                ReverseDifferentiatingRuleType.WIDE_PRODUCT.value[0]], fns, is_poly)
        else:
            product_rule = DifferentiatingRule(ReverseDifferentiatingRuleType.PRODUCT, RULE_WEIGHTS[
                ReverseDifferentiatingRuleType.PRODUCT.value[0]], fns, is_poly)
        if is_chain_wide:
            chain_rule = DifferentiatingRule(ReverseDifferentiatingRuleType.WIDE_CHAIN,
                                             RULE_WEIGHTS[
                ReverseDifferentiatingRuleType.WIDE_CHAIN.value[0]], fns, is_poly)
        else:
            chain_rule = DifferentiatingRule(ReverseDifferentiatingRuleType.CHAIN, RULE_WEIGHTS[
                ReverseDifferentiatingRuleType.CHAIN.value[0]], fns, is_poly)
        rules = [sum_rule, product_rule, chain_rule]
        if not fns:
            print("No fns defined")
            return None

        node = DifferentiableEquationNode(
            expression=[],
            parent=None,
            rule=None,
            difficulty=0,
            symbol=Symbol('x'),
            product_term=-1,
            product_depth=0,
            chain_depth=0,
            sum_depth=0,
            children=[],
        )
        node = sum_rule.apply(node)
        num_sum -= 1
        rule_reqs = [num_sum, product_depth, chain_depth]
        all_req_met = all(v == 0 for v in rule_reqs)
        if all_req_met:
            return node
