
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

