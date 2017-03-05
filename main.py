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
from bs4 import BeautifulSoup

from config import *
import wwstats

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

telegram_api_token =  BOT_TOKEN

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
    
def get_achievement_count(user_id):
    wuff_url = "http://www.tgwerewolf.com/Stats/PlayerAchievements/?pid={}"
    
    r = requests.get(wuff_url.format(user_id))
    
    dump = BeautifulSoup(r.json(), 'html.parser')
    
    count = int(len(dump('td')) / 2)
    
    return count

def display_stats(bot, update):
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id
    name = update.message.from_user.first_name
    username = update.message.from_user.username
    
    stats = get_stats(user_id)
    achievements = get_achievement_count(user_id)
    
    msg =  "<a href=\"https://telegram.me/" + str(username) + "\">" + str(name) + " the " + stats['most_common_role']['role'] + "</a>\n"
    msg += "<code>{:<4}</code> Achievements Unlocked!\n".format(achievements)
    msg += "<code>{:<4}</code> Games Won <code>({})</code>\n".format(stats['games_won']['number'], stats['games_won']['percent'])
    msg += "<code>{:<4}</code> Games Lost <code>({})</code>\n".format(stats['games_lost']['number'], stats['games_lost']['percent'])
    msg += "<code>{:<4}</code> Games Survived <code>({})</code>\n".format(stats['games_survived']['number'], stats['games_survived']['percent'])
    msg += "<code>{:<4}</code><b> Total Games</b>\n".format(stats['games_played'])
    msg += "<code>{}</code><b> times I've gleefully killed {}</b>\n".format(stats['most_killed']['times'], stats['most_killed']['name'])
    msg += "<code>{}</code><b> times I've been slaughted by {}</b>\n\n".format(stats['most_killed_by']['times'], stats['most_killed_by']['name'])

    bot.sendMessage(chat_id, msg, parse_mode="HTML", disable_web_page_preview=True)

    
def display_about(bot, update):
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id
    name = update.message.from_user.first_name
    username = update.message.from_user.username

    msg = "This is a editted version to the old @wolfcardbot.\n"
    msg += "Click [here](http://pastebin.com/efZ4CPXJ) to check the original source code."

    bot.sendMessage(chat_id, msg, parse_mode="Markdown", disable_web_page_preview=True)
    


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
        
    d.add_handler(CommandHandler('stats', display_stats))
    d.add_handler(CommandHandler('about', display_about))
    d.add_handler(CommandHandler('achievements', display_achv))

    u.start_polling()
    u.idle()

if __name__ == '__main__':
    main()
