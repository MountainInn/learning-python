from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Generator, List, Tuple, Iterable, Iterator

# Задача 1

class CyclicIterator:


    def __init__(self, iterable):
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
        return []


m = Movie('sw', [
  (datetime(2020, 1, 1), datetime(2020, 1, 7)),
  (datetime(2020, 1, 15), datetime(2020, 2, 7))
])

for d in m.schedule():
    print(d)
