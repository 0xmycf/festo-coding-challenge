#! /usr/bin/env python3.10

import re

from typing import Callable, Literal, Union
from functools import cache

from src.common import Solution, Solver, retOrFunction, lmap
from src.linear import Coord

I = Solution()

FileDict = list[dict[str, list[str] | str]]

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
        return retOrFunction(ans, fn)

    @staticmethod
    def part2(osvar, *args, **kwargs):
        ...

    @staticmethod
    def part3(_os, files, _p2, logs: dict[str, list[dict]], way, *args, fn=None, debug=False, **kwargs):
        """
        each log in logs has keys:
        - place: The place where the log was written.
        - log: dicts with time and the people who went in or out
        """
        summary = {}
        for place, log in logs.items():
            # entry: {'time': '0000', 'in': [list of names]}
            # people: { name -> { time_in -> [times], time_out -> [times] } }
            people = {}
            for entry in log:
                time = entry['time']
                # people can enter the same place twice
                for person in entry.get('in', []):
                    people[person] = people.get(person, {})
                    people[person]['time_in'] = people.get(person, {}).get('time_in', []) + [time]
                # some people might not went outside again
                # (I checked and everyone actually went out)
                for person in entry.get('out', []):
                    if person not in people:
                        continue
                    people[person]['time_out'] = people.get(person, {}).get('time_out', []) + [time]

            summary.update({place: people})

        # now we have a summary of all people who went in and out
        # now we can throw away all people who went into
        # one of the places which are not in the way
        additional_places = set(summary.keys()) - set(way)
        ids = set([])
        def go(x):
            bl = True
            for aplace in additional_places:
                bl = bl and not x in summary[aplace]
            return bl

        for place in set(way):
            ids |= set(filter(go, summary[place].keys()))

        # now we need to check that the people went through the way in the correct order
        # we can do this by checking the time they went in and out
        for wone, wtwo in zip(way, way[1:]):
            for name in list(ids)[:]:
                if name not in summary[wone] or name not in summary[wtwo]:
                    ids.remove(name)
                    continue
                # example of one summary[wone][name] entry:
                # Jingjing Omer
                # {'time_in': ['0751'], 'time_out': ['0824']}
                # {'time_in': ['0951', '1107'], 'time_out': ['1008', '1143']}

                # check if wone or wtwo is 'Pod Racing Track'
                # if so, then check if they went exactly twice
                if wone == 'Pod Racing Track' or wtwo == 'Pod Racing Track':
                    # explicit handling if both of the places are 'Pod Racing Track'
                    if wone == 'Pod Racing Track' and wtwo == 'Pod Racing Track':
                        if len(summary[wone][name]['time_in']) != 2 or len(summary[wtwo][name]['time_in']) != 2:
                            ids.remove(name)
                            continue
                        # this should be fine, since it doesnt matter when they went in or out
                        continue
                    else:
                        # check if the time in which the person went into wone is lower than the time in which they went into wtwo
                        summary[wone][name]['time_in'].sort()
                        summary[wtwo][name]['time_in'].sort()
                        if summary[wone][name]['time_in'][0] > summary[wtwo][name]['time_in'][0]:
                            ids.remove(name)
                            continue

                # otherwise their time_in and time_out arrays should be of length 1
                else:
                    if len(summary[wone][name]['time_in']) != 1 or len(summary[wtwo][name]['time_in']) != 1:
                        ids.remove(name)
                        continue

                    for time_in_1 in summary[wone][name]['time_in']:
                        bl = True
                        for time_in_2 in summary[wtwo][name]['time_in']:
                            # I can use <= because if its the same time its the same place
                            bl = bl and time_in_1 <= time_in_2
                        if not bl:
                            ids.remove(name)
                            break

        ans = []
        for file in files:
            if EpisodeOne.__getName(file) in ids:
                ans += [EpisodeOne.__getId(file)]

        return retOrFunction(ans, fn)

    @staticmethod
    def part4(*args, **kwargs): ...

    @staticmethod
    def provide_args(*args, **kwargs):
        with open("res/population.txt", 'r') as f:
            popfile = f.read()
            # return it as nested list, because the main function spreads the arguments
        with open("res/galaxy_map.txt", 'r') as f:
            mapfile = f.read()
        with open("res/security_log.txt", 'r') as f:
            sec_log = f.read()
        with open("res/place_sequence.txt", 'r') as f:
            way = lmap(lambda x: x.strip(), f.readlines())
        return [EpisodeOne.__parse_population(popfile), EpisodeOne.__parse_galaxy(mapfile), EpisodeOne.__parse_log(sec_log), way]

    @cache
    @staticmethod
    def provide_kwargs(*args, **kwargs):
        return {
                "fn": sum,
               }

    @cache
    @staticmethod
    def __parse_population(pop_str: str) -> FileDict:
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

    @cache
    @staticmethod
    def __parse_galaxy(gal_str: str):
        """
        @param gal_str: should be the whole file.

        One line looks like that:
        Erida               : (  17,   39,   68)
        """
        splitted = gal_str.splitlines()
        ans = {}
        for line in splitted:
            first, second = line.split(':')
            ans.update({
                first.strip(): Coord.of_str(second.strip())
                })

        return ans

    @cache
    @staticmethod
    def __parse_log(log_file: str):
        """
        @param log_file: should be the whole file.
        """
        content = filter(lambda x: x!="", log_file.split("Place:"))
        ans = {}
        for con in content:
            splitted = lmap(lambda x: x.strip(), con.split("\n\n"))
            location = splitted.pop(0)
            outer = []
            for block in filter(lambda s: s!="", splitted):
                tmp   = {}
                blocs = block.splitlines()
                time  = blocs.pop(0).replace(":", "").strip()
                tmp.update({
                    'time': time
                    })
                for b in blocs:
                    first = b[0]
                    match first:
                        case 'i': one, two = ('in', lmap(lambda x: x.strip(), b.replace("in:", "").strip().split(",")))
                        case 'o': one, two = ('out', lmap(lambda x: x.strip(), b.replace("out:", "").strip().split(",")))
                        case _  : raise Exception("Unknown block type: " + b)
                    tmp.update({
                        one: two
                        })
                outer += [tmp]
            ans.update({
                location: outer
                })

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


    @staticmethod
    def __getId(file) -> int:
        return int(file[EpisodeOne.__ID])

    @staticmethod
    def __getName(file) -> str:
        return file[EpisodeOne.__NAME]

def __parse_place(line: str) -> dict[str, str]:
    return {
            'place': line.split(':')[1].strip(),
            }

def __parse_time(line: str) -> dict[str, str]:
    return {
            'time': "".join(line.split(':')),
            }

# parses
# in: list, of, names
# out: list, of, names
# to a dict to 'out'/'in' and the list of names
def __parse_in_or_out(line: str) -> dict[str, list[str]]:
    splitted = line.split(':')
    lst      = lmap(lambda s: s.strip(), splitted[1].strip().split(','))
    return {
            splitted[0].strip(): lst,
           }

# returns the parsed line as dict
def match_line(line: str):
    if line == "":
        return {}
    first = line[0]
    if bool(re.match(r'\d+', first)):
        return __parse_time(line)

    match first:
        case 'P'      : return __parse_place(line)
        case 'i' | 'o': return __parse_in_or_out(line)
