"""
Corbin Mayes 3/5/19
Discussed with Hunter Gallant
"""

import random, math
from Kinematics import Kinematics

class PRM:
    def __init__(self, start_state, goal_state, obstacles, arm, lengths):
        self.start = start_state
        self.goal = goal_state
        self.obstacles = obstacles
        self.robo_arm = arm
        self.lengths = lengths

    def get_path(self, num):
        if self.start == self.goal:
            return[self.start]

        roadmap = self.build_roadmap(num)

        queue = [[self.start]]
        curr_path_num = 0

        while curr_path_num < len(queue):
            current_path = queue[curr_path_num]
            curr_path_num +=1
            vertex = current_path[-1]

            if len(roadmap[tuple(vertex)])>0:
                for neighbor in roadmap[vertex]:
                    if neighbor == self.goal:
                        current_path.append(neighbor)
                        return current_path
                    if neighbor not in current_path:
                        tmp_path = current_path.copy()
                        tmp_path.append(neighbor)
                        queue.append(tmp_path)
        return None

    def build_roadmap(self, num):
        roadmap = {}
        i = 0

        while i<num:
            if 1<i:
                rand_thetas = tuple(self.gen_rand_thetas())
                while rand_thetas in roadmap:
                    rand_thetas = tuple(self.gen_rand_thetas())
            elif i == 1:
                rand_thetas = self.goal
            else:
                rand_thetas = self.start

            if self.check_no_collision(rand_thetas):
                roadmap[tuple(rand_thetas)] = []
                i+=1
                neighborhood_list = self.check_neighbors(rand_thetas, roadmap)
                if len(neighborhood_list)>0:
                    for neighbor in neighborhood_list:
                        if neighbor != rand_thetas and self.connect(rand_thetas, neighbor):
                            roadmap[tuple(rand_thetas)].append(neighbor)
                            roadmap[tuple(neighbor)].append(rand_thetas)
        return roadmap

    def gen_rand_thetas(self):
        rand_thetas = []
        for i in range(0, len(self.start)):
            rand_thetas.append(self.get_rand_theta())
        return rand_thetas

    def get_rand_theta(self):
        rand_value = random.uniform(0, 2*math.pi)
        value = '%.1f'%(rand_value)
        theta = float(value)
        return theta

    def check_no_collision(self, thetas):
        k = Kinematics(thetas, self.lengths)

        tmp_arm = self.robo_arm

        for i in range(0, len(tmp_arm.joints)):
            tmp_arm.joints[i].theta = k.thetas[i]
        for j in range(1, len(tmp_arm.joints)):
            xy = k.calc_xy(j, tmp_arm.joints)
            tmp_arm.joints[j].x = xy[0]
            tmp_arm.joints[j].y = xy[1]
        tmp_arm.end_claw = k.calc_xy(j+1, tmp_arm.joints)

        for object in self.obstacles:
            if self.robo_arm.object_collision(object):
                return False

        return True

    def check_neighbors(self, thetas, roadmap):
        neighbor_list = []

        for tmp_tuple in roadmap:
            if (thetas[0]-0.2) <= tmp_tuple[0] <= (thetas[0]+0.2):
                neighbor_list.append(tmp_tuple)
        return neighbor_list

    def connect(self, thetas, neighbor):
        tmp_arm = self.robo_arm
        goal_reached = False
        num = 0
        while not goal_reached:
            num +=1
            goal_reached = True
            tmp_arm = self.update_arm(tmp_arm, thetas, neighbor, num)
            for object in self.obstacles:
                if tmp_arm.object_collision(object):
                    return False
            for i in range(0, len(tmp_arm.thetas)):
                if tmp_arm.thetas[i] != neighbor[i]:
                    goal_reached = False


    def update_arm(self, robo_arm, start_thetas, goal_thetas, num_iter):
        tmp_arm = robo_arm
        tmp_thetas = []
        for i in range(0, len(tmp_arm.thetas)):
            new_theta = tmp_arm.thetas[i] * (1 - (num_iter / (60 * 5))) + goal_thetas[i] * (
                        num_iter / (60 * 5))
            tmp_thetas.append(new_theta)
        kin = Kinematics(tmp_thetas, tmp_arm.length_arms)

        tmp_arm.thetas = tmp_thetas
        for i in range(0, len(tmp_arm.joints)):
            tmp_arm.joints[i].theta = kin.thetas[i]
        for j in range(1, len(tmp_arm.joints)):
            xy = kin.calc_xy(j, tmp_arm.joints)
            tmp_arm.joints[j].x = xy[0]
            tmp_arm.joints[j].y = xy[1]
        tmp_arm.end_claw = kin.calc_xy(j+1, tmp_arm.joints)

        return tmp_arm
