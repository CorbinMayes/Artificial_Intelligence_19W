"""
Corbin Mayes - 2/18/19
Discussed with Hunter Gallant
"""

import random

class HMM:
    def __init__(self):
        self.maze = []
        self.maze_width = 0
        self.maze_height = 0
        self.maze_dict = {}
        self.colors = ["R", "G", "B", "Y"]
        self.initial_model = {}
        self.transition_model = {}
        self.sensor_model = {}
        self.sensors = []

    """
    Reads the maze file and converts it into a list and a dictionary
    """
    def read_maze(self, filename):
        #Get the file's lines
        f = open(filename, "r")
        lines = f.readlines()
        f.close()

        i = 0
        w = 0
        #transforms the lines into spaces then adds them to the list and their color to the dictionary
        #Position 0 is the top left corner of the maze and it goes horizontally from there
        for line in lines:
            w +=1
            for j in range(0, len(line)):
                if line[j] != '\n':
                    self.maze.append(i)
                    self.maze_dict[i] = line[j]
                    i+=1
        self.maze_width = w
        self.maze_height = int(len(self.maze)/w)

    """
    Finds the total distribution of colors and walls in the maze
    """
    def generate_initial_model(self):
        if self.maze != []:

            #Calculate the total number of spaces that aren't walls
            tot_maze_size = 0
            for i in self.maze_dict:
                if self.maze_dict[i] != "#":
                    tot_maze_size += 1

            #Calculates the probability of that space given the total number of available spaces
            for i in self.maze_dict:
                if self.maze_dict[i] != "#":
                    self.initial_model[i] = 1/tot_maze_size
                else:
                    self.initial_model[i] = 0

    """
    Creates the transitional model for each spot in the maze
    """
    def generate_transition_model(self):
        for i in self.maze:
            #Get the available spaces surrounding a space
            surround = self.get_spaces_next_to(i)
            for j in self.maze:

                #Calculates the probability of remaining in the same space based off of the length of surround
                if j == i:
                    if i in self.transition_model:
                        self.transition_model[i][j] = (4-len(surround))*0.25
                    else:
                        self.transition_model[i] = {j:(4-len(surround))*0.25}

                #Calculates the probability of moving to a available space around the current space
                elif j in surround:
                    if i in self.transition_model:
                        self.transition_model[i][j] = 0.25
                    else:
                        self.transition_model[i] = {j:0.25}

                #Sets all other spaces to probability of 0
                else:
                    if i in self.transition_model:
                        self.transition_model[i][j] = 0
                    else:
                        self.transition_model[i] = {j:0}

    """
    Finds where the robot can move to from a given space
    """
    def get_spaces_next_to(self, space):
        next_to = []
        #if the space to the left is in the maze and isn't a wall
        if space%self.maze_width != 0 and self.maze[space-1] != "#":
            next_to.append(self.maze[space-1])

        #if the space above is in the maze and isn't a wall
        if space - self.maze_width >=0 and self.maze[space-self.maze_width] != "#":
            next_to.append(self.maze[space-self.maze_width])

        #if the space to the right is in the maze and isn't a wall
        if space%self.maze_width != self.maze_width-1 and self.maze[space+1] != "#":
            next_to.append(self.maze[space+1])

        #if the space below is in the maze and isn't a wall
        if space + self.maze_width < len(self.maze) and self.maze[space+self.maze_width] != "#":
            next_to.append(self.maze[space+self.maze_width])

        return next_to

    """
    Creates the sensor model as the evidence model
    """
    def generate_sensor_model(self):
        #Goes through all the colors and then all the spaces
        for i in self.colors:
            for j in self.maze:
                if self.maze_dict[j] != "#":

                    #if the space is the same as the color than it has a probability of 0.88 otherwise it is 0.04
                    if i not in self.sensor_model:
                        if i == self.maze_dict[j]:
                            self.sensor_model[i] = {j:0.88}
                        else:
                            self.sensor_model[i] = {j:0.04}
                    else:
                        if i == self.maze_dict[j]:
                            self.sensor_model[i][j] = 0.88
                        else:
                            self.sensor_model[i][j] = 0.04

                #if the space is a wall then the probability is 0
                else:
                    if i not in self.sensor_model:
                        self.sensor_model[i] = {j:0}
                    else:
                        self.sensor_model[i][j] = 0


    """
    Generates a random path that the sensor sensed
    """
    def generate_sensed(self):
        randrange = random.randint(1,10)
        for i in range(0, randrange):
            self.sensors.append(random.choice(self.colors))
        return self.sensors

    """
    recursive function that runs the filtering
    """
    def timestep(self, trans_model = None, time = 1, prob_dist = {}):
        current_prob_dist = prob_dist
        if time > len(self.sensors):
            return current_prob_dist

        """
        Predict
        """
        #Multiply all the transition model by the previous model
        tmp_p_s = []
        for i in trans_model:
            tmp = []
            for j in self.transition_model[i]:
                tmp.append(trans_model[i] * self.transition_model[i][j])
            tmp_p_s.append(tmp)

        #Add the columns of all the lists of products
        p_s = {}
        for d in range(0, len(tmp_p_s)):
            sum = 0
            for e in tmp_p_s:
                sum += e[d]
            p_s[d] = sum


        """
        Update
        """
        #Multiply the predict step by the sensor model for the current spot
        p_sgivenc = {}
        curr_sense_model = self.sensor_model[self.sensors[time-1]]
        for n in range(0, len(p_s)):
            if n not in p_sgivenc:
                p_sgivenc[n] = curr_sense_model[n] * p_s[n]
            else:
                p_sgivenc[n] += curr_sense_model[n] * p_s[n]

        #Calculate Alpha and normalize
        sum = 0
        for k in p_sgivenc:
            sum += p_sgivenc[k]
        alpha = 1/sum
        for g in p_sgivenc:
            p_sgivenc[g] *= alpha

        #recursive call
        current_prob_dist[time] = p_sgivenc
        return self.timestep(p_sgivenc, time+1, current_prob_dist)

    """
    Filtering initializer
    """
    def forward_filtering(self):
        current_step_trans_model = self.initial_model
        return self.timestep(current_step_trans_model)

    """
    Transforms filtered result into a more understandable string
    """
    def get_prob_distribution(self):
        prob_dist = self.forward_filtering()
        result = ""
        num = 0
        for i in prob_dist:
            result += "Timestep "+str(i)+" color: "+ self.sensors[num]+"\n"
            for j in prob_dist[i]:
                result += "Position "+str(j)+": "+str(prob_dist[i][j]*100)+"%\n"
            num += 1

        return result


if __name__ == "__main__":
    hmm = HMM()
    hmm.read_maze("test_maze.maz")
    hmm.generate_initial_model()
    hmm.generate_transition_model()
    hmm.generate_sensor_model()
    print(hmm.generate_sensed())
    print(hmm.get_prob_distribution())
