import telebot
from ig_downloader import get_user_story
from ig_downloader import get_post
import os
from telegram.ext import Updater 
from telegram.ext import CommandHandler, MessageHandler, Filters



# def story(message):
#     username = message.text.split(' ')[1]
    
#     story_urls = get_user_story(username)
#     for story_url in story_urls:
#         bot.send_message(message.chat.id, story_url)
# bot = telebot.TeleBot(Token)


# @bot.message_handler(commands=['start'])
# def start(message):
#     bot.send_message(message.chat.id, 'Hello, ' +
#                      message.from_user.first_name + '!')


# @bot.message_handler(func=lambda message: 'story' in message.text.lower())
    

    


# @bot.message_handler(func=lambda message: 'post' in message.text.lower())
# def post(message):
#     url = message.text.split(' ')[1]    
#     for url in get_post(url):
        # bot.send_message(message.chat.id, url)

token = '5190894970:AAES0EweIzvAg3NI4pxXuVVb7MpN3lXbE68'
updater = Updater(token,use_context=True)
dispacher = updater.dispatcher


def give_link(update, context):
    username = update.message.text.split(' ')[1]
    story_urls = get_user_story(username)
    for story_url in story_urls:
        update.message.reply_text(story_url)


def start(update, context):
    update.message.reply_text('Hello {}'.format(update.message.from_user.first_name))

start_handler = CommandHandler('start', start)
# send if message contains 'story'
story_handler = MessageHandler(Filters.regex('story'), give_link)


dispacher.add_handler(start_handler)
dispacher.add_handler(story_handler)
updater.start_polling()