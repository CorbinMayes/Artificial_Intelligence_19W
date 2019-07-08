from display import display_sudoku_solution
import random, sys
from SAT import SAT
from Sudoku import Sudoku
from DPLL import DPLL

if __name__ == "__main__":
    # for testing, always initialize the pseudorandom number generator to output the same sequence
    #  of values:
    random.seed(1)

    """
    one_cell GSAT
    """
    puzzle_name = "one_cell"
    sol_filename = puzzle_name+".sol"
    new_cnf = puzzle_name+".cnf"

    dpll = DPLL(new_cnf)
    print(puzzle_name+" is "+dpll.dpll_initializer())

    sat = SAT(new_cnf)

    result = sat.GSAT()
    if result:
        sat.write_solution(sol_filename)
        display_sudoku_solution(sol_filename)
    else:
        print("no solution found within limitations")


    """
    all_cells GSAT
    """
    puzzle_name = "all_cells"
    sol_filename = puzzle_name + ".sol"
    new_cnf = puzzle_name + ".cnf"

    dpll = DPLL(new_cnf)
    print(puzzle_name + " is " + dpll.dpll_initializer())

    sat = SAT(new_cnf)

    result = sat.GSAT()
    if result:
        sat.write_solution(sol_filename)
        display_sudoku_solution(sol_filename)
    else:
        print("no solution found within limitations")


    """
    puzzle 1 WalkSAT
    """

    puzzle_name = "puzzle1"
    sol_filename = puzzle_name + ".sol"

    puzzlesud = puzzle_name + ".sud"

    test_sudoku = Sudoku()
    test_sudoku.load(puzzlesud)

    new_cnf = puzzle_name + ".cnf"
    test_sudoku.generate_cnf(new_cnf)

    sat = SAT(new_cnf)

    result = sat.WalkSAT()
    if result:
        sat.write_solution(sol_filename)
        display_sudoku_solution(sol_filename)
    else:
        print("no solution found within limitations")


    """
    puzzle 2 WalkSAT
    """
    puzzle_name = "puzzle2"
    sol_filename = puzzle_name + ".sol"

    puzzlesud = puzzle_name + ".sud"

    test_sudoku = Sudoku()
    test_sudoku.load(puzzlesud)

    new_cnf = puzzle_name + ".cnf"
    test_sudoku.generate_cnf(new_cnf)

    sat = SAT(new_cnf)

    result = sat.WalkSAT()
    if result:
        sat.write_solution(sol_filename)
        display_sudoku_solution(sol_filename)
    else:
        print("no solution found within limitations")