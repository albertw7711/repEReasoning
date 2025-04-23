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
        current_attempt = 0
        while not all_req_met and current_attempt < DifferentiationGenerator.ATTEMPT_LIMIT:
            current_rule_index = -1
            while true:
                current_rule_index = random.choice(range(len(rules)))
                if rules[current_rule_index] is None:
                    continue
                elif rule_reqs[current_rule_index] > 0:
                    break
            current_rule = rules[current_rule_index]
            node = current_rule.apply(node)
            rule_reqs[current_rule_index] -= 1
            current_attempt += 1
            all_req_met = all(v == 0 for v in rule_reqs)
        if current_attempt == DifferentiationGenerator.ATTEMPT_LIMIT:
            return None
        node.derivative_degree = derivative_degree
        return node

    def generate_theorem_reuse(self,
                         derivative_degree=1,
                         num_sum: int=1, product_depth: int=0, chain_depth: int=0,
                         is_poly=false, is_trig=false, is_rec_trig=false,
                         is_inv_trig=false, is_inv_rec_trig=false, is_exp=false, is_log=false,
                         is_product_wide=false, is_chain_wide=false,
                         is_batch: bool=false):
        discovered_nodes = self.generating_db
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
            ReverseDifferentiatingRuleType.SUM.value[0]], discovered_nodes, is_poly, True)
        if is_product_wide:
            product_rule = DifferentiatingRule(ReverseDifferentiatingRuleType.WIDE_PRODUCT,
                                               RULE_WEIGHTS[
                                                   ReverseDifferentiatingRuleType.WIDE_PRODUCT.value[
                                                       0]], fns, is_poly)
        else:
            product_rule = DifferentiatingRule(ReverseDifferentiatingRuleType.PRODUCT, RULE_WEIGHTS[
                ReverseDifferentiatingRuleType.PRODUCT.value[0]], fns, is_poly)
        if is_chain_wide:
            chain_rule = DifferentiatingRule(ReverseDifferentiatingRuleType.WIDE_CHAIN,
                                             RULE_WEIGHTS[
                                                 ReverseDifferentiatingRuleType.WIDE_CHAIN.value[
                                                     0]], fns, is_poly)
        else:
            chain_rule = DifferentiatingRule(ReverseDifferentiatingRuleType.CHAIN, RULE_WEIGHTS[
                ReverseDifferentiatingRuleType.CHAIN.value[0]], fns, is_poly)
        rules = [sum_rule, product_rule, chain_rule]
        if not fns:
            print("No fns defined")
            return None

        # initialize using a random node from the discovered db
        current_attempt = 0
        sub_node_exists = False
        while current_attempt < DifferentiationGenerator.ATTEMPT_LIMIT:
            node = random.choice(discovered_nodes)
            if (node.sum_depth <= num_sum
                and node.product_depth <= product_depth
                and node.chain_depth <= chain_depth):
                sub_node_exists = True
                break
            current_attempt += 1
            if current_attempt == DifferentiationGenerator.ATTEMPT_LIMIT:
                break
        if not sub_node_exists:
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
            sum_rule.is_reuse = False
            sum_rule.fns = fns
            node = sum_rule.apply(node)
            sum_rule.is_reuse = True
            sum_rule.fns = discovered_nodes
            num_sum -= 1
        remaining_reqs = [num_sum-node.sum_depth, product_depth-node.product_depth,
                          chain_depth-node.chain_depth]
        all_req_met = all(v == 0 for v in remaining_reqs)
        current_attempt = 0
        while sub_node_exists and all_req_met and current_attempt < \
                DifferentiationGenerator.ATTEMPT_LIMIT:
            current_rule_index = -1
            while true:
                current_rule_index = random.choice(range(len(rules)))
                if rules[current_rule_index] is None:
                    continue
                elif remaining_reqs[current_rule_index] > 0:
                    break
            current_rule = rules[current_rule_index]
            if current_rule.rule_type == ReverseDifferentiatingRuleType.SUM:
                current_attempt = 0
                while current_attempt < DifferentiationGenerator.ATTEMPT_LIMIT:
                    node_tmp = deepcopy(node)
                    node = current_rule.apply(node)
                    if (node.sum_depth <= num_sum
                            and node.product_depth <= product_depth
                            and node.chain_depth <= chain_depth):
                        break
                    node = node_tmp
                    current_attempt += 1
            if current_attempt == DifferentiationGenerator.ATTEMPT_LIMIT:
                break
            if current_rule_index != 0:
                remaining_reqs[current_rule_index] -= 1
            else:
                remaining_reqs[current_rule_index] = num_sum - node.sum_depth
            current_attempt += 1
            all_req_met = all(v == 0 for v in remaining_reqs)

        # start padding
        sum_rule.is_reuse = False
        sum_rule.fns = fns
        all_req_met = all(v == 0 for v in remaining_reqs)
        if all_req_met:
            return node
        current_attempt = 0
        while not all_req_met and current_attempt < DifferentiationGenerator.ATTEMPT_LIMIT:
            current_rule_index = -1
            while true:
                current_rule_index = random.choice(range(len(rules)))
                if rules[current_rule_index] is None:
                    continue
                elif remaining_reqs[current_rule_index] > 0:
                    break
            current_rule = rules[current_rule_index]
            node = current_rule.apply(node)
            remaining_reqs[current_rule_index] -= 1
            current_attempt += 1
            all_req_met = all(v == 0 for v in remaining_reqs)
        if current_attempt == DifferentiationGenerator.ATTEMPT_LIMIT:
            return None
        node.derivative_degree = derivative_degree
        return node

    def generate_curriculum(self,
                            max_deri_degree=1,
                            max_num_sum: int=1, max_product_depth: int=0, max_chain_depth: int=0,
                            num_section=1, section_length=10, is_batch=false):
        reqs_list = []
        for _ in range(num_section):
            reqs = [Utils.easy_skewed_randint(1, max_deri_degree),
                    Utils.easy_skewed_randint(1, max_num_sum),
                    Utils.easy_skewed_randint(0, max_product_depth),
                    Utils.easy_skewed_randint(0, max_chain_depth)]
            fns_selection = np.random.choice(range(DifferentiationGenerator.NUM_FN_TYPE),
                                             size=Utils.easy_skewed_randint(1, DifferentiationGenerator.NUM_FN_TYPE),
                                             replace=False,
                                             p=np.array(DifferentiationGenerator.FN_WEIGHTS)/sum(
                                                 DifferentiationGenerator.FN_WEIGHTS))
            fns_toggle = [0] * DifferentiationGenerator.NUM_FN_TYPE
            for i in range(len(fns_toggle)):
                if i in fns_selection:
                    fns_toggle[i] = 1
            if all(f == 0 for f in fns_toggle):
                fns_toggle[random.randint(0, len(fns_toggle) - 1)] = 1
            wide_toggle = [random.randint(0, 1) for _ in range(
                DifferentiationGenerator.NUM_WIDE_TYPE)]
            reqs.extend(fns_toggle)
            reqs.extend(wide_toggle)
            reqs_list.append(reqs)
        reqs_list = Utils.sort_by_weighted_sum(reqs_list, DifferentiationGenerator.ARG_WEIGHTS)
        for reqs in reqs_list:
            if self.generating_db:
                num_native = random.randint(1, num_section-1)
            else:
                num_native = section_length
            num_reuse = section_length - num_native
            for _ in range(num_native):
                try:
                    theorem_new = (self.generate_theorem_native(*reqs))
                except:
                    theorem_new = None
                finally:
                    self.generating_db.append(deepcopy(theorem_new))
            for _ in range(num_reuse):
                try:
                    theorem_new = (self.generate_theorem_reuse(*reqs))
                except:
                    theorem_new = None
                finally:
                    self.generating_db.append(deepcopy(theorem_new))
        for i in range(len(self.generating_db)):
            thm = self.generating_db[i]
            if not thm:
                reqs = [1, 1]
                reqs.extend([0]*11)
                reqs[random.randint(4, DifferentiationGenerator.NUM_FN_TYPE+3)] = 1
                theorem_new = self.generate_theorem_native(*reqs)
                self.generating_db[i] = deepcopy(theorem_new)

    def generate_training_db(self, max_deri_degree=1,
                            max_num_sum: int=1, max_product_depth: int=0, max_chain_depth: int=0,
                            num_section=1, section_length=10, is_batch=false):
        self.generate_curriculum(max_deri_degree, max_num_sum, max_product_depth, max_chain_depth, num_section, section_length, is_batch)
        for node in self.generating_db:
            if not isinstance(node, DifferentiableEquationNode):
                node = DifferentiableEquationNode(
                    expression=[node],
                    parent=None,
                    rule=None,
                    difficulty=0,
                    symbol=list(node.free_symbols)[0],
                    product_term=-1,
                    product_depth=0,
                    chain_depth=0,
                    sum_depth=0,
                    derivative_degree=1,
                    children=[],
                )
            node_expr = Add(*node.expression)
            prompt = ""
            try:
                label = self.get_problem_label(node_expr, node.symbol, node.derivative_degree)
            except:
                print("Cannot differentiate " + str(node_expr))
                continue
