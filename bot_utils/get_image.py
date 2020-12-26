from bot_utils.common import bot
from bot_utils.msg_template import MsgTemplate

def process(message):
    """
    Wrapper for photo data
    Receive user image, save it to user map
    """
    success = False
    try:
        # Download a photo by id and save it
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        success = bot.save_user_img(message.chat.id, downloaded_file)
    except:
        pass
    # Send response
    if success:
        bot.send_photo(message.chat.id, open(bot.uvojenie_img_path, 'rb'))
    bot.send_message(message.chat.id, MsgTemplate.get_photo_respond(success))
