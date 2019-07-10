
#discussed with Hunter Gallant

from collections import deque
from SearchSolution import SearchSolution

class SearchNode:

    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent


def bfs_search(search_problem):
    #creates the graph of the problem
    search_problem.get_successors(search_problem.start_state)
    while len(search_problem.inspect)>0:
        for i in search_problem.inspect:
            search_problem.get_successors(i)

    #maintains the visited nodes and queues ones that haven't been visited yet
    visited = set([search_problem.start_state])
    queue = deque([search_problem.start_state])

    while queue:
        #get the next node to be searched
        vertex = queue.popleft()
        #makes sure the node is within the graph
        if vertex in search_problem.hashmap:
            #get the nodes children
            for j in search_problem.hashmap[vertex]:
                #test the children to see if it is the goal
                if search_problem.test_goal_state(j):
                    return backchain_helper(j, search_problem.child_parent_hashmap)
                if j not in visited:
                    visited.add(j)
                    queue.append(j)

#Backchains the found goal to get the path back to the starting position
def backchain_helper(found_state, parent_map):
    goal_path = []
    if parent_map[found_state] == None:
        return [found_state]
    else:
        goal_path = backchain_helper(parent_map[found_state], parent_map)
        goal_path.append(found_state)
    return goal_path


def dfs_search(search_problem, depth_limit=100, node=None, solution=None):
    #calls the recursive function which returns a path
    goal_node = recursive_dfs_helper(search_problem, node, depth_limit)
    #this is just a if statement to get only the path of the problem being run because
    #if multiple problems are being run it adds previous paths to later paths
    if goal_node != 'cutoff':
        final_goal = []
        i = 0
        while not search_problem.test_goal_state(goal_node[i]):
            final_goal.append(goal_node[i])
            i += 1
        final_goal.append(goal_node[i])
        return final_goal
    else:
        return goal_node
    # if no node object given, create a new search from starting state

def recursive_dfs_helper(search_problem, node, depth_limit, path = []):
    #just starts at the start node if not specified
    if node == None:
        node =  search_problem.start_state
    #if the node is the goal end the recursion and add to path
    if search_problem.test_goal_state(node):
        #path = [node]
        path.insert(0,node)
        return path
    #if the depth limit is hit without finding the goal then it ends the recursion
    elif depth_limit == 0:
        return 'cutoff'
    else:
        cutoff_occurred = False
        #create the graph
        search_problem.get_successors(node)
        if node in search_problem.hashmap:
            for child in search_problem.hashmap[node]:
                #calls the recursive function for the children of the node
                result = recursive_dfs_helper(search_problem, child, depth_limit-1, path)
                if result == 'cutoff':
                    cutoff_occurred = True
                #this returns the path if the goal was found
                elif result != None:
                    path.insert(0, node)
                    return path
                #cutsoff if limit hit
                if cutoff_occurred:
                    return 'cutoff'


#repeats the dfs until the it doens't cutoff and returns the path of the found goal
def ids_search(search_problem, depth_limit=100):
    for i in range(1,depth_limit+1):
        path = dfs_search(search_problem,i)
        if path != 'cutoff':
            return path
