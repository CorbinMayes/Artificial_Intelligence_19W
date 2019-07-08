"""
Corbin Mayes - 1/31/19
Discussed with Hunter Gallant
"""

from CSP import CSP
from BacktrackingSolver import BacktrackingSolver

class Circuit:
    def __init__(self, height, width, id):
        self.height = height
        self.width = width
        self.id = id

    def __str__(self):
        return ('circuit:' + str(self.id) + ' height:' + str(self.height) + ' width:' + str(self.width))

class CircuitBoardCSP:
    def __init__(self):
        #define the ciruits
        A_circuit = Circuit(2, 3, 'a')
        B_circuit = Circuit(2, 5, 'b')
        C_circuit = Circuit(3, 2, 'c')
        E_circuit = Circuit(1, 7, 'e')
        self.board = Circuit(3, 10, '.')
        self.variables = [0, 1, 2, 3]
        self.var_dict = {0:A_circuit, 1:B_circuit, 2:C_circuit, 3:E_circuit}
        self.domains = []
        self.dom_dict = {}

        #create the dictionary of possible locations as well as the domain
        count = 0
        for w in range(0, self.board.width):
            for h in range(0, self.board.height):
                self.dom_dict[count] = (w,h)
                count += 1
        for i in range(0, len(self.dom_dict)):
            self.domains.append(i)
        self.neighbors = {0:[1,2,3], 1:[0,2,3], 2:[0,1,3], 3:[0,1,2]}

        #create the csp
        self.csp = CSP(self.variables, self.domains, self.neighbors, self.constraints)

    """
    tests the constraints between two circuits and their values. Makes sure the circuits are
    in the board boundaries and also don't interfere with eachother
    """
    def constraints(self, var1, val1, var2, val2, assignment):
        for w1 in range(self.dom_dict[val1][0], self.dom_dict[val1][0]+self.var_dict[var1].width):
            for h1 in range(self.dom_dict[val1][1], self.dom_dict[val1][1] + self.var_dict[var1].height):
                for w2 in range(self.dom_dict[val2][0], self.dom_dict[val2][0] + self.var_dict[var2].width):
                    for h2 in range(self.dom_dict[val2][1], self.dom_dict[val2][1] + self.var_dict[var2].height):
                        if w1 == w2 and h1 == h2 or h1>=self.board.height or h2>=self.board.height or w1 >=self.board.width or w2>=self.board.width:
                            return False
        return True
    """
    solves the circuit board problem
    """
    def solve(self):
        #call the backtracker to get a solution
        backtrack_solver = BacktrackingSolver()
        tmp = backtrack_solver.Backtracking_Search(self.csp)
        print(tmp)

        if tmp != None:
            #using the dictionaries it translates the rough result into a
            #more understandable result
            pri = {}
            for i in tmp:
                pri[self.var_dict[i].__str__()] = self.dom_dict[tmp[i]]
            print(pri)

            #Translates the result into a list of lists to map out the solution
            result =[]
            #fill the space with empty markers
            for i in range(0, self.board.height):
                row = []
                for j in range(0, self.board.width):
                    row.append('.')
                result.append(row)

            #add the circuits to the board
            for cir in tmp:
                for h in range(self.dom_dict[tmp[cir]][1], self.dom_dict[tmp[cir]][1] + self.var_dict[cir].height):
                    for w in range(self.dom_dict[tmp[cir]][0], self.dom_dict[tmp[cir]][0] + self.var_dict[cir].width):
                        result[h][w] = self.var_dict[cir].id

            #translate the list of lists to a string and return the completed board
            str_result = ''
            for k in range(self.board.height-1, -1, -1):
                for l in range(0, self.board.width):
                    str_result = str_result + result[k][l] + ' '
                str_result = str_result + "\n"
        else:
            str_result = 'The board could not be solved'
        return str_result