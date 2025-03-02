def is_trivial(cnf):
    if not cnf:
        return True  # empty CNF: trivially satisfiable

    for clause in cnf:
        literals = set(clause)
