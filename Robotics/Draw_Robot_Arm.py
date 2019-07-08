"""
Corbin Mayes 3/3/19
Discussed with Hunter Gallant
"""

import cs1lib
import math
from Kinematics import Kinematics
import random
from PRM import PRM

class Robot_arm:
    def __init__(self, joint_thetas = [], arm_lengths = []):
        self.thetas = joint_thetas
        self.length_arms = arm_lengths
        self.joints = []
        self.joints.append(joint(0,50,self.thetas[0]))
        self.end_claw = (0,0)

    def add_joints(self):
        k = Kinematics(self.thetas, self.length_arms)
        for i in range(1,len(self.thetas)):
            xy = k.calc_xy(i, self.joints)
            self.joints.append(joint(xy[0], xy[1], self.thetas[i]))
        self.end_claw = k.calc_xy(i+1, self.joints)

    def object_collision(self, object):
        for j in range(0, len(self.joints)-1):
            jone = self.joints[j]
            jtwo = self.joints[j+1]
            slope = (jtwo.y - jone.y)/(jtwo.x - jone.x)

            tmp_x = jone.x
            tmp_y = jone.y
            coords_list = []

            end = int(jtwo.y-jone.y+1)
            for i in range(0, end):
                coords_list.append((tmp_x,tmp_y))
                tmp_x += 1
                tmp_y += slope

            for pos in coords_list:
                if object.x_range[0] <= pos[0] <= object.x_range[1]:
                    if object.y_range[0] <= pos[1] <= object.y_range[1]:
                        return True
        return False



class joint:
    def __init__(self, x, y, theta = 0):
        self.x = x
        self.y = y
        self.theta = theta

class Object:
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r
        self.x_range = (x-r, x+r)
        self.y_range = (y-r, y+r)

    def draw_obj(self):
        cs1lib.draw_circle(300+self.x, 600-self.y, self.r)



