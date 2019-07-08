How to run sudoku:

Run solve_sudoku.py to run both GSAT and WalkSAT. Currently, GSAT will run one_cell and all_cells. WalkSAT runs puzzle1 and puzzle2. 
solve_sudoku.py will run all of these at once so if you want to test only one, comment the others out. The GSAT files each have a dpll 
program that runs before GSAT runs to test if the file is satisfiable. The WalkSAT files don't have a dpll test because it would take a 
while to run with how big the cnf file is with its enormous amount of clauses. Give all the tests sometime to run because they do go 
through many flips

How to run mapcolor:

Run the solve_MapColor.py to run the WalkSAT on the MapColor.cnf file. This also has a DPLL test before the WalkSAT runs