import itertools

# Задача 3.1

cache : dict = dict()

def caching_decorator(func):
    '''Декоратор для кэширования результата функции.'''

    def wrapper(*args, **kwargs):
        key = tuple( [a for a in args] + [b for (kw , b) in kwargs] )

        result = cache.get(key)

        if result:
            print(f"Результат, взятый из кэша: {result}")
            return result

        result = func(*args, **kwargs)
        cache[key] = result

        print(f"Новый результат: {result}")
        return result

    return wrapper

@caching_decorator
def multiplier(number: int):
    '''Умножает заданное число на 2.'''
    return number * 2

def main():
    multiplier(2)
    multiplier(3)

    multiplier(2)
    multiplier(3)

if __name__ == "__main__":
    main()
