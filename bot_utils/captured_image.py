from detector import predict
from bot_utils.common import bot
from bot_utils.msg_template import MsgTemplate
from telebot.types import InlineKeyboardButton as Button, InlineKeyboardMarkup, InputMediaPhoto


def keyboard_scan():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(Button(text='🤖(detect)', callback_data='detect'),)
    return keyboard


@bot.callback_query_handler(func=lambda call: call.data.startswith('detect'))
def callback_detect(call):
    user_id = call.message.chat.id
    try:
        user_img = bot.captured_data_img(user_id)
        if user_img is not None:
            bot.edit_message_media(chat_id=user_id, message_id=call.message.message_id,
                                   media=InputMediaPhoto(user_img, caption=MsgTemplate.prediction_start_notice()))
            processed_photo = predict(user_id)
            bot.edit_message_media(chat_id=user_id, message_id=call.message.message_id,
                                   media=InputMediaPhoto(processed_photo, caption=MsgTemplate.prediction_end_notice()))
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False)
        else:
            bot.send_message(user_id, MsgTemplate.captured_image_error(success=False))
    except Exception:
        bot.send_message(user_id, MsgTemplate.captured_image_error(exception_occurred=True))


def process(message):
    """
    Wrapper for command_captured_image,
    It start detector usage scenario
    """
    user_id = message.chat.id
    try:
        user_img = bot.captured_data_img(user_id)
        if user_img is not None:
            bot.send_photo(user_id, user_img,
                           reply_to_message_id=message.message_id,
                           reply_markup=keyboard_scan())
        else:
            bot.send_message(user_id, MsgTemplate.captured_image_error(success=False))
    except Exception:
        bot.send_message(user_id, MsgTemplate.captured_image_error(exception_occurred=True))
