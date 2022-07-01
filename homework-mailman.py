from sys import float_info
from math import dist
from itertools import permutations
from typing import List, Tuple
from dataclasses import dataclass

start = (0,2)
points = [
    (2,5),
    (5,2),
    (6,6),
    (8,3),
    ]

possible_paths = list( permutations(points) )

print(f"Permutations count: {len(possible_paths)}")

Point = tuple[ int, int ]

@dataclass
class Segment:
    start_point : Point
    end_point : Point
    distance: float

class Path:
    def __init__(self):
        self.segments = list()
        self.total_distance = 0

    def __repr__(self):
        start_point = self.segments[0].start_point
        distance = 0
        steps = "".join([f" -> {s.end_point}[{s.distance}]" for s in self.segments ])
        return f'{start_point}{steps} = {self.total_distance}'

results : List[Path] = list()

for path in possible_paths:
    current_point = start
    result_path : Path = Path()

    for next_point in points:
        distance = dist(current_point, next_point)
        result_path.segments.append(Segment(current_point, next_point, distance))
        result_path.total_distance += distance
        current_point = next_point

    results.append(result_path)

min_distance = float_info.max
min_index = -1

for index , res in enumerate( results ):
    if res.total_distance < min_distance:
        min_index = index

shortest_path = results[min_index]

print(shortest_path)
