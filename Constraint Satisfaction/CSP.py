"""
Corbin Mayes - 1/31/19
Discussed with Hunter Gallant
"""

class CSP:
    def __init__(self, variables, domains, neighbors, constraints):
        self.variables = variables
        self.domains = domains
        self.neighbors = neighbors
        self.constraints = constraints
        self.curr_domains = None
        self.num_assigns = 0

    """
    assigns a variable a value in the assignment
    """
    def assign(self, var, value, assignment):
        assignment[var] = value
        self.num_assigns += 1

    """
    removes an assignment
    """
    def unassign(self, var, assignment):
        if var in assignment:
            del assignment[var]

    """
    returns the number of conflicts for a given variable and value
    """
    def num_conflicts(self, var, value, assignment):
        count = 0
        for v in self.neighbors[var]:
            if v in assignment and not self.constraints(var, value, v, assignment[v], assignment):
                count += 1
        return count

    """
    allows the pruning of values from the domain
    """
    def support_pruning(self):
        if self.curr_domains is None:
            tmp_dict = {}
            for v in self.variables:
                tmp_dict[v] = list(self.domains)
            self.curr_domains = tmp_dict

    """
    begins to accumulate inferences assuming that var=value
    """
    def suppose(self, var, value):
        self.support_pruning()
        removals = []
        for r in self.curr_domains[var]:
            if r != value:
                removals.append((var, r))
        self.curr_domains[var] = [value]
        return removals

    """
    rules out var=value
    """
    def prune(self, var, value, removals):
        self.curr_domains[var].remove(value)
        if removals is not None:
            removals.append((var, value))

    """
    returns all possibilities that haven't been ruled out for var
    """
    def choices(self, var):
        return self.domains

    """
    returns the partial assignment of the current inference
    """
    def infer_assignment(self):
        self.support_pruning()
        tmp_assignment = {}
        for v in self.variables:
            if len(self.curr_domains[v]) == 1:
                tmp_assignment[v] = self.curr_domains[v][0]
        return tmp_assignment
    """
    undo a suppositon and all inferences from it
    """
    def restore(self, removals):
        for R,r in removals:
            self.curr_domains[R].append(r)

    """
    returns if a goal state has been found
    """
    def goal_test(self, assignment):
        if len(assignment) == len(self.variables):
            return True
        return False