import re
import sys
import time
import requests

from bot_utils.common import bot
from bot_utils.msg_template import MsgTemplate
from bot_utils import get_image, captured_image, examples


""""""""""""""""""""" Commands and data handler """""""""""""""""""""


def commands_handler(cmnds):
    def wrapped(message):
        if not message.text:
            return False
        split_message = re.split(r'[^\w@/]', message.text.lower())
        s = split_message[0]
        return (s in cmnds) or (s.split('@')[0] in cmnds)

    return wrapped


@bot.message_handler(func=commands_handler(['/start']))
def command_start(message):
    bot.reply_to(message, MsgTemplate.start_respond(), parse_mode='HTML', disable_web_page_preview=True)


@bot.message_handler(func=commands_handler(['/help']))
def command_help(message):
    bot.reply_to(message, MsgTemplate.help_respond(), parse_mode='HTML', disable_web_page_preview=True)


@bot.message_handler(func=commands_handler(['/captured_image']))
def command_captured_image(message):
    captured_image.process(message)


@bot.message_handler(func=commands_handler(['/examples']))
def command_examples(message):
    examples.process(message)


@bot.message_handler(content_types=['photo'])
def photo(message):
    get_image.process(message)


@bot.message_handler(content_types=["text"])
def other_messages(message):
    bot.send_message(message.chat.id, MsgTemplate.default_respond())


""""""""""""""""""""" Main loop """""""""""""""""""""


if __name__ == '__main__':
    while True:
        try:
            bot.set_proxy()
            bot.polling(none_stop=True)

        except requests.exceptions.ReadTimeout as e:
            print('Read Timeout. Reconnecting in 5 seconds.')
            time.sleep(5)

        except requests.exceptions.ConnectionError as e:
            print('Connection Error. Reconnecting...')
            time.sleep(1)

        except KeyboardInterrupt as e:
            print('Keyboard Interrupt. Good bye.')
            sys.exit(0)
