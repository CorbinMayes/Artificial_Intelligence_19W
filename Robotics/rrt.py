# using shapely for collision detection

import random
import shapely
from shapely.geometry import Polygon, Point
from planar_trajectory import PlanarTrajectory
from planarsim import controls_rs

class RRT:
    def __init__(self, traj, num_vert, distance):
        self.trajectory = traj
        self.num_vertices = num_vert
        self.incr_dist = distance
        self.tree = {}

        self.init_configuration = tuple(self.trajectory.q)
        self.tree[self.init_configuration] = []

    """
    builds the RRT graph
    """
    def rrt(self):
        for i in range(1, self.num_vertices+1):
            q_rand = self.random_configuration()
            q_near = self.nearest_vertex(q_rand)
            q_new = self.new_conf(q_rand, q_near)
            self.tree[q_new] = q_near
        return self.tree

    """
    create a random configuration of x,y,theta values
    """
    def random_configuration(self):
        rand_x = random.uniform(0.0, 8.0)
        string_x = '%.1f'%(rand_x)
        float_x = float(string_x)

        rand_y = random.uniform(0.0, 3.0)
        string_y = '%.1f' % (rand_y)
        float_y = float(string_y)

        rand_theta = random.uniform(-1.0, 1.0)
        string_theta = '%.1f' % (rand_theta)
        float_theta = float(string_theta)

        return (float_x, float_y, float_theta)


    """
    gets the nearest vertex to the random one
    """
    def nearest_vertex(self, rand_vertex):
        dist_dict = {}
        curr_min = None

        for vert in self.tree:
            dist_dict[vert] = self.dist_heur(rand_vertex, vert)
            if curr_min == None:
                curr_min = vert
            else:
                if dist_dict[curr_min] > dist_dict[vert]:
                    curr_min = vert
        return curr_min


    """
    calculate the distance between two vertices
    """
    def dist_heur(self, rand, vert):
        return abs(rand[0] - vert[0]) + abs(rand[1] - vert[1])


    """
    choose the new configuration
    """
    def new_conf(self, rand_vert, near_vert):
        rand_conf = self.random_configuration()
        dist_near = self.dist_heur(rand_vert, near_vert)
        dist_new = self.dist_heur(rand_vert, rand_conf)

        while (dist_near + self.incr_dist) < dist_new < (dist_near + self.incr_dist):
            rand_conf = self.random_configuration()
            dist_new = self.dist_heur(rand_vert, rand_conf)

        return rand_conf

if __name__ == "__main__":
    poly = Polygon(((0, 0), (0, 1), (1, 1), (1, 0)))
    point = Point(2, .2)

    random.seed(1)
    #print(poly)
    #print(poly.contains(point))
    new_trajectory = PlanarTrajectory(controls_rs, 0, 0, 0, [0, 3, 5, 3], [1.0, 2.0, 2.0, 4.0])
    test_rrt = RRT(new_trajectory, 100, 0.5)
    print(test_rrt.rrt())
