"""
Corbin Mayes 2/14/19
Discussed with Hunter Gallant
"""

from SAT import SAT
from DPLL import DPLL


if __name__ == "__main__":
    puzzle_name = "MapColor"
    sol_filename = puzzle_name + ".sol"
    new_cnf = puzzle_name + ".cnf"

    map_DPLL = DPLL(new_cnf)
    print("MapColor.cnf is "+map_DPLL.dpll_initializer())

    map_sat = SAT(new_cnf)
    result = map_sat.WalkSAT()

    if result:
        solution = map_sat.solution
        tmp_solution = []
        for solv in solution:
            tmp_solution.append(map_sat.var_dict[solv])
        print(tmp_solution)