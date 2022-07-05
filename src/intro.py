#! /usr/bin/env python3.10

import sys, os
import csv

from functools import reduce
from dotenv    import load_dotenv
load_dotenv()

def puzzle1(magic_num: str, reader) -> list[int]:
    """
    Puzzle 1
    """
    return list(map(lambda e: int(e[1]), filter(lambda entry: magic_num in entry[1], reader)))

def puzzle2(module: str, reader) -> list[int]:
    """
    Puzzle 2
    """
    fmod = 0b10000000 >> (int(module) - 1)
    return list(map(lambda e: int(e[1]), filter(lambda row: (int(row[2], 10)) & fmod == fmod, reader)))

def puzzle3(time: str, reader) -> list:
    """
    Puzzle 3
    """
    time = time.replace(':', '')
    def lam(row):
        frow = row[3].replace(':', '')
        return frow != '9999' and int(frow) < int(time)

    return list(map(lambda e: int(e[1]), filter(lam, reader)))

def get(key: str) -> str:
    """
    Get the value of a key from the environment
    """
    return os.environ.get(key, default="")

puzzles_list = [
        (get('INTROP1'), puzzle1),
        (get('INTROP2'), puzzle2),
        (get('INTROP3'), puzzle3)
        ]

def find_username(reader):
    """
    Find the username of the mug thief
    """
    ids = list(map(lambda t: t[1](t[0], reader), puzzles_list))
    id_ = list(reduce(lambda acc, val: set(acc) & set(val), ids))[0]
    return [x[0] for x in reader if int(x[1]) == id_][0]

if __name__ == '__main__':

    if len(sys.argv) == 1:
        print('Usage: python3 intro.py [filename]')
        sys.exit(1)

    filename = sys.argv[1]

    with open(filename, 'r') as f:
        reader = csv.reader(f)
        reader = list(reader)
        print(
            sum(puzzle1(get('INTROP1'), reader)),
            sum(puzzle2(get('INTROP1'), reader)),
            sum(puzzle3(get('INTROP1'), reader)),
            find_username(reader)
        )
           
