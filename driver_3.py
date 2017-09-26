import sys
from copy import deepcopy

def main():
    #Option 1: run with command line input as such: python3 driver_3.py <sudoku string of 81 numbers>
    if ".txt" not in sys.argv[1]:
        csp = create_csp(sys.argv[1])
        if ac_3(csp): #can be solved
            if all_filled(csp): #can be solved with ac_3
                write_solution(csp)
            else: #cannot be solved with ac_3 (backtracking required)
                bt = backtracking_search(csp)
                if bt:
                    csp.D = bt
                    write_solution(csp)
        else: #can't be solved
            print("Unsolvable Puzzle")

    #Option 2: run with .txt file as such: python3 driver_3.py sudoku_start.txt
    #Outputs results to results.txt
    else:
        open('test.txt', 'w').close()
        open('results.txt', 'w').close()
        with open(sys.argv[1]) as f:
            content = f.readlines()
            content = [x.strip() for x in content]
            for sudoku_str in content:
                csp = create_csp(sudoku_str)
                if ac_3(csp): #can be solved
                    if all_filled(csp): #can be solved with ac_3
                        # with open("cp_3_solvable.txt", "a") as myfile:
                        #     myfile.write("yes\n")
                        write_solution(csp)
                    else: #cannot be solved with ac_3 (backtracking required)
                        # with open("cp_3_solvable.txt", "a") as myfile:
                        #     myfile.write("no\n")
                        bt = backtracking_search(csp)
                        if bt:
                            csp.D = bt
                            write_solution(csp)
                else: #can't be solved
                    print("Unsolvable Puzzle")

class CSP():
    def __init__(self, variables, domains, constraints):
        self.X = variables
        self.D = domains
        self.C = constraints

def create_csp(board_str):
    #read in string and convert into list of tuples if board index + value
    #e.g board = [('A1', '0'), ('A2', '0'), ('A3', '3'), etc.]
    board_values = []
    for ch in board_str:
        board_values.append(ch)

    #variables = array of all indicies from A1 - I8
    variables = []
    alphabet_arr = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
    for row in range(1,10):
        for col in range(1,10):
            variables.append(('{}{}'.format(alphabet_arr[row-1],col)))

    board = []
    for i in range (0, len(board_values)):
        board.append((variables[i], board_values[i]))

    #domains = dictionary of index: array of possible number values
    domains = {}
    for (index, value) in board:
        if value == '0':
            domains.update({index: [1,2,3,4,5,6,7,8,9]})
        else:
            domains.update({index: [int(value)]})

    #constraints = dictionary of index: array of indicies that can't have the same number
    constraints = {}
    for (idx, value) in board:
        x = alphabet_arr.index(idx[0])
        y = int(idx[1])

        vals = []
        for row in range(9):
            for col in range(1,10):
                rounded_x = 3 * (x // 3)
                rounded_y = 3 * ((y-1) // 3)
                if x == row and y != col:
                    vals.append('{}{}'.format(alphabet_arr[row],col))
                elif x != row and y == col:
                    vals.append('{}{}'.format(alphabet_arr[row],col))
                elif row in range(rounded_x, rounded_x + 3) and (col-1) in range(rounded_y, rounded_y + 3) \
                and (x!=row and y!=col):
                    vals.append('{}{}'.format(alphabet_arr[row],col))
        constraints.update({idx: vals})

    csp = CSP(variables, domains, constraints)
    # print("\nVariables: ", csp.X)
    # print("\nDomains: ",csp.D)
    # print("\nConstraints: ",csp.C)
    return csp


def ac_3(csp):
    #returns false if inconsistency found, true otherwise

    #initially all arcs in csp
    queue = []
    for i in csp.X:
        for j in csp.C[i]:
            queue.append((i,j))

    while len(queue) != 0: #queue not empty
        xixj = queue.pop(0) #remove first from queue
        xi = xixj[0]
        xj = xixj[1]

        if revise(csp, xi, xj):
            if len(csp.D[xi]) == 0: #if size of Di = 0
                return False

            #for each neighbor of Xi minus Xj, add them to queue
            for xk in csp.C[xi]:
                if xk != xj:
                    queue.append((xk, xi))
    return True

def revise(csp, xi, xj):
    #returns true iff domain of Xi is revised
    revised = False
    for x in csp.D[xi]:
        # if no value y in D[xj] allows (x,y) to satisfy constraint between Xi and Xj
        noval = True
        for y in csp.D[xj]:
            if x != y:
                noval = False
        if noval:
            csp.D[xi].remove(x) #delete x from D
            revised = True
    return revised

def all_filled(csp):
    #check all squares, if they don't all have exactly one value, allfilled = False
    allfilled = True
    for index in csp.X:
        if len(csp.D[index]) > 1: #there are possibilities remaining
            allfilled = False
    return allfilled

def write_solution(csp):

    s = ""
    for index in csp.X:
        s += str(csp.D[index][0])
    #Run with single sudoku string
    if ".txt" not in sys.argv[1]:
        print(s)
    #Run with .txt file
    else:
        with open("results.txt", "a") as myfile:
            myfile.write(s)
            myfile.write("\n")

  
def backtracking_search(csp):
    #returns a solution, or failure
    return backtrack({}, csp)


def backtrack(assignment, csp_original):
    #returns a solution, or failure
    csp = deepcopy(csp_original)

    if len(assignment) == 0: #first time running
        assignment = create_assignment(csp)

    #if assignment is complete return assignment
    complete = True
    for key in assignment:
        if not(assignment[key]):
            complete = False
    if complete:
        return assignment 

    var = sel_unassigned_var(csp)
    for value in csp.D[var]:
       #check if value is consistent with assignment
        consistent = True
        for key in csp.C[var]:
            if [value] == [assignment[key]]:
                consistent = False

        if consistent == True:
            csp.D[var] = [value] #add var = value to assignment
            if ac_3(csp)!= False: #inferences != failure (ac_3 returns false if failure)
                result = backtrack(create_assignment(csp), csp)
                if result != False: #if result != failure, return result
                    return result
            csp.D = deepcopy(csp_original.D) #remove inferences (restore domain to original state)
    return False


def create_assignment(csp):
    d = {}
    for idx in csp.X:
        if len(csp.D[idx]) == 1:
            d.update({idx: [csp.D[idx][0]]})
        else:
            d.update({idx: []})
    #print(d)
    return d


def sel_unassigned_var(csp):
    #MVR Heuristic
    #Selects the square with the least possible numbers that will fit

    min_index = ""
    min_poss_nums = 10

    for index in csp.X:
        poss_nums = len(csp.D[index]) #number of possible nums
        if poss_nums < min_poss_nums and poss_nums != 1:
            min_index = index
            min_poss_nums = poss_nums
    return min_index #returns index with least amount of possible numbers that can fit


main()