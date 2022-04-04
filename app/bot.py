import telebot
from ig_downloader import get_user_story
from ig_downloader import get_post_media
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
    story_files = get_user_story(username)
    if story_files[0] == 0:
        bot.send_message(message.chat.id, story_files[1])
    else:
        for story_url in story_files[1]:
            # if story_file.endswith('.mp4'):
            #     bot.send_video(message.chat.id, open(story_file, 'rb'))
            # else:
            #     bot.send_photo(message.chat.id, open(story_file, 'rb'))
            # os.remove(story_file)
            bot.send_message(message.chat.id, story_url)


@bot.message_handler(func=lambda message: 'post' in message.text.lower())
def post(message):
    url = message.text.split('  ')[1]
    post_media = get_post_media(url)
    if post_media[0] == 0:
        bot.send_message(message.chat.id, post_media[1])
    else:
        # if post_media[1].endswith('.mp4'):
        #     bot.send_video(message.chat.id, open(post_media[1], 'rb'))
        # else:
        #     bot.send_photo(message.chat.id, open(post_media[1], 'rb'))
        # os.remove(post_media[1])
        bot.send_message(message.chat.id, post_media[1])


bot.infinity_polling()
