"""
Corbin Mayes - 1/31/19
Discussed with Hunter Gallant
"""
from CSP import CSP
from BacktrackingSolver import BacktrackingSolver

class MapColorCSP():

    def __init__(self):
        self.variables = [0, 1, 2, 3, 4, 5, 6]
        self.var_dict = {0:'WA', 1:'NT', 2:'SA', 3:'Q', 4:'NSW', 5:'V', 6:'T'}
        self.domains = [0, 1, 2]
        self.dom_dict = {0:'red', 1:'blue', 2:'green'}
        self.neighbors = {0:[1,2], 1:[0,2,3], 2:[0,1,3,4,5], 3:[1,2,4], 4:[2,3,5], 5:[2,4], 6:[]}
        self.csp = CSP(self.variables, self.domains, self.neighbors, self.constraints)

    """
    constraint if the values are equivalent
    """
    def constraints(self, var1, val1, var2, val2, assignment):
        if val1 == val2:
            return False
        else:
            return True

    """
    solves the problem by running the backtracker and prints out solution
    """
    def solve(self):
        backtrack_solver = BacktrackingSolver()
        tmp = backtrack_solver.Backtracking_Search(self.csp)
        result = {}
        if tmp != None:
            for i in tmp:
                result[self.var_dict[i]] = self.dom_dict[tmp[i]]
            return result
        else:
            return 'The map is not solvable'