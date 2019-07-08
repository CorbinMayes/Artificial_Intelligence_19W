#Corbin Mayes 1/17/19
#Spoke with Hunter Gallant

from Maze import Maze
from time import sleep

from MazeworldProblem import MazeworldProblem

from uninformed_search import bfs_search
from astar_search import astar_search

class SensorlessProblem:

    def __init__(self, maze, goal_location):
        self.maze = maze
        self.goal = goal_location
        self.start_state = set()
        for w in range(0, self.maze.width):
            for h in range(0, self.maze.height):
                if self.maze.is_floor(w,h):
                    self.start_state.add((w,h))

    def __str__(self):
        string =  "Blind robot problem: "
        return string

    def get_successors(self, state):
        tmp_list = []
        tmp_list.append(self.north(state))
        tmp_list.append(self.south(state))
        tmp_list.append(self.east(state))
        tmp_list.append(self.west(state))

        passed_list = []
        for test in tmp_list:
            #if the set of possible states collapses then add to list
            if len(test)!= len(state):
                passed_list.append(test)
        if passed_list != []:
            return passed_list
        else:
            return 'no possible moves'

    #moves all possible states up 1
    def north(self, state):
        tmp_state = set()
        for loc in state:
            if self.maze.is_floor(loc[0],loc[1]+1):
                if loc[0]>=0 and loc[0]<self.maze.width:
                    if loc[1]+1>=0 and loc[1]+1<self.maze.height:
                        tmp_loc = (loc[0], loc[1]+1)
                        tmp_state.add(tmp_loc)
        return tmp_state

    #moves all possible states down 1
    def south(self, state):
        tmp_state = set()
        for loc in state:
            if self.maze.is_floor(loc[0],loc[1]-1):
                if loc[0]>=0 and loc[0]<=self.maze.width:
                    if loc[1]-1>=0 and loc[1]-1<self.maze.height:
                        tmp_loc = (loc[0], loc[1]-1)
                        tmp_state.add(tmp_loc)
        return tmp_state

    #moves all possible states right 1
    def east(self, state):
        tmp_state = set()
        for loc in state:
            if self.maze.is_floor(loc[0]+1,loc[1]):
                if loc[0]+1>=0 and loc[0]+1<self.maze.width:
                    if loc[1]>=0 and loc[1]<self.maze.height:
                        tmp_loc = (loc[0]+1, loc[1])
                        tmp_state.add(tmp_loc)
        return tmp_state

    #moves all possible states left 1
    def west(self, state):
        tmp_state = set()
        for loc in state:
            if self.maze.is_floor(loc[0]-1,loc[1]):
                if loc[0]-1>=0 and loc[0]-1<self.maze.width:
                    if loc[1]>=0 and loc[1]<self.maze.height:
                        tmp_loc = (loc[0]-1, loc[1])
                        tmp_state.add(tmp_loc)
        return tmp_state

    #The heuristic that adds up all the possible distances from the point
    #(0,0). The fewer possible points in the state then the less the heuristic
    #is.
    def zero_heuristic(self, state):
        heuristic = 0
        if state != set():
            for loc in state:
                heuristic += abs(0 - loc[0])
                heuristic += abs(0 - loc[1])
        else:
            heuristic = 999999999
        return heuristic

    #Test if the state is a singleton
    def goal_test(self, state):
        if len(state) == 1:
            return True
        return False

    #once the robot's location is known it moves to the stated goal in using
    #the mazeworld problem with a single robot
    def to_goal(self, state):
        tmp_state = state.copy()
        loc = tmp_state.pop()
        to_goal_problem = MazeworldProblem(self.maze, self.goal)
        to_goal_problem.start_state = (loc[0], loc[1])
        to_goal_problem.botloc = loc
        result = astar_search(to_goal_problem, to_goal_problem.manhattan_heuristic)
        print(result)

        # given a sequence of states (including robot turn), modify the maze and print it out.
        #  (Be careful, this does modify the maze!)

    def animate_path(self, path):
        # reset the robot locations in the maze
        self.maze.robotloc = tuple(self.start_state)

        for state in path:
            for item in state:
                print(str(self))
                self.maze.robotloc = tuple(item)
                sleep(1)

            print(str(self.maze))


## A bit of test code

if __name__ == "__main__":
    test_maze3 = Maze("maze3.maz")
    test_problem = SensorlessProblem(test_maze3, (1,0))
    print(test_problem.start_state)
    print(test_problem.get_successors(test_problem.start_state))
