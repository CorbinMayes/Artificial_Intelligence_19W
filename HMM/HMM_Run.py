"""
Corbin Mayes - 2/18/19
Discussed with Hunter Gallant
"""

from HMM import HMM


"""
Test maze without walls
"""
hmm = HMM()
print("no_walls_maze")
hmm.read_maze("no_walls_maze.maz")
hmm.generate_initial_model()
hmm.generate_transition_model()
hmm.generate_sensor_model()
print(hmm.generate_sensed())
print(hmm.get_prob_distribution())


"""
Test maze with walls
"""
print("-----------")
print("test_maze")
hmm.read_maze("test_maze.maz")
hmm.generate_initial_model()
hmm.generate_transition_model()
hmm.generate_sensor_model()
print(hmm.generate_sensed())
print(hmm.get_prob_distribution())


"""
2nd Test maze with walls
"""
print("----------")
print("test_maze2")
hmm.read_maze("test_maze.maz")
hmm.generate_initial_model()
hmm.generate_transition_model()
hmm.generate_sensor_model()
print(hmm.generate_sensed())
print(hmm.get_prob_distribution())