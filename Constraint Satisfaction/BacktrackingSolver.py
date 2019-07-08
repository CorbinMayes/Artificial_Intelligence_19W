"""
Corbin Mayes - 1/31/19
Discussed with Hunter Gallant
"""

import random


class BacktrackingSolver:

    def __init__(self):
        self.count = 0

    def Backtracking_Search(self, csp):
        bt = self.Backtrack({}, csp)
        print('iterations through backtrack: ' + str(self.count))
        return bt

    def Backtrack(self, assignment, csp):
        self.count +=1
        #test if the goal state has been found
        if csp.goal_test(assignment):
            return assignment

        #get the next unassigned variable to test
        #var = self.select_unassigned_variable(assignment, csp)
        var = self.mrv(assignment, csp)

        #checks possible values within the domain
        #for value in self.order_domain_values(var, assignment, csp):
        for value in self.lcv(var, assignment, csp):
            #if the value doesn't have any conflicts it assigns the variable that value
            if csp.num_conflicts(var, value, assignment)==0:
                csp.assign(var, value, assignment)
                inferences = csp.suppose(var, value)
                #if self.no_inference(csp, var, value, assignment, inferences):
                if self.mac3_inference(csp, var, value, assignment, inferences):
                    result = self.Backtrack(assignment, csp)
                    if result != None:
                        return result
                csp.restore(inferences)
        csp.unassign(var, assignment)
        return None


    """
    ----variable ordering----
    """
    def select_unassigned_variable(self, assignment, csp):
        for var in csp.variables:
            if var not in assignment:
                return var
        return None

    """
    minimum remaining values heuristic
    """
    def mrv(self, assignment, csp):
        tmp_list = []
        for v in csp.variables:
            if v not in assignment:
                tmp_list.append(v)
        return self.argmin_random_tie(tmp_list, self.num_legal_moves, csp, assignment)

    def num_legal_moves(self, csp, var, assignment):
        if csp.curr_domains:
            return len(csp.curr_domains[var])
        else:
            count = 0
            for val in csp.domains:
                if csp.num_conflicts(var, val, assignment) == 0:
                    count+=1
            return count
    """
    Return an element with lowest fn(seq[i]) score; break ties at random
    """
    def argmin_random_tie(self, seq, fn, csp, assignment):
        best_score = fn(csp, seq[0], assignment)
        n = 0
        for x in seq:
            xscore = fn(csp, x, assignment)
            if xscore < best_score:
                best, best_score = x, xscore
                n = 1
            elif xscore == best_score:
                n += 1
                if random.randrange(n) == 0:
                    best = x
        return best



    """
    ----value ordering----
    """
    def order_domain_values(self, var, assignment, csp):
        return csp.choices(var)

    def lcv(self, var, assignment, csp):
        return sorted(csp.choices(var), key=lambda val: csp.num_conflicts(var, val, assignment))


    """
    ----Inferences----
    """
    def no_inference(self, csp, var, value, assignment, inferences):
        return True

    """
    maintains the arc consistency
    """
    def mac3_inference(self, csp, var, value, assignment, removals):
        tmp_list = []
        for X in csp.neighbors[var]:
            tmp_list.append((X, var))
        return self.AC3(csp, tmp_list, removals, assignment)

    """
    tests for arc consistency
    """
    def AC3(self, csp, queue = None, removals = None, assignment=None):
        if queue is None:
            tmp = []
            for Xi in csp.variables:
                for Xk in csp.neighbors[Xi]:
                    tmp.append((Xi, Xk))
            queue = tmp
        csp.support_pruning()
        while queue:
            (Xi,Xj) = queue.pop()
            if self.revise(csp, Xi, Xj, removals, assignment):
                if not csp.curr_domains[Xi]:
                    return False
                for Xk in csp.neighbors[Xi]:
                    if Xk != Xj:
                        queue.append((Xk, Xi))
        return True


    """
    returns true if a value was removed
    """
    def revise(self, csp, Xi, Xj, removals, assignment):
        revised = False
        for x in csp.curr_domains[Xi][:]:
            for y in csp.curr_domains[Xj]:
                if csp.constraints(Xi, x, Xj, y, assignment):
                    return False
            csp.prune(Xi, x, removals)
            revised = True
        return revised
