Sudoku Solver
Constraint Satisfaction Problems


To Run:
Option 1: Run with command line input, <input_string> being a sudoku board sequence of 81 numbers
e.g. python3 driver_3.py <input_string>

Option 2: Run with .txt file
e.g. python3 driver_3.py sudoku_start.txt
Outputs are written to a file called results.txt


Observations:
-The only 3 cases solvable by AC-3 (Arc-Constraint-3) are case #1, #2, #332 in the given test cases.
-All cases were solvable by my program
-Runtime: The program finishes running the given 400 sudoku inputs in under 3 minutes.
