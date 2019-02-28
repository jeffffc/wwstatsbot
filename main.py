#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# wolfcardbot.py - Extracts Werewolf for Telegram Stats & Displays in Chat
# author - Carson True
# license - GPL

# edited by @jeffffc

import requests
import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext.dispatcher import run_async
import datetime
import json

from config import BOT_TOKEN, LOG_GROUP_ID

import wwstats

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def get_stats(user_id):
    wuff_url = "http://www.tgwerewolf.com/Stats/PlayerStats/?pid={}&json=true"
    stats = requests.get(wuff_url.format(user_id)).json()
    return stats


def get_achievement_count(user_id):
    wuff_url = "http://www.tgwerewolf.com/Stats/PlayerAchievements/?pid={}&json=true"
    r = requests.get(wuff_url.format(user_id)).json()
    return len(r)
	
def get_kills(user_id):
    wuff_url = "http://www.tgwerewolf.com/Stats/PlayerKills/?pid={}&json=true"
    kills = requests.get(wuff_url.format(user_id)).json()
    return kills

def get_killed_by(user_id):
    wuff_url = "http://www.tgwerewolf.com/Stats/PlayerKilledBy/?pid={}&json=true"
    killedby = requests.get(wuff_url.format(user_id)).json()
    return killedby

def get_deaths(user_id):
    wuff_url = "http://www.tgwerewolf.com/Stats/PlayerDeaths/?pid={}&json=true"
    deaths = requests.get(wuff_url.format(user_id)).json()
    return deaths
	
@run_async
def display_kills(bot, update):
    chat_id = update.message.chat_id
    if update.message.reply_to_message is not None:
        user_id = update.message.reply_to_message.from_user.id
        name = update.message.reply_to_message.from_user.first_name
    else:
        user_id = update.message.from_user.id
        name = update.message.from_user.first_name

    print("%s - %s (%d) - kills" % (str(datetime.datetime.now()+datetime.timedelta(hours=8)), name, user_id))

    kills = get_kills(user_id)

    msg = "Players <a href='tg://user?id={}'> {}</a> most killed:\n".format(user_id, name)
    
    for n in range(len(kills)):
        msg += "<code>{:<5}</code> <b>{}</b>\n".format(kills[n]['times'],kills[n]['name'])
    
    bot.sendMessage(chat_id, msg, parse_mode="HTML", disable_web_page_preview=True)

@run_async	
def display_killed_by(bot, update):
    chat_id = update.message.chat_id
    if update.message.reply_to_message is not None:
        user_id = update.message.reply_to_message.from_user.id
        name = update.message.reply_to_message.from_user.first_name
    else:
        user_id = update.message.from_user.id
        name = update.message.from_user.first_name

    print("%s - %s (%d) - killed by" % (str(datetime.datetime.now()+datetime.timedelta(hours=8)), name, user_id))

    killedby = get_killed_by(user_id)

    msg = "Players who killed <a href='tg://user?id={}'>{}</a> most:\n".format(user_id, name)
    
    for n in range(len(killedby)):
        msg += "<code>{:<5}</code> <b>{}</b>\n".format(killedby[n]['times'],killedby[n]['name'])
    
    bot.sendMessage(chat_id, msg, parse_mode="HTML", disable_web_page_preview=True)

@run_async
def display_deaths(bot, update):
    chat_id = update.message.chat_id
    if update.message.reply_to_message is not None:
        user_id = update.message.reply_to_message.from_user.id
        name = update.message.reply_to_message.from_user.first_name
    else:
        user_id = update.message.from_user.id
        name = update.message.from_user.first_name

    print("%s - %s (%d) - deaths" % (str(datetime.datetime.now()+datetime.timedelta(hours=8)), name, user_id))

    deaths = get_deaths(user_id)
    stats = get_stats(user_id)

    msg = "Types of deaths that <a href='tg://user?id={}'>{}</a> most had:\n".format(user_id, name)
    
    for n in range(len(deaths)):
        
        """ The total of deaths for each kill method is calculated based on the percentage
        gave by the JSON data. Because of that, the calculated value is not totally accurate."""
	
        totalMethod = ((stats['gamesPlayed']-stats['survived']['total'])*float(deaths[n]['percent'])/100)
        msg += "<code>{}%</code>   <b>{}</b>   <code>(approx. {})</code>\n".format(deaths[n]['percent'],deaths[n]['method'],round(totalMethod))
		
        """msg += "<code>({}%)</code> <b>{}</b>\n".format(deaths[n]['percent'],deaths[n]['method'])"""
    bot.sendMessage(chat_id, msg, parse_mode="HTML", disable_web_page_preview=True)
	
