Corbin Mayes - 3/10/19

#Robotics

##PRM for Robot Arm

To start off the project, I wanted to be able to see and test the robot arm as it moved. So by using the CS1 lib, I built a graphics system to represent the arm and its locations. Once I had 
basic representation for the robot arm I moved on to the actual parts of the assignment. While doing this I built a joint class to store the x, y, and theta values as well as an arm class to 
store the joints as well as the end claw.

###Kinematics

>I created the kinematics class to be able to calculate the x and y values given the thetas of the joints as well as the lengths of the arms. It relies on the x and y values for the previous 
joints.

###Obstacles and Collision

>Next was obstacles and collisions with said obstacles caused by the movement of the arm. I began by creating an object class that would just draw a circle on the graphics to represent itself. 
Next I created the collision test function within the arm class because its just easier to have access to all the values for the joints. It tests the joints as well as the connections between 
them for any collision with the given object.

###PRM 

>The PRM builds the path by first building the roadmap. It builds the roadmap by adding the start and goal thetas and then adds their neighbors. It then begins adding random thetas assignments 
that aren't in the roadmap already and adding them and their neighbors to the roadmap. Once the roadmap is built, the get_path function uses a search function that is similar to a bfs to get a 
path to the goal using the roadmap. I built the helper functions to help both of the main functions. It follows the algorithm given by the planning algorithms website.

##RRT for a car

I followed the RRT algorithm from the same source as the PRM. Its helper functions are random configuration which randomly gets a state for the car to be in, nearest vertex which gets the nearest 
vertex to the current one, dist heur which just calculates the distance between two vertices, and new configuration which gets a new configuration from the current one. These allow the tree to be 
created using the provided algorithm