#Corbin Mayes 1/17/19
#Spoke with Hunter Gallant

from Maze import Maze
from MazeworldProblem import MazeworldProblem
from SensorlessProblem import SensorlessProblem

from uninformed_search import bfs_search
from astar_search import astar_search

test_maze3 = Maze("maze3.maz")
test_sp = SensorlessProblem(test_maze3, (1, 4))

test_maze2 = Maze("maze2.maz")
test_sp1 = SensorlessProblem(test_maze2, (3,0))

test_maze4 = Maze("maze4.maz")
test_sp2 = SensorlessProblem(test_maze4, (0,4))

test_maze5 = Maze("maze5.maz")
test_sp3 = SensorlessProblem(test_maze5, (4,5))


result = astar_search(test_sp, test_sp.zero_heuristic)
print(result)
if result.path != []:
   test_sp.to_goal(result.path[len(result.path)-1])

result = astar_search(test_sp1, test_sp1.zero_heuristic)
print(result)
if result.path != []:
    test_sp1.to_goal(result.path[len(result.path)-1])

#result = astar_search(test_sp2, test_sp2.zero_heuristic)
#print(result)
#if result.path != []:
#   test_sp2.to_goal(result.path[len(result.path)-1])

#result = astar_search(test_sp3, test_sp3.zero_heuristic)
#print(result)
#if result.path != []:
    #test_sp2.to_goal(result.path[len(result.path)-1])