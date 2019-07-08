#Corbin Mayes 1/17/19
#Talked with Hunter Gallant

from SearchSolution import SearchSolution
from heapq import heappush, heappop

class AstarNode:
    # each search node except the root has a parent node
    # and all search nodes wrap a state object

    def __init__(self, state, heuristic, parent=None, transition_cost=0):
        #classify the instance variables
        self.state = state
        self.heuristic = heuristic
        self.parent = parent
        self.transition_cost = transition_cost

    def priority(self):
        # calculate the priority of the node
        return (self.heuristic + self.transition_cost)

    # comparison operator,
    # needed for heappush and heappop to work with AstarNodes:
    def __lt__(self, other):
        return self.priority() < other.priority()


# take the current node, and follow its parents back
#  as far as possible. Grab the states from the nodes,
#  and reverse the resulting list of states.
def backchain(node):
    result = []
    current = node
    while current:
        result.append(current.state)
        current = current.parent

    result.reverse()
    return result


def astar_search(search_problem, heuristic_fn):
    #get the start start node and add it to the heap
    start_node = AstarNode(search_problem.start_state, heuristic_fn(search_problem.start_state))
    pqueue = []
    heappush(pqueue, start_node)

    #create the solution
    solution = SearchSolution(search_problem, "Astar with heuristic " + heuristic_fn.__name__)

    visited_cost = {}
    if type(start_node.state) is list:
        visited_cost[start_node.state] = 0
    elif type(start_node.state) is set:
        visited_cost[frozenset(start_node.state)] = 0
    elif type(start_node.state) is tuple:
        visited_cost[start_node.state] = 0

    explored = set()

    while pqueue:
        #get the next node on the heap
        node = heappop(pqueue)
        if type(node.state) is list or type(node.state) is tuple:
            explored.add(node.state)
        elif type(node) is set:
            explored.add(frozenset(node.state))

        #test if its the goal
        if search_problem.goal_test(node.state):
            solution.path = backchain(node)
            solution.nodes_visited = len(explored)
            if type(node) is list or type(node) is tuple:
                solution.cost = visited_cost[node.state]
            elif type(node) is set:
                solution.cost = visited_cost[frozenset(node.state)]
            return solution

        #get the children of the node
        for child in search_problem.get_successors(node.state):
            child_node = AstarNode(child, heuristic_fn(child), node, len(backchain(node))+1)
            if type(child_node.state) is list or type(child_node.state) is tuple:
                visited_cost[child_node.state] = child_node.transition_cost
            elif type(child_node.state) is set:
                visited_cost[frozenset(child_node.state)] = child_node.transition_cost
            #add the child to the heap if not seen
            if child_node not in backchain(node):
                if child_node not in pqueue and child_node.state not in explored:
                    heappush(pqueue, child_node)
                #if child is already in heap then test for the priority to get the best solution
                elif child_node in pqueue:
                    equal_node = pqueue[child_node]
                    if child_node.priority() < equal_node.priority():
                        del pqueue[equal_node]
                        heappush(pqueue, child_node)
    solution.path = []
    return solution


