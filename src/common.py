#! /usr/bin/env python3.10


from abc        import ABC, abstractmethod
from dotenv     import load_dotenv
from typing     import Callable, TypeVar

import os
import re


# TypeVars for common function definitions
T = TypeVar('T')
S = TypeVar('S')


def getos(key: str) -> str:
    """
    Get the value of a key from the environment
    """
    if not os.environ.get('LOADED') == 'True':
        load_dotenv()

    return os.environ.get(key, default="")

class Solution:

    # https://stackoverflow.com/questions/31875/is-there-a-simple-elegant-way-to-define-singletons
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls, *args, **kwargs)
            cls.__lst = {}
        return cls._instance

    @property
    def ans_dic(self) -> dict[str, Callable]:
        """
        holds all arguments as keys to functions for the solutions
        """
        return self.__lst

    def solution(self, key: str):
        """
        Adds the function to the lst dictionary with the $(key)P[1-3] as the key
        raises ValueError if the key is not of type "[A-Z]+[1-3]"
        raises TypeError if the function is not static
        """
        # This makes sure I don't enter a wrong key by accident
        if not bool(re.match('[A-Z]+[1-9]{0,1}', key)):
            raise ValueError('Key must be of type "[A-Z]+[1-3]"')

        def decorator(cls):
            class_dict = cls.__dict__

            # 1..=4 where 1-3 are the parts of the puzzle
            # and part 4 is the solution to the episode
            for i in range(1,5):
                func = class_dict[f'part{i}']
                if not isinstance(func, staticmethod):
                    raise TypeError(
                        f"\tFunctions part1-3 must be static\n\t\tClass {cls.__name__}"
                        )

                self.__lst.update({f'{key}:{i}': func})
            self.__lst.update({f'provide_args{key}': class_dict['provide_args']})
            self.__lst.update({f'provide_kwargs{key}': class_dict['provide_kwargs']})
            return cls
        return decorator

class Solver(ABC):
    """
    This is the solution base class
    This ensures all solutions implement all necessary functions
    """

    @staticmethod
    @abstractmethod
    def part1(*args, **kwargs): raise NotImplementedError

    @staticmethod
    @abstractmethod
    def part2(*args, **kwargs): raise NotImplementedError

    @staticmethod
    @abstractmethod
    def part3(*args, **kwargs): raise NotImplementedError

    @staticmethod
    @abstractmethod
    def part4(*args, **kwargs): raise NotImplementedError

    @staticmethod
    @abstractmethod
    def provide_args(*args, **kwargs): raise NotImplementedError

    @staticmethod
    @abstractmethod
    def provide_kwargs(*args, **kwargs): raise NotImplementedError

def returnIfNonef(x: T, f: Callable[[T], S] | None) -> T | S:
    """
    Checks if the provided function f is None and returns x if so
    Otherwise it returns f(x)
    """
    if f is None:
        return x
    return f(x)
