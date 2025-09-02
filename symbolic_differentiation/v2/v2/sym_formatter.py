from copy import deepcopy
from collections import OrderedDict

from sympy import *
from sympy.core.function import UndefinedFunction
from prompt_templates import *
from sym_verifier import SymDifferentiationVerifier
from sym_generator import SymDifferentiationGenerator

import json

class SymDifferentiationFormatter:
    def __init__(self, generator):
        self.generator = generator

    def expr_to_latex(self, expr):
        if expr is None:
            return None
        if not isinstance(expr, Expr):
            if isinstance(expr, UndefinedFunction):
                expr = expr(symbols("x"))
            else:
                raise Exception("Undefined expression type")

        return latex(expr)

    def get_prompt(self, node):
        expr = self.expr_to_latex(node.expr)
        final_prompt = prompt_template.replace("<INPUT>…</INPUT>", f"<INPUT>{expr}</INPUT>")
        return final_prompt

    def get_label(self, node):
        try:
            verifier = SymDifferentiationVerifier()
            sol = verifier.get_sol_for_node(node)
            rule_log = "\n".join(self.format_step(step) for step in sol[:-1])
            final_answer = self.format_step(sol[-1])
            return label_template.format(rule_log=rule_log, final_answer=final_answer)
        except Exception as e:
            print(e)


    def format_step(self, step) -> str:
        step_copy = deepcopy(step)
        step_copy.target = self.expr_to_latex(step_copy.target)
        step_copy.u = self.expr_to_latex(step_copy.u)
        step_copy.v = self.expr_to_latex(step_copy.v)
        step_copy.sol = self.expr_to_latex(step_copy.sol)
        if step_copy.rule is None:
            return f"❯ STD     : d/dx {step_copy.target} → {step_copy.sol}"
        elif step_copy.rule == 1:
            return f"❯ PRODUCT : Split {step_copy.target} into u={step_copy.u} and v={step_copy.v}"
        elif step_copy.rule == 0:
            return f"❯ SUM     : Split {step_copy.target} into u={step_copy.u} and v={step_copy.v}"
        elif step_copy.rule == 2:
            return f"❯ CHAIN   : Treat {step_copy.target} as {step_copy.u} composed with {step_copy.v}"
        elif step_copy.rule == 9:
            return f'❯ REUSE‑INTRO : Reusing derivative of "{step_copy.target}" from earlier.'
        elif step_copy.rule == 10:
            return step_copy.sol
        else:
            raise Exception(f"❯ {step_copy.rule} : {step_copy.sol or 'Unspecified operation'}")

    def get_training_db(self):
        if len(self.generator.output_db) == 1:
            self.generator.generate_curriculum()

        training_db = OrderedDict()
        for level, level_nodes in enumerate(self.generator.output_db):
            level_db = {}
            for node_i, node in enumerate(level_nodes):
                prompt = self.get_prompt(node)
                label = self.get_label(node)
                level_db[str(node_i)] = {"prompt": prompt, "label": label}
            training_db[str(level)] = level_db
        return training_db

    def print_training_db(self, training_db):
        print(json.dumps(training_db, indent=4))


if __name__ == '__main__':
    generator1 = SymDifferentiationGenerator(product_max=2, chain_max=2, section_length=5,
                                            is_poly=true, is_trig=true, is_exp=true)
    formatter1 = SymDifferentiationFormatter(generator1)
    training_db1 = formatter1.get_training_db()
    print(training_db1["5"]["0"]["prompt"])
    print(training_db1["5"]["0"]["label"])