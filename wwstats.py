import requests
from achvlist import ACHV

achv_names = [y['name'] for y in ACHV]
total = len(ACHV)


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


def check(userid):
    url = "http://tgwerewolf.com/stats/PlayerAchievements/?pid={}&json=true".format(userid)
    stats = requests.get(url).json()
    attained_count = len(stats)
    attained_names = [each['name'] for each in stats]
    not_via_playing = [z for z in ACHV if z['name'] not in attained_names and "not_via_playing" in z]
    inactive = [z for z in ACHV if z['name'] not in attained_names and "inactive" in z]
    missing = [z for z in ACHV if z['name'] not in attained_names and not ("inactive" in z or "not_via_playing" in z)]
    
    msgs = []
    header = "*ATTAINED ({0}/{1}):*\n".format(attained_count, total)
    msg = ""
    
    for each in stats:
        if each['name'] in achv_names:
            msg += "- {}\n".format(each['name'])
    
    msg = header + "```" + msg + "```"
    msgs.append(msg)
    
    main = "*MISSING ({0}/{1}):*\n".format(total - attained_count , total)
    missing_header = "*MISSING AND ATTAINABLE VIA PLAYING ({0}/{1}):*\n\n".format(len(missing) , total)
    missing_msgs = []
    for z in missing:
        msg1 = "`- {}`\n".format(z['name'])
        msg1 += ">>> _{}_\n".format(z['desc'])
        missing_msgs.append(msg1)
    for each in chunks(missing_msgs, 30):
        msg = main + missing_header
        msg += "".join(each)
        msgs.append(msg)
    
    not_via_playing_header = "*NOT DIRECTLY ATTAINABLE VIA PLAYING ({0}/{1}):*\n\n".format(len(not_via_playing) , total)
    not_via_playing_msgs = []
    for z in not_via_playing:
        msg1 = "`- {}`\n".format(z['name'])
        msg1 += ">>> _{}_\n".format(z['desc'])
        not_via_playing_msgs.append(msg1)
    for each in chunks(not_via_playing_msgs, 30):
        msg = main + not_via_playing_header
        msg += "".join(each)
        msgs.append(msg)
    
    inactive_header = "*INACTIVE ({0}/{1}):*\n\n".format(len(inactive) , total)
    inactive_msgs = []
    for z in inactive:
        msg1 = "`- {}`\n".format(z['name'])
        msg1 += ">>> _{}_\n".format(z['desc'])
        inactive_msgs.append(msg1)
    for each in chunks(inactive_msgs, 30):
        msg = main + inactive_header
        msg += "".join(each)
        msgs.append(msg)
    
    return msgs
