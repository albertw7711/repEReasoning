def is_trivial(cnf):
    if not cnf:
        return True  # empty CNF: trivially satisfiable

    for clause in cnf:
        literals = set(clause)
        # Check for tautological clause: x and ¬x both present
        stripped = {lit.strip('¬') for lit in literals}
        for var in stripped:
            if var in literals and f"¬{var}" in literals:
                return True  # tautology detected

    # Optional: detect all-unit and very short
    if len(cnf) <= 2 and all(len(clause) == 1 for clause in cnf):
        return True

    return False

def is_formula_reusable(formula):
    hardness = formula.get_hardness()

    if formula.is_qbf:
