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
        return q

    def get_sol_for_node_helper(self, node, queue, visited):
        step = None
        if node.is_solved:
