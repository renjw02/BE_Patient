#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# here put the import lib

def pg_params_check(content):
    '''
    fpg_morning
    fpg_noon
    fpg_evening
    p2hpg_morning
    p2hpg_noon
    p2hpg_evening
    '''    

    if 'fpg_morning' in content:
        content['fpg_morning'] = round(content['fpg_morning'], 1)
    else:
        content['fpg_morning'] = 0

    if 'fpg_noon' in content:
        content['fpg_noon'] = round(content['fpg_noon'], 1)
    else:
        content['fpg_noon'] = 0

    if 'fpg_evening' in content:
        content['fpg_evening'] = round(content['fpg_evening'], 1)
    else:
        content['fpg_evening'] = 0

    if 'p2hpg_morning' in content:
        content['p2hpg_morning'] = round(content['p2hpg_morning'], 1)
    else:
        content['p2hpg_morning'] = 0

    if 'p2hpg_noon' in content:
        content['p2hpg_noon'] = round(content['p2hpg_noon'], 1)
    else:
        content['p2hpg_noon'] = 0

    if 'p2hpg_evening' in content:
        content['p2hpg_evening'] = round(content['p2hpg_evening'], 1)
    else:
        content['p2hpg_evening'] = 0

    # # date
    # if 'pg_date' in content:
    #     pass
    # else:
    #     return "pg_date", False

    return "ok", True