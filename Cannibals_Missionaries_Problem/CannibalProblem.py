
#discussed assignment with Hunter Gallant

class CannibalProblem:
    def __init__(self, start_state=(3, 3, 1)):
        self.start_state = start_state
        self.goal_state = (0, 0, 0)

        #list of nodes to be visited
        self.inspect = []

        #list of visited nodes
        self.visited = []

        #table that tracks edges of the graph from parent to children
        self.hashmap = {}

        #table that maintains the list of child to parent edge
        self.child_parent_hashmap = {self.start_state:None}

    # get successor states for the given state
    def get_successors(self, state):
        if state in self.inspect:
            self.inspect.remove(state)

        if not state in self.visited:
            self.visited.append(state)

        tmp_tuple_list = []

        #adds possible tuples if boat is on left side
        if state[2] == 1:
            tmp_tuple_list.append((state[0] - 1,state[1],0))
            tmp_tuple_list.append((state[0] - 2, state[1], 0))
            tmp_tuple_list.append((state[0] - 1, state[1] - 1, 0))
            tmp_tuple_list.append((state[0], state[1] - 1, 0))
            tmp_tuple_list.append((state[0], state[1] - 2, 0))

        #adds possible tuples if boat is on right side
        elif state[2] == 0:
            tupleRight = (self.start_state[0] - state[0], self.start_state[1] - state[1], self.start_state[2] - state[2])

            #if statements make sure that there are enough people on the right side to pull from
            if tupleRight[0]>=1:
                tmp_tuple_list.append((state[0] + 1, state[1], 1))
            if tupleRight[0]>=2:
                tmp_tuple_list.append((state[0] + 2, state[1], 1))
            if tupleRight[0]>=1 and tupleRight[1]>=1:
                tmp_tuple_list.append((state[0] + 1, state[1] + 1, 1))
            if tupleRight[1]>=1:
                tmp_tuple_list.append((state[0], state[1] + 1, 1))
            if tupleRight[1]>=2:
                tmp_tuple_list.append((state[0], state[1]+2, 1))

        #tests the tuples within the helper method
        for i in tmp_tuple_list:
            self.helper(i,state)

    #helper method that tests the rules of a tuple
    def helper(self, tupleLeft, parentState):
        #find the number of cannibals and missionaries on other side of river
        tupleRight = (self.start_state[0]-tupleLeft[0],self.start_state[1]-tupleLeft[1],self.start_state[2]-tupleLeft[2])

        #test if within bounds
        if min(tupleLeft)>=0 and max(tupleLeft)<=max(self.start_state):

            #test if within lists
            if not tupleLeft in self.inspect and not tupleLeft in self.visited:

                #test if more cannibals than missionaries on left side
               if tupleLeft[0]>=tupleLeft[1] or tupleLeft[0] == 0:

                    #test if more cannibals than missionaries on right side
                    if tupleRight[0]>=tupleRight[1] or tupleRight[0] == 0:
                        self.inspect.append(tupleLeft)
                        if parentState in self.hashmap:
                            self.hashmap[parentState].append(tupleLeft)
                        else:
                            self.hashmap[parentState] = [tupleLeft]

                        self.child_parent_hashmap[tupleLeft] = parentState

    #goal test funcion
    def test_goal_state(self, state):
        if self.goal_state == state:
            return True
        else:
            return False

    #to string method
    def __str__(self):
        string =  "Missionaries and cannibals problem: " + str(self.start_state)
        return string


## A bit of test code

if __name__ == "__main__":
    test_cp = CannibalProblem((3, 3, 1))
    print(test_cp.get_successors((3, 3, 1)))
    #print(test_cp)
    #print(test_cp.inspect)
    while len(test_cp.inspect)>0:
        for i in test_cp.inspect:
            #print(test_cp.inspect)
            test_cp.get_successors(i)
            print(test_cp.child_parent_hashmap)
    #print(len(test_cp.visited))
