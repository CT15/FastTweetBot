import logging
import telegram_id

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from keys_tokens import BOT_TOKEN
from twitter import api

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

is_creating_tweet = False
saved_tweet = None

def start(bot, update):
    start_message = ('Hi there! Welcome to Fast Tweet Bot, '
                    'a bot that helps you to tweet content '
                    'on your Twitter account. Try the /help '
                    'command to see all available commands.')

    update.message.reply_text(start_message)


def help(bot, update):
    help_message = ('You can control me by sending these commands:\n'
                    '/create - create and save a new Tweet\n'
                    '/tweet - post a saved Tweet to Twitter\n'
                    '/saved - see your saved Tweet\n')

    update.message.reply_text(help_message)

def check_is_creating_tweet(update):
    global is_creating_tweet

    if is_creating_tweet:
        update.message.reply_text('Abort creating new Tweet.')
        is_creating_tweet = False


def create(bot, update):
    global is_creating_tweet

    is_creating_tweet = True
    update.message.reply_text('You can start creating your Tweet now ...')


def tweet(bot, update):
    global saved_tweet

    if update.message.from_user.id != telegram_id.id:
        no_match_message = ('Sorry, you cannot Tweet using this bot because '
                            'you are not the owner of this bot. However, you '
                            'can create one for yourself by following the step'
                            'by step guide at https://github.com/CT15/FastTweetBot')
        update.message.reply_text(no_match_message)
        return

    check_is_creating_tweet(update)

    if saved_tweet is None:
        fail_message = ('You have not created any Tweet yet. '
                        'Use the /create command to create one.')
        update.message.reply_text(fail_message)
        return

    keyboard = [[InlineKeyboardButton('Yes', callback_data='Yes'),
                 InlineKeyboardButton('No', callback_data='No')]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    message = ('Are you sure? '
               'Use the /saved command to check what you are going to Tweet.')

    update.message.reply_text(message, reply_markup=reply_markup)


def confirm_tweet(bot, update):
    global saved_tweet

    query = update.callback_query
    confirm_message = ('Tweeted successfully! Saved Tweet is cleared.')
    cancel_message = ('Cancel Tweeting. '
                      'Use the /saved command to see your saved Tweet.')
    missing_tweet_message = ('There is currently no saved Tweet. '
                             'Use the /create command to create one.')
    message = confirm_message

    if query.data == 'Yes' and saved_tweet is not None:
        api.update_status(saved_tweet)
        saved_tweet = None
    elif query.data == 'No':
        message = cancel_message
    else:
        message = missing_tweet_message

    bot.edit_message_text(text=message,
                      chat_id=query.message.chat_id,
                      message_id=query.message.message_id)


def saved(bot, update):
    global saved_tweet

    check_is_creating_tweet(update)

    if saved_tweet is not None:
        update.message.reply_text('Your saved Tweet: ' + saved_tweet)
        return

    no_saved_tweet_message = ('There is currently no saved Tweet. '
                              'Use the /create command to create one.')

    update.message.reply_text(no_saved_tweet_message)


def create_tweet(bot, update):
    global is_creating_tweet
    global saved_tweet

    if not is_creating_tweet:
        fail_message = ('Are you trying to create a Tweet? Use the /create '
                        'command to do so.')

        update.message.reply_text(fail_message)
        return

    char_count = len(update.message.text)
    if char_count > 280:
        fail_message = (f"Your Tweet contains {char_count}. "
                        'Twitter only allows a maximum of 280 characters '
                        'per Tweet.\n'
                        'You can start recreating your Tweet now ...')
        update.message.reply_text(fail_message)

    saved_tweet = update.message.text
    success_message = ('Your tweet is successfully saved! '
                       'Use the /saved command to see your saved Tweet.')
    update.message.reply_text(success_message)

    is_creating_tweet = False
    return


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    """Start the bot"""
    updater = Updater(BOT_TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('help', help))

    dp.add_handler(CommandHandler('create', create))
    dp.add_handler(CommandHandler('tweet', tweet))
    updater.dispatcher.add_handler(CallbackQueryHandler(confirm_tweet))
    dp.add_handler(CommandHandler('saved', saved))

    dp.add_handler(MessageHandler(Filters.text, create_tweet))

    dp.add_error_handler(error)

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()
