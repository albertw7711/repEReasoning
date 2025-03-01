class SAT_QBF_Formula:
    def __init__(self, variables, prefix, cnf, parents=[], is_qbf=True):
        self.variables = variables # ['x1', 'x2', ...]
        self.prefix = prefix # [('∃', 'x1'), ('∀', 'x2'), ...]
