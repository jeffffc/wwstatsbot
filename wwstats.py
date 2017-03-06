#!/usr/bin/python3
# -*- coding: utf-8 -*

from bs4 import BeautifulSoup
from bs4 import UnicodeDammit
import requests
import urllib.request
import urllib.parse
import codecs
from achvlist import *

def check(id):
    url = "http://tgwerewolf.com/stats/PlayerAchievements/?pid=" + str(id)
    stats = {}
    #url = urllib.parse.quote(url)
#    r = requests.get(url)
#    soup = BeautifulSoup(r.content)
#    soup = str(r.content)
#    output = soup.prettify("utf-8")
#    output = soup.encode("utf-8")
#    output = UnicodeDammit(soup)
#    output = codecs.decode(soup, 'unicode_escape').encode('latin1').decode('utf8')
#    print(output)
    r = requests.get(url)

    dump = BeautifulSoup(r.json(), 'html.parser')
    db = dump('td')
    num = 0
    for i in range(0, len(db), 2):
        stats[num] = db[i].string
        num = num + 1

    msg = "ATTAINED ({0}/{1}):\n".format(str(len(stats)), str(len(ACHV)))

    for x in stats:
        if stats[x] in [y['name'] for y in ACHV]:
            msg += "- `" + stats[x] + "`\n"


    msg2 = "\nMISSING ({0}/{1}):\n".format(str(len(ACHV)-len(stats)), str(len(ACHV)))
    msg2 += "--> ATTAINABLE VIA PLAYING:\n"
    for z in ACHV:
        if z['name'] not in stats.values():
            if "inactive" in z or "not_via_playing" in z:
                continue
            msg2 += "- `" + z['name'] + "`\n"
            msg2 += ">>> _" + z['desc'] + "_\n"
    msg2 += "\n--> NOT ATTAINABLE VIA PLAYING:\n"
    for z in ACHV:
        if z['name'] not in stats.values():
            if "not_via_playing" in z:
                msg2 += "- `" + z['name'] + "`\n"
            else:
                continue
    msg2 += "\n--> INACTIVE:\n"
    for z in ACHV:
        if z['name'] not in stats.values():
            if "inactive" in z:
                msg2 += "- `" + z['name'] + "`\n"
            else:
                continue

    return msg, msg2
