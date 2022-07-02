from sys import float_info
from math import dist
from itertools import permutations

start = (0,2)
points = [
    (2,5),
    (5,2),
    (6,6),
    (8,3),
    ]

points_permutations = list( permutations(points) )

class Path:
    def __init__(self, starting_point):
        self.starting_point = starting_point
        self.points = list()
        self.distances = list()


    def append(self, point : tuple[ int, int ], distance : float):
        distance += self.get_total_distance()
        self.distances.append(distance)
        self.points.append(point)

    def get_total_distance(self):
        return self.distances[-1] if self.distances else 0


paths = list()

for perm in points_permutations:
    current_point = start
    path : Path = Path(start)
    def __repr__(self):
        points_range = range(len( self.points ))
        steps = [f' -> {self.points[i]}[{self.distances[i]}]' for i in points_range]
        steps_string = "".join(steps)
        return f'{self.starting_point}{steps_string} = {self.get_total_distance()}'

    for next_point in perm:
        distance = dist(current_point, next_point)
        path.append(next_point, distance)
        current_point = next_point

    paths.append(path)



shortest_path = min(enumerate(paths), key=lambda pair: pair[1].get_total_distance())[1]

print(shortest_path)
