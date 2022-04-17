import telebot
from ig_downloader import get_user_story
from ig_downloader import get_post
import os
from telegram.ext import Updater 
from telegram.ext import CommandHandler, MessageHandler, Filters
from telegram import ParseMode


token = '5190894970:AAES0EweIzvAg3NI4pxXuVVb7MpN3lXbE68'
updater = Updater(token,use_context=True)
dispacher = updater.dispatcher


def give_link(update, context):
    username = update.message.text.split(' ')[1]
    story_urls = get_user_story(username)
    for story_url in story_urls:
        update.message.reply_text(text=f"<a href={story_url}>download</a>",parse_mode=ParseMode.HTML)


def start(update, context):
    update.message.reply_text('Hello {}'.format(update.message.from_user.first_name))

start_handler = CommandHandler('start', start)
# send if message contains 'story'
story_handler = MessageHandler(Filters.regex('story'), give_link)


dispacher.add_handler(start_handler)
dispacher.add_handler(story_handler)
updater.start_polling()