from telegram.ext import Updater 
from telegram.ext import CommandHandler, MessageHandler, Filters
from api import InstaLink


token = '5190894970:AAES0EweIzvAg3NI4pxXuVVb7MpN3lXbE68'
downloader = InstaLink('saitaro.bot','othman8462','settings.json')
updater = Updater(token,use_context=True)
dispacher = updater.dispatcher

story_image = 'https://i.ibb.co/RQwcPBS/Screenshot-2022-04-20-183948.png'
post_image = 'https://i.ibb.co/YhXbcSD/Screenshot-2022-04-20-184106.png'



def help(update, context):
    help_message = """
you can use this bot to download stories/igtv/posts media from instagram

to get stories use 
@username
            
to get post or igtv use
url 

    """
   
    update.message.reply_text(help_message)
    update.message.reply_text(text=f"<a href='{post_image}'>.</a>",parse_mode='HTML')
    update.message.reply_text(text=f"<a href='{story_image}'>.</a>",parse_mode='HTML')


def start(update, context):
    update.message.reply_text('Hello {}\n '.format(update.message.from_user.first_name))
    help(update,context)





def story_media_link(update, context):
    url = update.message.text.replace('@','')
    for story in downloader.get_user_stories(url):
        update.message.reply_text(text=f"<a href='{story}'>.</a>",parse_mode='HTML')
    


def post_media_link(update,context):
    url = update.message.text
    for media in downloader.get_post(url):
        if media == 'Invalid url':
            update.message.reply_text(text=media)
            return
        update.message.reply_text(text=f"<a href='{media}'>Download</a>",parse_mode='HTML')
    
def old(update,context):
    update.message.reply_text('طريقة تحميل الستوري قد تغيرت ')
    update.message.reply_text(text=f"<a href='{story_image}'>.</a>",parse_mode='HTML')
    


start_handler = CommandHandler('start', start)
help_handler = CommandHandler('help', help)
story_handler = MessageHandler(Filters.regex('^@') , story_media_link)
post_handler = MessageHandler(Filters.regex('^http') , post_media_link)
old_handler = MessageHandler(Filters.regex('story'), start)
dispacher.add_handler(start_handler)
dispacher.add_handler(help_handler)
dispacher.add_handler(story_handler)
dispacher.add_handler(post_handler)
updater.start_polling()