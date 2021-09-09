import logging
import os
from formatter import Formatter as f
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

PORT = int(os.environ.get('PORT', 5000))

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
TOKEN = os.environ['telegramkey']


def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hello! Welcome to GeoApp, type or click /help for instructions.')

def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text("This is a Geography Bot designed to help you find yourself or somewhere.\n\
    To check the current weather of a place, type /weather nameoftheplace.\n\
    To check aditional information of a place, type /placeinfo nameoftheplace.")

def weather(update,context):
    try:
        update.message.reply_text(f.get_weather(context))
    except Exception as e:
        print("Error running General Info. Command: " + str(update.message.text) + " | Error: " + str(e))
        update.message.reply_text("Não digite nada após /covidbr.")

def placeinfo(update,context):
    try:
        UF = update.message.text.split(" ")[1]
        update.message.reply_text(f.get_uf(UF))
    except Exception as e:
        print("Error running UF. Command: " + str(update.message.text) + " | Error: " + str(e))
        update.message.reply_text("Esta não é uma Unidade Federativa válida.")

def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("weather", weather))
    dp.add_handler(CommandHandler("placeinfo", placeinfo))


    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
    updater.bot.setWebhook('https://pythongeobot.herokuapp.com/' + TOKEN)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()