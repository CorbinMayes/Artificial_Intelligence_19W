"""
Corbin Mayes 2/14/19
"""

import random

class DPLL:
    def __init__(self, cnf):
        pass
        self.filename = cnf

        # Open the file and get all the clauses
        f = open(self.filename, "r")
        lines = f.readlines()
        f.close()

        # get the clauses and split them into a list
        tmp_clauses = []
        for line in lines:
            tmp_clauses.append(line[:-1])

        # split the clause strings into a list
        tmp_clauses2 = []
        for i in tmp_clauses:
            tmp_clauses2.append(i.split())

        self.clauses = set()
        # create clause list and dictionary
        for p in tmp_clauses2:
            tmp_set = set()
            for n in p:
                tmp_set.add(n)
            self.clauses.add(frozenset(tmp_set))

    def dpll_initializer(self):
        return self.dpll(self.clauses)


    """
    Tests if a set of clauses is satisfiable
    """
    def dpll(self, clauses):
        S = clauses

        #tests if set is already satisfiable
        if S == set():
            return "satisfiable"

        #If Set has any unit clauses, simplify the set by removing them
        uc = self.is_unit_clause(S)
        while(uc!=None):
            for i in uc:
                if i[0] == "-":
                    pos_i = i[1:]
                    if {i} in S and {pos_i} in S:
                        return "unsatisfiable"
                    else: S = self.simplify(S, i)
                else:
                    neg_i = "-"+i
                    if {i} in S and {neg_i} in S:
                        return "unsatisfiable"
                    else: S = self.simplify(S, i)
            uc = self.is_unit_clause(S)

        #tests again for satisfaction
        if S==set():
            return"satisfiable"

        #picks a random variable from the shortest clause
        p = self.rand_lit_from_short_clause(S)

        #gets the negated literal
        not_p = None
        if p[0] == "-":
            not_p = p[1:]
        else: not_p = "-"+p

        #simpify the set and test for satisfaction
        new_S = self.simplify(S, p)
        if (self.dpll(new_S)=="satisfiable"):
            return "satisfiable"

        #if the simplified set above didn't work try the simplified set without the negated literal
        else: return(self.dpll(self.simplify(S, not_p)))


    """
    simplifies a set by removing clauses and literals
    """
    def simplify(self, S, p):
        #get the negated literal
        not_p = None
        if p[0] == "-":
            not_p = p[1:]
        else: not_p = "-"+p

        new_S = set()
        for clause in S:

            #remove the negated literal from any clause that contains it
            if not_p in clause:
                new_set = set()
                for item in clause:
                    new_set.add(item)
                new_set.remove(not_p)
                new_S.add(frozenset(new_set))

            #removes all clausee with the literal
            elif p not in clause:
                new_S.add(clause)

        return new_S

    """
    Returns the first unit clause in the set 
    """
    def is_unit_clause(self, S):
        for item in S:
            if len(item) == 1:
                return item
        return None


    """
    Returns a random variable from the shortest clause
    """
    def rand_lit_from_short_clause(self, S):
        shortest_length = 1000000000
        shortest_clause = None

        #iterates through to find the shortest clause
        for clause in S:
            if len(clause) < shortest_length:
                tmp_clause = []
                for i in clause:
                    tmp_clause.append(i)
                shortest_clause = tmp_clause
                shortest_length = len(clause)

        #returns a random variable from the clause
        if shortest_clause != None:
            return random.choice(shortest_clause)