"""
Corbin Mayes - 1/31/19
Discussed with Hunter
"""

from CSP import CSP
from BacktrackingSolver import BacktrackingSolver

class Person:
    def __init__(self, name, availability, is_leader):
        self.name = name
        self.availability = availability
        self.is_leader = is_leader

class CS1SectionCSP:

    def __init__(self, section_leaders, students, sections):
        self.num_leaders = len(section_leaders)
        self.num_students = len(students)
        self.variables = []
        self.var_dict = {}

        #creates the variables list and the corresponding dictionary
        for i in range(0, len(section_leaders)):
            self.variables.append(i)
            self.var_dict[i] = Person(section_leaders[i][0]+'*', section_leaders[i][1:len(section_leaders[i])], True)
        pos = len(self.variables)
        for j in range(len(self.variables), len(self.variables)+len(students)):
            self.variables.append(j)
            self.var_dict[j] = Person(students[j-pos][0], students[j-pos][1:len(students[j-pos])], False)

        self.domains = []
        self.dom_dict = {}
        #creates the domain adn the corresponding dictionary of values
        for k in range(0, len(sections)):
            self.domains.append(k)
            self.dom_dict[k] = sections[k]

        #creates the neighbors list for the CSP to use
        self.neighbors = {}
        for m in range(0, len(self.variables)):
            for n in range(0, len(self.variables)):
                if m not in self.neighbors:
                    self.neighbors[m] = [n]
                else:
                    self.neighbors[m].append(n)

        self.csp = CSP(self.variables, self.domains, self.neighbors, self.constraints)


    def constraints(self, var1, val1, var2, val2, assignment):
        #make sure that the persoin is actually available at the time
        if self.dom_dict[val1] not in self.var_dict[var1].availability:
            return False

        #there cannot be two section leaders per section
        if self.var_dict[var1].is_leader and self.var_dict[var2].is_leader and val1 == val2 and self.var_dict[var1].name != self.var_dict[var2].name:
            return False

        # makes sure there are no sections with fewer than n/k -1 or greater than n/k +1 students
        if len(assignment) == len(self.variables):

            #count the number of students per section
            count_dict = {}
            for i in assignment:
                if assignment[i] in count_dict:
                    count_dict[assignment[i]] = count_dict[assignment[i]] + 1
                else:
                    count_dict[assignment[i]] = 1

            #check the size of each section
            for c in count_dict:
                if self.num_students%self.num_leaders == 0:
                    if count_dict[c]<((self.num_students/self.num_leaders)-1) or count_dict[c]>((self.num_students/self.num_leaders)+1):
                        return False
                else:
                    if count_dict[c]<((self.num_students/self.num_leaders)-1) or count_dict[c]>((self.num_students/self.num_leaders)+2):
                        return False

            #check to make sure there is at least one leader within the section
            for p in assignment:
                if self.var_dict[p].is_leader:
                    if assignment[p] == val1:
                        return True
            return False
        return True


    def solve(self):
        backtrack_solver = BacktrackingSolver()
        tmp = backtrack_solver.Backtracking_Search(self.csp)
        result = {}
        if tmp != None:
            for i in tmp:
                result[self.var_dict[i].name] = self.dom_dict[tmp[i]]
            return result
        else:
            return 'There is no possible section assignment'