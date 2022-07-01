from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Generator, List, Tuple, Iterable

# Задача 1

class CyclicIterator:

    def __init__(self, iterable : Iterable):
        self.iterable = iterable
        self.iterator = iter(iterable)

    def __iter__(self):
        return self

    def __next__(self):
        while True:
            try:
                return next(self.iterator)
            except StopIteration:
                self.iterator = iter(self.iterable)


cyclic_iterator = CyclicIterator(range(3))
iteration_count = 0
break_after = 10

print("\n\nProblem 1")
print("Cyclic iterator")
print()

for i in cyclic_iterator:
    print(i)
    iteration_count += 1
    if iteration_count >= break_after:
        break

# Задача 2

@dataclass
class Movie:
    title: str
    dates: List[Tuple[datetime, datetime]]

    def schedule(self) -> Generator[datetime, None, None]:
        for date_range in self.dates:
            current_date : datetime = date_range[0]
            while current_date <= date_range[1]:
                yield current_date
                current_date += timedelta(days=1)
        return []


m = Movie('sw', [
  (datetime(2020, 1, 1), datetime(2020, 1, 7)),
  (datetime(2020, 1, 15), datetime(2020, 2, 7))
])


print("\n\nProblem 2")
print("Array expansion")
print()

for d in m.schedule():
    print(d)
