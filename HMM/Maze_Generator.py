
"""
Corbin Mayes - 2/18/19
Discussed with Hunter Gallant
"""


import random

class Maze_Generator:
    def __init__(self, w = 1, h = 1):

        self.width = w
        self.height = h

        self.color_list = ["R", "B", "G", "Y", "#"]

        self.maze = ""

    def generate_maze(self):
        for i in range(self.height):
            for j in range(self.width):
                self.maze += random.choice(self.color_list)
            self.maze += "\n"
        return self.maze

    def maze_file(self, name = "test_maze"):
        filename = name + ".maz"
        f = open(filename, "w")
        f.write(self.maze)
        f.close()

    def __str__(self):
        return self.maze
if __name__ == "__main__":

    mg = Maze_Generator(4,4)

    print(mg.generate_maze())

    mg.maze_file("test_maze2")