def graphics():
    global pause_start
    global obstacle_collision
    global collisions, current_goal, current_pos, obstacle_collision
    global pathway, collision_last_time, num_of_collision
    global final_thetas, last_time_positive
    pause_start += 1

    cs1lib.clear()
    cs1lib.set_stroke_width(3)

    for obj in obstacle_list:
        cs1lib.set_fill_color(0,0,1)
        obj.draw_obj()

    for obj in obstacle_list:
        if (Ra.object_collision(obj)):
            obstacle_collision = True

    #initial drawing of the arm. It pauses for a second before the animation begins
    if pause_start <=0:
        cs1lib.draw_line(0+normalize_x, 0+normalize_y, Ra.joints[0].x+normalize_x, normalize_y-Ra.joints[0].y)
        cs1lib.set_fill_color(1,0,1)
        for j in range(0, len(Ra.joints)):
            cs1lib.draw_circle(normalize_x+Ra.joints[j].x, normalize_y-Ra.joints[j].y, 5)
        for m in range(0, len(Ra.joints)-1):
            cs1lib.draw_line(Ra.joints[m].x+normalize_x, normalize_y-Ra.joints[m].y, normalize_x+Ra.joints[m+1].x, normalize_y-Ra.joints[m+1].y)
        last_joint = Ra.joints[len(Ra.joints)-1]
        cs1lib.draw_line(normalize_x+last_joint.x, normalize_y-last_joint.y, normalize_x+Ra.end_claw[0], normalize_y-Ra.end_claw[1])

    #This is the animation part of the drawing
    else:
        if pathway != None:
            if tuple(current_pos) == tuple(pathway[current_goal]):
                current_goal +=1
            if current_goal > len(pathway) - 1:
                current_goal = len(pathway) - 1

            current_goal_thetas = pathway[current_goal]

            if (1 - (pause_start/(num_frame * speed))) > 0:
                if collision_last_time and current_pos != pathway[current_goal]:
                    for current_num_loc in range(current_goal, len(pathway)):
                        goal_collision = pathway[current_num_loc]
                        if current_num_loc == len(pathway)-1:
                            if goal_collision[num_of_collision] < 0:
                                goal_collision[num_of_collision] += 2*math.pi
                            else:
                                goal_collision[num_of_collision] -= 2*math.pi
                        else:
                            if goal_collision[num_of_collision] <0:
                                goal_collision[num_of_collision] += math.pi
                            else:
                                goal_collision[num_of_collision] -= math.pi
                        pathway[current_num_loc] = goal_collision
                    print(pathway)

                tmp_setup = []
                for i in range(0, len(initial_thetas)):
                    new_theta = current_pos[i] * (1-(pause_start/(num_frame * speed))) + current_goal[i] * (pause_start/(num_frame * speed))
                    tmp_setup.append(new_theta)

                if collision_last_time and current_pos != pathway[current_goal]:
                    collision_last_time = False
                    if not last_time_positive:
                        tmp_setup[num_of_collision] += 0.5 * math.pi
                    else:
                        tmp_setup[num_of_collision] -= 0.5 * math.pi

                if pathway[current_goal][0] - 0.05 <= tmp_setup[0] <= pathway[current_goal][0] + 0.05:
                    if pathway[current_goal][1] - 0.05 <= tmp_setup[1] <= pathway[current_goal][1]+0.05:
                        current_pos = pathway[current_goal]
                        pause_start = 1

                kin = Kinematics(tmp_setup, initial_lengths)


            else:
                kin = Kinematics(final_thetas, initial_lengths)

        else:
            if pause_start == num_frame:
                print("No path found with current number of vertices generated")
            #Alters the theta frame by frame so that the diagonal movement of the joints happen at very small increments
            #such that it appears to move in an arc pattern
            if (1-(pause_start/(num_frame*speed))) > 0:
                tmp_thetas = []
                for i in range(0, len(initial_thetas)):
                    new_theta = initial_thetas[i] * (1-(pause_start/(num_frame*speed))) + final_thetas[i] * (pause_start/(num_frame*speed))
                    tmp_thetas.append(new_theta)
                kin = Kinematics(tmp_thetas, initial_lengths)
            else:
                kin = Kinematics(final_thetas, initial_lengths)

            #updates the current joints thetas and (x,y) values
            for i in range(0, len(Ra.joints)):
                Ra.joints[i].theta = kin.thetas[i]
            for j in range(1, len(Ra.joints)):
                xy = kin.calc_xy(j, Ra.joints)
                Ra.joints[j].x = xy[0]
                Ra.joints[j].y = xy[1]
            Ra.end_claw = kin.calc_xy(j+1, Ra.joints)

        #Draws the robot arm in its entirety
        cs1lib.draw_line(0 + normalize_x, 0 + normalize_y, Ra.joints[0].x + normalize_x, normalize_y - Ra.joints[0].y)
        cs1lib.set_fill_color(1, 0, 1)
        for j in range(0, len(Ra.joints)):
            cs1lib.draw_circle(normalize_x + Ra.joints[j].x, normalize_y - Ra.joints[j].y, 5)
        for m in range(0, len(Ra.joints) - 1):
            cs1lib.draw_line(Ra.joints[m].x + normalize_x, normalize_y - Ra.joints[m].y,normalize_x + Ra.joints[m + 1].x, normalize_y - Ra.joints[m + 1].y)
        last_joint = Ra.joints[len(Ra.joints) - 1]
        cs1lib.draw_line(normalize_x + last_joint.x, normalize_y - last_joint.y, normalize_x + Ra.end_claw[0], normalize_y - Ra.end_claw[1])

        for num in range(0, len(initial_thetas)):
            if not obstacle_collision:
                for obstacle in obstacle_list:
                    if Ra.object_collision(obstacle):
                        if collisions < max_collisions and not collision_last_time:
                            collisions += 1
                            collision_last_time = True
                            num_of_collision = num
                        elif not collision_last_time:
                            obstacle_collision = True
                        break


    if obstacle_collision and (1 - (pause_start/num_frame * speed)) < 0:
        #if pause_start % 40 <= 20:
            cs1lib.set_fill_color(1, 0, 0, 0.5)
            cs1lib.draw_rectangle(0, 0, 600, 600)




normalize_x = 300
normalize_y = 600

initial_thetas = [1.5, 1, 2, 0]
initial_lengths = [50, 50, 50, 50]

final_thetas = [1, -1, 1, 1]

num_frame = 60
speed = 5
pause_start = -60

obstacle_collision = False
collisions = 0
max_collisions = 10
collision_last_time = False
num_of_collision = 0
last_time_positive = False

random.seed(3)
num_obstacles = random.randint(1, 4)
obstacle_list = []



for i in range(0, num_obstacles):
    rand_x = random.randint(-200, 200)
    rand_y = random.randint(0, 150)
    rand_r = random.randint(5, 10)

    new_obstacle = Object(rand_x, rand_y, rand_r)

    obstacle_list.append(new_obstacle)

Ra = Robot_arm(initial_thetas, initial_lengths)
Ra.add_joints()

prm = PRM(initial_thetas, final_thetas, obstacle_list, Ra, initial_lengths)
pathway = prm.get_path(500)
print(pathway)

current_goal = 1
current_pos = initial_thetas


cs1lib.start_graphics(graphics, framerate=60, width=600, height=600)