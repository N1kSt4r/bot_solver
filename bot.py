from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import re
import random
# import phase1
# import phase2
import numpy as np
import os
import time

methods = ['phase1', 'phase2']

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def start(bot, update):
    update.message.reply_text('Hi. Today I help you resolve some tasks\n'
                              'Use /help - to get cookie... Nooo, to get a format for message')


def help(bot, update):
    update.message.reply_text('Use get_list - to get list of method\n'
			      			  'Use get_format *some_number* to check format for method')


def take_args(task_name):
    file = './{}/{}'.format(task_name, task_name)
    return 'python {}.py < {}.input > {}.output 2> {}.output'.format(task_name, file, file, file)


def echo(bot, update):
    message = re.split("[\n]+", update.message.text)

    if re.match("(get_format )[\\d]+", message[0]):
        k = int(message[0][11:])
        buffer = ''
        for string in open('./{}/{}.format'.format(methods[k], methods[k])):
            buffer += string

        update.message.reply_text(buffer)
    elif re.match("(solve )[\\d]+", message[0]):
        k = int(message[0][6:])
        
        input = open('./{}/{}.input'.format(methods[k], methods[k]), 'w')
        for line in message[1:]:
            input.write(line + '\n')
        time.sleep(1)
        input.close()
        
        os.system(take_args(methods[k]))
        time.sleep(3)
        
        buffer = ''
        for string in open('./{}/{}.output'.format(methods[k], methods[k])):
            buffer += string

        update.message.reply_text(buffer)
    elif message[0] == 'get_list':
        update.message.reply_text('0. Simplex-method. Phase 1. ' + '\n1. Simplex-method. Phase 2')
    else:
        update.message.reply_text("Sorry, but incorrect format of message...")
        help(bot, update)


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    updater = Updater("800022406:AAFW0iQ5neKikMzIIGE1GMnDrrbQkACCWq8")

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    dp.add_handler(MessageHandler(Filters.text, echo))

    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
