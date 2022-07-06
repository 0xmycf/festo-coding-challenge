#! /usr/bin/env python3.10

import traceback

from dotenv import load_dotenv
from src.common import Solution, getos
load_dotenv()

# load all scripts
from src import *

INSTANCE = Solution()

for key, val in INSTANCE.ans_dic.items():
    pure_key = key.split(':')[0]
    if 'provide_args' in key or 'provide_kwargs' in key:
        continue
    try:
        print('')
        print(f'{key}:')
        if key[-1] != '4':
            print(val(getos(key.replace(':','')), *INSTANCE.ans_dic[f'provide_args{pure_key}'](), **INSTANCE.ans_dic[f'provide_kwargs{pure_key}']()))
        else:
            print(val(*INSTANCE.ans_dic[f'provide_args{pure_key}']()))

    except NotImplementedError:
        print(f'{key} not implemented yet')
        continue

    except Exception as e:
        print(e.__class__.__name__)
        traceback.print_exc()
        print(f"Error in {key} with pure_key {pure_key}")
        continue
