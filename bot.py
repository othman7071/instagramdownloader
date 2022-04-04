import telebot
from ig_downloader import get_user_story
from ig_downloader import get_post
import os

Token = '5190894970:AAES0EweIzvAg3NI4pxXuVVb7MpN3lXbE68'
bot = telebot.TeleBot(Token)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Hello, ' +
                     message.from_user.first_name + '!')


@bot.message_handler(func=lambda message: 'story' in message.text.lower())
def story(message):
    username = message.text.split(' ')[1]
    try:
        story_urls = get_user_story(username)
        for story_url in story_urls:
            bot.send_message(message.chat.id, story_url)
    except Exception as e:
        bot.send_message(message.chat.id, e)
        return

    


@bot.message_handler(func=lambda message: 'post' in message.text.lower())
def post(message):
    url = message.text.split(' ')[1]    
    for url in get_post(url):
        bot.send_message(message.chat.id, url)


bot.infinity_polling()
