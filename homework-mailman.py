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

    def append(self, point : Point, distance : float):
        self.points.append(point)

        if self.distances:
            distance += self.distances[-1]

        self.distances.append(distance)

    def get_total_distance(self):
        return self.distances[-1] if self.distances else 0

    def __repr__(self):
        steps = "".join([f" -> {self.points[i]}[{self.distances[i]}]" for i in range(len( self.points )) ])
        return f'{self.starting_point}{steps} = {self.get_total_distance()}'

paths = list()

for perm in points_permutations:
    current_point = start
    path : Path = Path(start)

    for next_point in perm:
        distance = dist(current_point, next_point)
        path.append(next_point, distance)
        current_point = next_point

    paths.append(path)

shortest_distance = float_info.max
shortest_index = -1

    if res.get_total_distance() < min_distance:
        min_index = index
for index , path in enumerate( paths ):

shortest_path = paths[shortest_index]

print(shortest_path)
