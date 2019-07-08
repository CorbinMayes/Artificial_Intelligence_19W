"""
Corbin Mayes - 1/31/19
Discussed with Hunter Gallant
"""

from CS1SectionCSP import CS1SectionCSP

sections = ['Monday 5:00', 'Monday 7:00', 'Tuesday 4:00', 'Wednesday 5:30', 'Thursday 5:00', 'Friday 3:00']
section_leaders = [['Sam', sections[0], sections[1], sections[2]], ['Jason', sections[3], sections[4], sections[5]]]
students = [['Billy', sections[0], sections[3]], ['Bob', sections[0], sections[4]], ['Joe', sections[1], sections[4]], ['Anne', sections[1], sections[4]], ['Louise', sections[2], sections[4]]]

#sections = ['Monday 5:00', 'Monday 6:00', 'Monday 7:00']
#section_leaders = [['Sam', sections[0], sections[1]] , ['Jason', sections[2]]]
#students = [['Billy', sections[0], sections[1]], ['Bob',  sections[2]], ['Joe', sections[0], sections[2]], ['Louise', sections[2]]]

CS1SectionAssignment = CS1SectionCSP(section_leaders, students, sections)
print(CS1SectionAssignment.solve())
