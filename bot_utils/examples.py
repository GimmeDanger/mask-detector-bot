from bot_utils.common import bot
from bot_utils.msg_template import MsgTemplate
from telebot.types import InlineKeyboardButton as Button, InlineKeyboardMarkup, InputMediaPhoto


def keyboard_carousel():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(Button(text='⬅️(prev)', callback_data='prev'),
                 Button(text='➡️(next)', callback_data='next'), )
    return keyboard


def run_carousel_template(call, step):
    user_id = call.message.chat.id
    try:
        carousel_img = bot.user_carousel_img(user_id, step)
        if carousel_img is not None:
            bot.edit_message_media(chat_id=user_id, message_id=call.message.message_id,
                                   media=InputMediaPhoto(carousel_img), reply_markup=keyboard_carousel())
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False)
        else:
            bot.send_message(user_id, MsgTemplate.carousel_error(success=False))
    except Exception:
        bot.send_message(user_id, MsgTemplate.carousel_error(exception_occurred=True))


@bot.callback_query_handler(func=lambda call: call.data.startswith('prev'))
def callback_prev(call):
    run_carousel_template(call, step=-1)


@bot.callback_query_handler(func=lambda call: call.data.startswith('next'))
def callback_next(call):
    run_carousel_template(call, step=1)


def process(message):
    """
    Wrapper for command_examples
    Provide carousel of precomputed examples
    """
    user_id = message.chat.id
    try:
        carousel_img = bot.user_carousel_img(user_id)
        if carousel_img is not None:
            bot.send_photo(user_id, carousel_img,
                           reply_to_message_id=message.message_id,
                           reply_markup=keyboard_carousel())
        else:
            bot.send_message(user_id, MsgTemplate.carousel_error(success=False))
    except Exception:
        bot.send_message(user_id, MsgTemplate.carousel_error(exception_occurred=True))
