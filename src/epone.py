#! /usr/bin/env python3.10

import re

from typing import Union
from functools import cache

from src.common import Solution, Solver, returnIfNonef, lmap

I = Solution()

@I.solution("EPONE")
class EpisodeOne(Solver):

    __NAME   = 'Name'
    __ID     = 'ID'
    __HOME   = 'Home Planet'
    __SAMPLE = 'Sample'

    @staticmethod
    def part1(envarg, entry_list, *args, fn=None, **kwargs):
        pico = "pico"
        mat_list = list(map(lambda x: (x[EpisodeOne.__ID], x[EpisodeOne.__SAMPLE]), entry_list))

        def check_for_pico(*val):
            id_ = val[0]
            mat = val[1]
            tmat = EpisodeOne.__transpose(mat, lambda x: ''.join(x))
            for row in mat:
                if pico in row or pico[::-1] in row:
                    return True
            for col in tmat:
                if pico in col or pico[::-1] in col:
                    return True
            return False

        ans = [int(x[0]) for x in filter(lambda x: check_for_pico(*x), mat_list)]
        return returnIfNonef(ans, fn)

    @staticmethod
    def part2(*args, **kwargs): ...

    @staticmethod
    def part3(*args, **kwargs): ...

    @staticmethod
    def part4(*args, **kwargs): ...

    @staticmethod
    def provide_args(*args, **kwargs):
        with open("res/population.txt") as f:
            # return it as nested list, because the main function spreads the arguments
            return [EpisodeOne.__parse_population(f.read())]

    @cache
    @staticmethod
    def provide_kwargs(*args, **kwargs):
        return {
                "fn": sum,
               }

    @cache
    @staticmethod
    def __parse_population(pop_str: str):
        files = pop_str.split("\n\n")

        ans: list[dict[str, Union[str, list[str]]]] = []

        tmp = lmap(lambda x: x.splitlines(), files)
        for file_ in tmp:
            file = list(filter(lambda x: x != '', file_))
            tmp, mat = {}, []
            first_three = file[:3]
            sample = file[3:]
            
            for line in sample:
                if not bool(re.search(r"B|\+", line)):
                    mat.append(line.strip().replace("|", ""))

            if mat == []:
                continue

            tmp.update({
                'Sample': mat,
                })

            tmp.update({
                key.strip(): val.strip() for key, val in map(lambda s: s.split(':'), first_three)
                })
            ans.append(tmp)

        return ans

    @staticmethod
    def __transpose(matrix, f=None):
        """
        Transposes a matrix, applying a function to each row
        [[1,2,3], [4,5,6]] -> [[1,4], [2,5], [3,6]]
        or
        ['abc', 'def'] -> [['a', 'd'], ['b', 'e'], ['c', 'f']]
        """
        ret = list(map(list, zip(*matrix)))
        if f is None:
            return ret
        else:
            return list(map(f, ret))
