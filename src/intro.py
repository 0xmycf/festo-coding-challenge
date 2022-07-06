#! /usr/bin/env python3.10

import csv

from functools import reduce
from src.common import Solution, getos, Solver, returnIfNonef

INSTANCE = Solution()

@INSTANCE.solution("INTROP")
class Intro(Solver):
    @staticmethod
    def part1(magic_num: str, *reader, fn=None):
        """
        Puzzle 1
        """
        ans = list(map(lambda e: int(e[1]), filter(lambda entry: magic_num in entry[1], reader)))
        return returnIfNonef(ans, fn)

    @staticmethod
    def part2(module: str, *reader, fn=None):
        """
        Puzzle 2
        """
        fmod = 0b10000000 >> (int(module) - 1)
        ans =  list(map(lambda e: int(e[1]), filter(lambda row: (int(row[2], 10)) & fmod == fmod, reader)))
        return returnIfNonef(ans, fn)

    @staticmethod
    def part3(time: str, *reader, fn=None):
        """
        Puzzle 3
        """
        time = time.replace(':', '')
        def lam(row):
            frow = row[3].replace(':', '')
            return frow != '9999' and int(frow) < int(time)
        ans =  list(map(lambda e: int(e[1]), filter(lam, reader)))
        return returnIfNonef(ans, fn)

    @staticmethod
    def provide_args(*args, **kwargs):
        with open('./res/office_database.txt', 'r') as f:
            reader = csv.reader(f)
            reader = list(reader)
        return reader

    @staticmethod
    def provide_kwargs(*args, **kwargs):
        return { 'fn' : sum }

    @staticmethod
    def part4(*reader, **kwargs):
        """
        Find the username of the mug thief
        """
        lst = zip([getos(f'INTROP{i}') for i in range(1,4)], [ Intro.part1, Intro.part2, Intro.part3 ])
        ids = list(map(lambda t: t[1](t[0], *reader), lst))
        id_ = list(reduce(lambda acc, val: set(acc) & set(val), ids))[0]
        return [x[0] for x in reader if int(x[1]) == id_][0]