@run_async	
def display_stats(bot, update, args):
    chat_id = update.message.chat_id
    if update.message.reply_to_message is not None:
        user_id = update.message.reply_to_message.from_user.id
        name = update.message.reply_to_message.from_user.first_name
    else:
        if args:
	    try:
                user_id = int(args[0])
                name = args[0]
            except:
                user_id = update.message.from_user.id
                name = update.message.from_user.first_name
        else:
            user_id = update.message.from_user.id
            name = update.message.from_user.first_name

    print("%s - %s (%d) - stats" % (str(datetime.datetime.now()+datetime.timedelta(hours=8)), name, user_id))

    stats = get_stats(user_id)
    achievements = get_achievement_count(user_id)

    msg = "<a href='tg://user?id={}'>{} the {}</a>\n".format(user_id, name, stats['mostCommonRole'])
    msg += "<code>{:<5}</code> Achievements Unlocked!\n".format(achievements)
    msg += "<code>{:<5}</code> Games Won <code>({}%)</code>\n".format(stats['won']['total'], stats['won']['percent'])
    msg += "<code>{:<5}</code> Games Lost <code>({}%)</code>\n".format(stats['lost']['total'], stats['lost']['percent'])
    msg += "<code>{:<5}</code> Games Survived <code>({}%)</code>\n".format(
        stats['survived']['total'], stats['survived']['percent'])
    msg += "<code>{:<5}</code> Total Games\n".format(stats['gamesPlayed'])
    msg += "<code>{:<5}</code> times I've gleefully killed {}\n".format(
        stats['mostKilled']['times'], stats['mostKilled']['name'])
    msg += "<code>{:<5}</code> times I've been slaughted by {}\n\n".format(
        stats['mostKilledBy']['times'], stats['mostKilledBy']['name'])

    bot.sendMessage(chat_id, msg, parse_mode="HTML", disable_web_page_preview=True)


def display_about(bot, update):
    chat_id = update.message.chat_id
    msg = "Use /stats for stats. Use /achievements or /achv for achivement list."
    msg += "\n\nThis is an edited version to the old `@wolfcardbot`.\n"
    msg += "Click [here](http://pastebin.com/efZ4CPXJ) to check the original source code.\n"
    msg += "Click [here](https://github.com/jeffffc/wwstatsbot) for the source code of the current project."

    bot.sendMessage(chat_id, msg, parse_mode="Markdown", disable_web_page_preview=True)


def startme(bot, update):
    if update.message.chat.type == 'private':
        update.message.reply_text("Thank you for starting me. "
                                  "Use /stats and /achievements to check your related stats!")
    else:
        return


@run_async
def display_achv(bot, update):
    user_id = update.message.from_user.id
    name = update.message.from_user.first_name

    print("%s - %s (%d) - achv" % (str(datetime.datetime.now()+datetime.timedelta(hours=8)), name, user_id))

    msgs = wwstats.check(user_id)

    try:
        for msg in msgs:
            bot.sendMessage(chat_id = user_id, text=msg, parse_mode='Markdown')
        if update.message.chat.type != 'private':
            update.message.reply_text("I have sent you your achievement list in PM.")
    except:
        url = "telegram.me/{}".format(bot.username)
        keyboard = [[InlineKeyboardButton("Start Me!", url=url)]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text("You have to start me in PM first.", reply_markup=reply_markup)


def error_handler(bot, update, error):
    e = str(error).lower()
    if "timed out" in e or "not modified" in e or "query_id_invalid" in e:
        return
    msg = "This update caused error.\n"
    msg += "{}\n\n".format(error.msg)
    msg += "```{}```".format(json.dumps(json.loads(update.message.to_json()), indent=2, ensure_ascii=False))
    bot.send_message(LOG_GROUP_ID, error.msg, parse_mode='Markdown')


def main():
    u = Updater(token=BOT_TOKEN)
    d = u.dispatcher

    d.add_handler(CommandHandler('start', startme))
    d.add_handler(CommandHandler('stats', display_stats, pass_args=True))
    d.add_handler(CommandHandler('kills', display_kills))
    d.add_handler(CommandHandler('killedby', display_killed_by))
    d.add_handler(CommandHandler('deaths', display_deaths))
    d.add_handler(CommandHandler('about', display_about))
    d.add_handler(CommandHandler(['achievements', 'achv'], display_achv))
    d.add_error_handler(error_handler)
    u.start_polling(clean=True)
    u.idle()


if __name__ == '__main__':
    main()
