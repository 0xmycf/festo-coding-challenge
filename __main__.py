#! /usr/bin/env python3.10

import traceback
import sys

from dotenv import load_dotenv
from src.common import Solution, Unstoppable, getos
load_dotenv()

# load all scripts
from src import *

INSTANCE = Solution()

if len(sys.argv) > 1 and (sys.argv[1] == "d" or sys.argv[1] == "debug"):
    debug = True
else:
    debug = False

for key, val in INSTANCE.ans_dic.items():
    pure_key = key.split(':')[0]
    if 'provide_args' in key or 'provide_kwargs' in key:
        continue
    try:
        print('')
        print(f'{key}:')
        if key[-1] != '4':
            kwargs = {**INSTANCE.ans_dic[f'provide_kwargs{pure_key}'](), "debug": debug}
            print(val(getos(key.replace(':','')), *INSTANCE.ans_dic[f'provide_args{pure_key}'](), **kwargs))
        else:
            print(val(*INSTANCE.ans_dic[f'provide_args{pure_key}']()))

    except Unstoppable as e:
        raise BaseException(e)

    except NotImplementedError:
        print(f'{key} not implemented yet')
        continue

    except Exception as e:
        print(e.__class__.__name__)
        traceback.print_exc()
        print(f"Error in {key} with pure_key {pure_key}")
        continue
