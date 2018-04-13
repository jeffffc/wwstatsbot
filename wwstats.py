#!/usr/bin/python3
# -*- coding: utf-8 -*

import requests
from achvlist import ACHV

achv_names = [y['name'] for y in ACHV]
total = len(ACHV)


def check(userid):
    url = "http://tgwerewolf.com/stats/PlayerAchievements/?pid={}&json=true".format(userid)
    stats = requests.get(url).json()
    attained_count = len(stats)
    attained_names = [each['name'] for each in stats]

    msg = "*ATTAINED ({0}/{1}):*\n".format(attained_count, total)

    for each in stats:
        if each['name'] in achv_names:
            msg += "- `{}`\n".format(each['name'])

    msg2 = "\n*MISSING ({0}/{1}):*\n".format(total - attained_count, total)
    msg2 += "*--> ATTAINABLE VIA PLAYING:*\n"
    for z in ACHV:
        if z['name'] not in attained_names:
            if "inactive" in z or "not_via_playing" in z:
                continue
            msg2 += " -`{}`\n".format(z['name'])
            msg2 += ">>> _{}_\n".format(z['desc'])
    msg2 += "\n--> *NOT DIRECTLY ATTAINABLE VIA PLAYING:*\n"
    for z in ACHV:
        if z['name'] not in attained_names:
            if "not_via_playing" in z:
                msg2 += " -`{}`\n".format(z['name'])
                msg2 += ">>> _{}_\n".format(z['desc'])
            else:
                continue
    msg2 += "\n--> *INACTIVE: *\n"
    for z in ACHV:
        if z['name'] not in attained_names:
            if "inactive" in z:
                msg2 += " -`{}`\n".format(z['name'])
                msg2 += ">>> _{}_\n".format(z['desc'])
            else:
                continue

    return msg, msg2
