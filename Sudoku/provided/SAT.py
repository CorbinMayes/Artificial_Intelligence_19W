"""
Corbin Mayes 2/14/19
Discussed with Hunter Gallant
"""


import random

class SAT:

    def __init__(self, cnf_file):
        self.filename = cnf_file

        #Open the file and get all the clauses
        f = open(self.filename, "r")
        lines = f.readlines()
        f.close()

        #get the clauses and split them into a list
        tmp_clauses = []
        for line in lines:
            tmp_clauses.append(line[:-1])

        #split the clause strings into a list
        tmp_clauses2 = []
        for i in tmp_clauses:
            tmp_clauses2.append(i.split())

        self.variables = []
        self.var_dict = {}
        self.clauses = []
        self.clause_dict = {}

        k = 1
        l = 0

        for j in tmp_clauses2:

            #avoid the clauses of length 1
            if len(j)>2:
                for m in j:

                    #check to see if the variable is in the variable dictionary
                    in_list = False
                    for var in self.var_dict:
                        if self.var_dict[var] == m:
                            in_list = True
                            break

                    #If it isn't in the dictionary add to the dictionary and the equivalent key to the list
                    if not in_list:
                        self.variables.append(k)
                        self.var_dict[k] = m
                        k+=1

        #create clause list and dictionary
        for p in tmp_clauses2:
            tmp_set = set()
            for n in p:

                #if the clause isn't negated check if it needs to be added to the dictionary
                if n[0] != "-":
                    for vari in self.var_dict:
                        if self.var_dict[vari] == n:
                            tmp_set.add(vari)
                            break
                #if the cluase is negated then check the dictionary for the positive and add it if need be
                else:
                    for vari in self.var_dict:
                        if self.var_dict[vari] == n[1:]:
                            tmp_set.add(-vari)
                            break

            #add the clause to the list and dictionary
            self.clauses.append(l)
            self.clause_dict[l] = tmp_set
            l += 1


        self.solution = []

    """
    GSAT solver
    """
    def GSAT(self,p = 3, max_flips=300, max_tries=4):

        #Tries to solve the max_tries amount of random truth tables
        for i in range(1, max_tries):

            #create a random truth assignment
            truth_assignment = {}
            print("\nnew truth assignment attempt")
            for num in self.variables:
                rand_num = random.randint(1,2)
                if rand_num == 1: truth_assignment[num] = True
                else: truth_assignment[num] = False

            #Does as many variable flips as allowed
            for j in range(1, max_flips):

                #if the truth assignment satisfies all the clauses it creats the solution list and returns true
                if self.satisfy(truth_assignment):
                    for t in truth_assignment:
                        if truth_assignment[t]:
                            self.solution.append(t)
                    return True

                #either randomly flip a variable or pick a variable to flip that will minimize the clause failures
                random_prob = random.randint(1,10)
                if p>=random_prob:
                    v = random.choice(self.variables)
                    print("random variable flipped: "+str(v))
                else:
                    v = self.var_to_flip(truth_assignment)

                #if there is a variable to flip, flip its assignment in the truth table
                if v != None:
                    if truth_assignment[v] == True:
                        truth_assignment[v] = False
                    else:
                        truth_assignment[v] = True
        return False


    """
    Chooses the variable to flip based on how many unsatisfied clauses the variable would fix
    """
    def var_to_flip(self, truth_assignment):
        tmp_truth_assignment = truth_assignment
        min_clause_fails = self.num_clause_fails(tmp_truth_assignment)
        var = []

        for i in tmp_truth_assignment:

            #switches the variable to test in the truth assignment
            if tmp_truth_assignment[i] == True:
                tmp_truth_assignment[i] = False
            else:
                tmp_truth_assignment[i] = True

            #Tests how many clause failures the truth assignment with the flipped variable would have
            k = self.num_clause_fails(tmp_truth_assignment)

            #If the number of clause failures is less than the current number of clause failures then make the variable
            #the new min. If it is equal to the current number, add it to the list
            if k<min_clause_fails:
                min_clause_fails = k
                var = [i]
            elif k == min_clause_fails:
                var.append(i)

            #revert the flipped variable back to the original state
            if tmp_truth_assignment[i] == True:
                tmp_truth_assignment[i] = False
            else:
                tmp_truth_assignment[i] = True
        print("variables to flip"+str(var))

        #picks a random variable to return out of the list of variables to flip
        if var != []:
            return random.choice(var)
        else:
            return None

    """
    Returns the number of clause failures for a given truth assignment
    """
    def num_clause_fails(self, truth_assignment):
        count = 0
        for i in self.clauses:
            tmp_bool = False

            #tests to see if the clause is satisfied by testing each variable in clause by the truth assignment
            for j in self.clause_dict[i]:
                if j in truth_assignment: tmp_bool = truth_assignment[j]
                elif abs(j) in truth_assignment: tmp_bool = not truth_assignment[abs(j)]
                if tmp_bool: break

            #adds 1 to the count if the clause is unsatisfied
            if not tmp_bool:
                count += 1
        return count

    """
    Tests if the truth assignment satisfies all clauses
    """
    def satisfy(self, truth_assignment):
        bool = True
        for i in self.clauses:
            tmp_bool = False

            #tests to see if the clause is satisfied by testing each variable in clause by the truth assignment
            for j in self.clause_dict[i]:
                if j in truth_assignment: tmp_bool = truth_assignment[j]
                elif abs(j) in truth_assignment: tmp_bool = not truth_assignment[abs(j)]
                if tmp_bool: break

            #if the truth assignment doesn't satisfy one clause return False
            bool = (bool and tmp_bool)
            if not bool:
                return False
        return True


    def WalkSAT(self, p=3, max_flips=100000):

        #create the random truth assignment
        truth_assignment = {}
        for num in self.variables:
            rand_num = random.randint(1,2)
            if rand_num == 1: truth_assignment[num] = True
            else: truth_assignment[num] = False

        #goes until it hits the limit on number of variables flipped
        for j in range(1, max_flips):

            #if the truth_assignment satifies all the clauses create the solution and return True
            if self.satisfy(truth_assignment):
                for t in truth_assignment:
                    if truth_assignment[t]:
                        self.solution.append(t)
                return True

            #Pick a random unsatisfied clause
            clause = self.rand_false_clause_find(truth_assignment)

            #Pick either a random variable or the variable with the most clause failures within the clause
            if p>=random.randint(1,10):
                v = random.choice(self.variables)
                print("random variable flipped: "+str(v))
            else:
                v = self.clause_var_to_flip(clause, truth_assignment)

            #if the variable is not None, flip it
            if v!=None:
                if truth_assignment[v] == True:
                    truth_assignment[v] = False
                else:
                    truth_assignment[v] = True
        return False

    """
    Iterates through all the failed clauses then picks one at random
    """
    def rand_false_clause_find(self, truth_assignment):
        false_clauses = []
        for i in self.clauses:
            tmp_bool = False

            #test to see if the clause is unsatisfied
            for j in self.clause_dict[i]:
                if j in truth_assignment: tmp_bool = truth_assignment[j]
                elif abs(j) in truth_assignment: tmp_bool = not truth_assignment[abs(j)]
                if tmp_bool: break

            #if the clause is unsatisfied add to the list
            if not tmp_bool: false_clauses.append(i)
        return random.choice(false_clauses)

    """
    Within the given clause pick the variable with the highest number of clause failures
    """
    def clause_var_to_flip(self, clause, truth_assignment):
        tmp_truth_assignment = truth_assignment
        min_clause_fails = self.num_clause_fails(tmp_truth_assignment)
        var = []
        for j in self.clause_dict[clause]:
            i = abs(j)

            #switches the variable to flip in the truth assignment
            if tmp_truth_assignment[i] == True:
                tmp_truth_assignment[i] = False
            else:
                tmp_truth_assignment[i] = True

            #Tests how many clause failures the truth assignment with the flipped variable would have
            k = self.num_clause_fails(tmp_truth_assignment)

            # If the number of clause failures is less than the current number of clause failures then make the variable
            # the new min. If it is equal to the current number, add it to the list
            if k < min_clause_fails:
                min_clause_fails = k
                var = [i]
            elif k == min_clause_fails:
                var.append(i)

            # revert the flipped variable back to the original state
            if tmp_truth_assignment[i] == True:
                tmp_truth_assignment[i] = False
            else:
                tmp_truth_assignment[i] = True
        print("variables to flip" + str(var))

        # picks a random variable to return out of the list of variables to flip
        if var != []:
            return random.choice(var)
        else:
            return None


    def write_solution(self, filename):
        f = open(filename, "w")

        for i in self.solution:
            f.write(self.var_dict[i])
            f.write("\n")

        f.close()