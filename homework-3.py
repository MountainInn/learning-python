from abc import ABC, abstractmethod
import time
import redis

#
# Задача 3.1
#


class Cache(ABC):

    def set(self, key: str, val):
        ...

    def get(self, key: str):
        ...


class DictCache(Cache):

    def __init__(self):
        self.dict: dict = dict()

    def set(self, key: str, val):
        self.dict[key] = val

    def get(self, key: str):
        return self.dict.get(key)


class RedisCache(Cache):

    def __init__(self):
        self.redis: redis.Redis = redis.Redis(host='localhost', port='6379')

    def set(self, key: str, val):
        self.redis.set(key, val)

    def get(self, key: str):
        return self.redis.get(key)

    def flushdb(self):
        self.redis.flushdb()


def cache_result(cache: Cache):
    '''Декоратор для кэширования результата функции в словаре.'''

    def decorator(func):
        def wrapper(*args, **kwargs):
            arguments = [a for a in args] + [a for (kw, a) in kwargs]
            key = "".join([str(a) for a in arguments])

            result = cache.get(key)

            if result:
                print(f"Результат, взятый из кэша: {result}")
                return result

            result = func(*args, **kwargs)
            cache.set(key, result)

            print(f"Новый результат: {result}")
            return result

        return wrapper
    return decorator


dict_cache: DictCache = DictCache()
redis_cache: RedisCache = RedisCache()


def multiplier(number: int):
    '''Умножает заданное число на 2.'''
    return number * 2


@cache_result(dict_cache)
def multiplier_with_dict(number: int):
    return multiplier(number)


@cache_result(redis_cache)
def multiplier_with_redis(number: int):
    return multiplier(number)

#
# Задача 3.2
#


def repeat(call_count: int, start_sleep_time: float, factor: float, border_sleep_time: float):
    def decorator(func):

        def output(repeat_count: int, sleep_time: float, result: float):
            repeat_count_str: str = str(repeat_count+1).rjust(3, '-')
            sleep_time_str: str = str(sleep_time).rjust(3, '-')
            print(
                f'Запуск номер {repeat_count_str}. Ожидание {sleep_time_str} секунд. Результат декорируемой функции = {result}')

        def wrapper(*args, **kwargs):
            repeat_count: int = 0
            sleep_time: float = start_sleep_time

            while repeat_count < call_count:
                time.sleep(sleep_time)

                result = func(*args, **kwargs)
                output(repeat_count, sleep_time, result)

                sleep_time = min(sleep_time + start_sleep_time *
                                 2 ** factor, border_sleep_time)
                repeat_count += 1

        return wrapper

    return decorator


@repeat(call_count=6, start_sleep_time=1, factor=2, border_sleep_time=30)
def repeated_multiplier(number: int):
    return multiplier(number)


def main():
    redis_cache.flushdb()

    print("Кэширование в словарь:")
    multiplier_with_dict(2)
    multiplier_with_dict(3)

    multiplier_with_dict(2)
    multiplier_with_dict(3)

    multiplier_with_dict(9)
    multiplier_with_dict(9)

    print("\nКэширование в redis:")
    multiplier_with_redis(2)
    multiplier_with_redis(3)

    multiplier_with_redis(2)
    multiplier_with_redis(3)

    multiplier_with_redis(9)
    multiplier_with_redis(9)

    print("\nДекоратор repeat:")
    repeated_multiplier(8)


if __name__ == "__main__":
    main()
