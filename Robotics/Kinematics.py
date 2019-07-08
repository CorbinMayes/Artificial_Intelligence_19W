import math

class Kinematics:
    def __init__(self, thetas, lengths):
        self.thetas = thetas
        self.lengths = lengths

    def calc_xy(self, num, joints):
        x = self.lengths[num-1] * math.cos(self.sum_thetas(0, num-1))
        y = self.lengths[num-1] * math.sin(self.sum_thetas(0, num-1))

        x+= joints[num-1].x
        y+= joints[num-1].y

        return (x,y)

    def sum_thetas(self, start, end):
        sum = 0
        for i in range(start, end+1):
            sum += self.thetas[i]
        return sum

