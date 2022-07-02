from sys import float_info
from math import dist
from itertools import permutations


class Path:
    def __init__(self, starting_point, other_points):
        self.points = list()
        self.distances = list()
        self.starting_point = starting_point

        current_point = starting_point

        for next_point in other_points:
            distance = dist(current_point, next_point) + \
                self.get_total_distance()

            self.distances.append(distance)
            self.points.append(next_point)

            current_point = next_point

    def __repr__(self):
        points_range = range(len(self.points))
        steps = [
            f' -> {self.points[i]}[{self.distances[i]}]' for i in points_range]
        steps_string = "".join(steps)
        return f'{self.starting_point}{steps_string} = {self.get_total_distance()}'

    def get_total_distance(self):
        return self.distances[-1] if self.distances else 0


start = (0, 2)
points = [
    (2, 5),
    (5, 2),
    (6, 6),
    (8, 3),
]
points_permutations = list(permutations(points))
paths = list()

for points_perm in points_permutations:
    path: Path = Path(start, points_perm)
    paths.append(path)

shortest_path = min(
    enumerate(paths), key=lambda pair: pair[1].get_total_distance())[1]

print(shortest_path)
