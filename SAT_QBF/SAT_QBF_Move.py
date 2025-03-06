

class SAT_QBF_Move:
    def __init__(self):
        self.move_registry = {
            "add_variable": self.add_variable,
            "add_clause": self.add_clause,
            "increase_clause_len": self.increase_clause_len,
            "extend_prefix": self.extend_prefix,
