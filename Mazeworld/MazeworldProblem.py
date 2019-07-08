#Author Corbin Mayes 1/17/19
#Discussed with Hunter Gallant

from Maze import Maze
from time import sleep

class MazeworldProblem:

    ## you write the constructor, and whatever methods your astar function needs

    def __init__(self, maze, goal_locations):
        self.goal = goal_locations
        self.maze = maze
        tmp_start_state = self.maze.robotloc
        tmp_start_state.append(1)
        self.start_state = tuple(tmp_start_state)
        self.botloc = self.maze.robotloc


        self.parent_child_hashmap = {}

    def __str__(self):
        string =  "Mazeworld problem: "
        return string

    #updates current location of robots
    def updatebots(self, state):
        state_list = list(state)
        state_list.pop(len(state_list)-1)
        self.botloc = state_list

    def get_successors(self, state):
        #update the robots' locations
        self.updatebots(state)
        current_state = state

        tmp_tuple_list = []

        #get all 4 options of moves
        for k in range(0, 4):
            tmp_state = []
            #get the whole state
            for j in range(0, len(state)-1, 2):
                tmp_state.append(state[j])
                tmp_state.append(state[j+1])
                robot_moved = state[len(state)-1]

                #move the correct robot
                if j == (robot_moved-1)*2:
                    if k == 0:
                        tmp_state[j] = tmp_state[j] + 1
                    elif k == 1:
                        tmp_state[j] = tmp_state[j] - 1
                    elif k == 2:
                        tmp_state[j+1] = tmp_state[j+1] + 1
                    elif k == 3:
                        tmp_state[j+1] = tmp_state[j+1] - 1

            #update the robot to be moved
            tmp_state.append(state[len(state)-1]+1)
            if tmp_state[len(tmp_state)-1] > len(tmp_state)/2:
                tmp_state[len(tmp_state)-1] = 1
            #add to list to be checked for rules
            tmp_tuple_list.append(tuple(tmp_state))



        passed_tuple_list = []
        for i in tmp_tuple_list:
            #if it passes the rules then add to passed list
            if self.rules(i, state):
                passed_tuple_list.append(i)
        #if in the beginning the first robot can't move test the
        #other robots until one moves or if none can move says
        #no possible moves
        if state == self.start_state:
            if passed_tuple_list != []:
                return passed_tuple_list
            elif current_state[6] <= len(current_state)/2:
                next_robot_move = []
                for i in range(0,len(state)-1):
                    next_robot_move.append(state[i])
                next_robot_move.append(state[len(state)-1]+1)
                passed_tuple_list.insert(0, tuple(next_robot_move))
                return self.get_successors(tuple(next_robot_move))
            else:
                return 'no possible moves'
        else:
            return passed_tuple_list



    def rules(self, state, parent_state):
        #test if the state has all the x and y points greater than or equal to 0
        if not min(state)<= -1:

            #test x points to be less than the width of the maze
            is_in_maze_x = True
            for x in range(0,len(state)-1,2):
                if state[x] > self.maze.width:
                    is_in_maze_x = False
            if is_in_maze_x:

                #test y points to be less than the height of the maze
                is_in_maze_y = True
                for y in range(1,len(state)-1,2):
                    if state[y] > self.maze.height:
                        is_in_maze_y = False
                if is_in_maze_y:

                    #Make sure all robots are on the floor tiles and not on walls
                    all_is_floor = True
                    for index in range(0,len(state)-1,2):
                        if not self.maze.is_floor(state[index], state[index+1]):
                            all_is_floor = False
                    if all_is_floor:

                        #Make sure no robots intersect
                        no_intersection = True
                        if (int(len(state)/2))>1:
                            robot_moved = parent_state[len(parent_state)-1]
                            if self.has_bot(state[(robot_moved-1)*2], state[((robot_moved-1)*2)+1]):
                                no_intersection = False
                            if no_intersection:
                                return True
                        else:
                            return True
        return False


        # given a sequence of states (including robot turn), modify the maze and print it out.
        #  (Be careful, this does modify the maze!)

    def animate_path(self, path):
        # reset the robot locations in the maze
        self.maze.robotloc = tuple(self.start_state)

        for state in path:
            print(str(self))
            if int(len(state)-1)/2 > 1:
                self.maze.robotloc = tuple(state[0:(len(state)-1)])
            else:
                self.maze.robotloc = tuple(state[0:(len(state))])
            sleep(1)

            print(str(self.maze))

    def goal_test(self, state):
        test_list = list(state)
        test_list.pop(len(test_list)-1)
        robot_locations = tuple(test_list)
        return self.goal == robot_locations

    def has_bot(self, x, y):
        if x < 0 or x >= self.maze.width:
            return False
        if y < 0 or y >= self.maze.height:
            return False

        for i in range(0, len(self.botloc), 2):
            rx = self.botloc[i]
            ry = self.botloc[i + 1]
            if rx == x and ry == y:
                return True

        return False

    def manhattan_heuristic(self, state):
        heuristic = 0
        for i in range(0,len(state)-1):
            heuristic += abs(self.goal[i]-state[i])
        return heuristic




## A bit of test code. You might want to add to it to verify that things
#  work as expected.

if __name__ == "__main__":
    test_maze3 = Maze("maze3.maz")
    test_mp = MazeworldProblem(test_maze3, (1, 4, 1, 3, 1, 2))

    print(test_mp.get_successors((1, 0, 1, 1, 2, 1, 3)))
