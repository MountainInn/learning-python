import re
import math
import itertools

# Задача 1


def domain_name(url):
    return re.sub(r"https?|://|www\.|\..+", "", url)


assert domain_name("http://google.com") == "google"
assert domain_name("http://google.co.jp") == "google"
assert domain_name("www.xakep.ru") == "xakep"
assert domain_name("https://youtube.com") == "youtube"


#  Задача 2


def int32_to_ip(int32):
    binary: str = bin(int32).removeprefix("0b").ljust(32, '0')
    numbers: list[str] = []

    for i in range(0, 32, 8):
        octet: str = binary[i:i+8]
        number: int = int(octet , 2)
        numbers.append(str( number ))

    ip: str = ".".join(numbers)

    return ip


assert int32_to_ip(2154959208) == "128.114.17.104"
assert int32_to_ip(0) == "0.0.0.0"
assert int32_to_ip(2149583361) == "128.32.10.1"



#  Задача 3


def zeroes(n):
    if n == 0:
        return 0

    k_range: range = range(1, math.floor( math.log(n, 5) ) + 1)

    zero_count: int = sum([math.floor(n / math.pow(5, k)) for k in k_range])

    return zero_count

assert zeroes(0) == 0
assert zeroes(6) == 1
assert zeroes(30) == 7


# Задача 4


def bananas(s) -> set:

    def indices(elem, l) -> list[int]:
        return [index for index, item in enumerate(l) if item == elem]


    comb_b: list[int] = list(itertools.combinations(indices('b', s), 1))
    comb_a: list[int] = list(itertools.combinations(indices('a', s), 3))
    comb_n: list[int] = list(itertools.combinations(indices('n', s), 2))

    comb_chars: list = list(itertools.product(comb_b, comb_a, comb_n))

    result = set()

    for (bs, aas, ns) in comb_chars:
        word = list(itertools.repeat('-', len(s)))

        for b in bs:
            word[b] = 'b'

        for a in aas:
            word[a] = 'a'

        for n in ns:
            word[n] = 'n'

        word_str: str = ''.join(word)
        check_word: str = word_str.replace('-', '')

        if check_word == "banana":
            result.add(word_str)

    return result


assert bananas("banann") == set()
assert bananas("banana") == {"banana"}
assert bananas("bbananana") == {"b-an--ana", "-banana--", "-b--anana", "b-a--nana", "-banan--a",
                     "b-ana--na", "b---anana", "-bana--na", "-ba--nana", "b-anan--a",
                     "-ban--ana", "b-anana--"}
assert bananas("bananaaa") == {"banan-a-", "banana--", "banan--a"}
assert bananas("bananana") == {"ban--ana", "ba--nana", "bana--na", "b--anana", "banana--", "banan--a"}



# Задача 5


def count_find_num(primesL, limit):

    def contains_all(elems, iterable):
        result: bool = True

        for e in elems:
            contains: bool = False

            for i in iterable:
                contains = i == e
                if contains:
                    break

            result = result and contains

        return result


    def product(iterable):
        result: int = 1
        for i in iterable:
            result *= i

        return result
    

    results: list[(int, int)] = list()
    comb_length: int = len(primesL)

    while True:

        combs: list[int]
        combs = list(itertools.combinations_with_replacement(primesL, comb_length))
        combs = filter(lambda l : contains_all(primesL, l), combs)

        products: list[int] = map(lambda x : product(x), combs)

        all_greater_than_limit: bool = True

        for p in products:
            if p <= limit:
                results.append(p)
                all_greater_than_limit = False

        if all_greater_than_limit:
            if results:
                return [len(results), max(results)]
            else:
                return []
        else:
            comb_length += 1

    return []


primesL = [2, 3]
limit = 200
assert count_find_num(primesL, limit) == [13, 192]

primesL = [2, 5]
limit = 200
assert count_find_num(primesL, limit) == [8, 200]

primesL = [2, 3, 5]
limit = 500
assert count_find_num(primesL, limit) == [12, 480]

primesL = [2, 3, 5]
limit = 1000
assert count_find_num(primesL, limit) == [19, 960]

primesL = [2, 3, 47]
limit = 200
assert count_find_num(primesL, limit) == []
