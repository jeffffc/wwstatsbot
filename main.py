#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# wolfcardbot.py - Extracts Werewolf for Telegram Stats & Displays in Chat
# author - Carson True
# license - GPL

# edited by @jeffffc

import requests
import logging

from telegram import ParseMode
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext.dispatcher import run_async
from bs4 import BeautifulSoup

from config import *
import wwstats

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

telegram_api_token =  BOT_TOKEN

#@run_async
def get_stats(user_id):
    stats = {}
    wuff_url = "http://www.tgwerewolf.com/Stats/PlayerStats/?pid={}"

    r = requests.get(wuff_url.format(user_id))

    dump = BeautifulSoup(r.json(), 'html.parser')

    stats['games_played'] = dump('td')[1].string
    stats['games_won'] = { 'number': dump('td')[3].string, 'percent': dump('td')[4].string }
    stats['games_lost'] = { 'number': dump('td')[6].string, 'percent': dump('td')[7].string }
    stats['games_survived'] = { 'number': dump('td')[9].string, 'percent': dump('td')[10].string  }
    stats['most_common_role'] = { 'role': dump('td')[12].string, 'times': dump('td')[13].string[:-6] }
    stats['most_killed'] = { 'name': dump('td')[15].string, 'times': dump('td')[16].string[:-6] }
    stats['most_killed_by'] = { 'name': dump('td')[18].string, 'times': dump('td')[19].string[:-6] }

    return stats


#@run_async
def get_achievement_count(user_id):
    wuff_url = "http://www.tgwerewolf.com/Stats/PlayerAchievements/?pid={}"

    r = requests.get(wuff_url.format(user_id))

    dump = BeautifulSoup(r.json(), 'html.parser')

    count = int(len(dump('td')) / 2)

    return count


@run_async
def display_stats(bot, update):
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id
    name = update.message.from_user.first_name
    username = update.message.from_user.username

    stats = get_stats(user_id)
    achievements = get_achievement_count(user_id)

    if username == "":
        msg =  str(name) + " the " + stats['most_common_role']['role'] + "\n"
    else:
        msg =  "<a href='https://telegram.me/" + str(username) + "'>" + str(name) + " the " + stats['most_common_role']['role'] + "</a>\n"
    msg += "<code>{:<5}</code> Achievements Unlocked!\n".format(achievements)
    msg += "<code>{:<5}</code> Games Won <code>({})</code>\n".format(stats['games_won']['number'], stats['games_won']['percent'])
    msg += "<code>{:<5}</code> Games Lost <code>({})</code>\n".format(stats['games_lost']['number'], stats['games_lost']['percent'])
    msg += "<code>{:<5}</code> Games Survived <code>({})</code>\n".format(stats['games_survived']['number'], stats['games_survived']['percent'])
    msg += "<code>{:<5}</code> Total Games\n".format(stats['games_played'])
    msg += "<code>{:<5}</code> times I've gleefully killed {}\n".format(stats['most_killed']['times'], stats['most_killed']['name'])
    msg += "<code>{:<5}</code> times I've been slaughted by {}\n\n".format(stats['most_killed_by']['times'], stats['most_killed_by']['name'])

    bot.sendMessage(chat_id, msg, parse_mode="HTML", disable_web_page_preview=True)

@run_async
def display_about(bot, update):
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id
    name = update.message.from_user.first_name
    username = update.message.from_user.username
    msg = "Use /stats for stats. Use /achievements or /achv for achivement list."
    msg += "\n\nThis is an edited version to the old @wolfcardbot.\n"
    msg += "Click [here](http://pastebin.com/efZ4CPXJ) to check the original source code.\n"
    msg += "Click [here](https://github.com/jeffffc/wwstatsbot) for the source code of the current project."

    bot.sendMessage(chat_id, msg, parse_mode="Markdown", disable_web_page_preview=True)


def startme(bot, update):
    if update.message.chat.type == 'private':
        update.message.reply_text("Thank you for starting me. Use /stats and /achievements to check your related stats!")
    else:
        return


@run_async
def display_achv(bot, update):
    user_id = update.message.from_user.id
    msg1, msg2 = wwstats.check(user_id)
    try:
        bot.sendMessage(chat_id = user_id, text = msg1, parse_mode='Markdown')
        bot.sendMessage(chat_id = user_id, text = msg2, parse_mode='Markdown')
        if update.message.chat.type != 'private':
            update.message.reply_text("I have sent you your achievement list in PM.")
    except:
        update.message.reply_text("You have to start me in PM first.")


def main():
    u = Updater(token=telegram_api_token)
    d = u.dispatcher

    d.add_handler(CommandHandler('start', startme))
    d.add_handler(CommandHandler('stats', display_stats))
    d.add_handler(CommandHandler('about', display_about))
    d.add_handler(CommandHandler('achievements', display_achv))
    d.add_handler(CommandHandler('achv', display_achv))
    u.start_polling()
    u.idle()

if __name__ == '__main__':
    main()
