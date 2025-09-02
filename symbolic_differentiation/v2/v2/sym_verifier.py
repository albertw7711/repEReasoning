from sym_objs import *
from sym_generator import *
from collections import deque
from sympy import *

class SymDifferentiationVerifier:
    def __init__(self, symbol=symbols("x")):
        self.symbol = symbol

    def get_sol_for_node(self, node):
        q = deque()
        visited = set()
        self.get_sol_for_node_helper(node, q, visited)

        final_sol = diff(node.expr, self.symbol)
        final_step = Step(10, node.expr, node.expr, None, final_sol)
        q.append(final_step)
        return list(q)

    # post-order traversal
    def get_sol_for_node_helper(self, node, queue, visited):
        step = None
        if node.is_solved:
            if node.expr not in visited:
                step = Step(9, node.expr, node.expr, None, node.deri)
                queue.append(step)
                visited.add(node.expr)
                return
        else:
            match node.rule:
                case None: # standard deri
                    step = Step(node.rule, node.expr, None, None, node.deri)
                case 0: # sum (has to be reversed due to prev impl)
                    step = Step(node.rule, node.expr, node.p2.expr, node.p1.expr)
                case 1|2: # product, chain
                    step = Step(node.rule, node.expr, node.p1.expr, node.p2.expr)
            queue.append(step)
            node.is_solved = True
            visited.add(node.expr)
        if node.rule is not None:
            self.get_sol_for_node_helper(node.p1, queue, visited)
            self.get_sol_for_node_helper(node.p2, queue, visited)

    def print_sol(self, full_sol):
        for step in full_sol:
            print(step.rule, " | ", step.target, " | ", step.u, " | ", step.v, " | ", step.sol)

if __name__ == "__main__":
    generator = SymDifferentiationGenerator(product_max=2, chain_max=2, section_length=5,
                                            is_poly=true, is_trig=true, is_exp=true)
    generator.generate_curriculum()
    verifier = SymDifferentiationVerifier()
    full_sol = verifier.get_sol_for_node(generator.output_db[5][0])
    verifier.print_sol(full_sol)