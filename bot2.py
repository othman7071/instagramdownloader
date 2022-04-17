from telegram.ext import Updater 
from telegram.ext import CommandHandler, MessageHandler, Filters
from api import InstaLink

from telegram import ParseMode

token = '5190894970:AAES0EweIzvAg3NI4pxXuVVb7MpN3lXbE68'

downloader = InstaLink('saitaro.bot','othman8462','settings.json')

updater = Updater(token,use_context=True)
dispacher = updater.dispatcher

def start(update, context):
    update.message.reply_text('Hello {}'.format(update.message.from_user.first_name))

def give_link(update, context):
    text = update.message.text.split(' ')[1]
    for story in downloader.get_user_stories(text):
        update.message.reply_text(text=f"<a href={story}>download</a>",parse_mode=ParseMode.HTML)
        
start_handler = CommandHandler('start', start)

# send if message contains 'story'
story_handler = MessageHandler(Filters.regex('story'), give_link)

dispacher.add_handler(start_handler)
dispacher.add_handler(story_handler)
updater.start_polling()