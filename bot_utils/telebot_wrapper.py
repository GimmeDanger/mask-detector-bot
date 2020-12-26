import telebot
from os import path
from telebot import apihelper
from itertools import cycle


class TelebotWrapper(telebot.TeleBot):

    data_path = 'data'
    user_data_path = fr'./{data_path}/user_data'
    examples_data_path = fr'./{data_path}/examples'
    uvojenie_img_path = fr'./{data_path}/uvojenie.png'

    # tracking user data: {user id, curr_po}
    user_carousel_pos_dict = dict()

    # proxy switching list,
    # thanks to https://github.com/uburuntu
    # for this idea and his inspiring bots
    curr_proxy = cycle([
        '',
        'socks5://telegram:telegram@sr123.spry.fail:1080',
        'socks5://28006241:F1zcUqql@phobos.public.opennetwork.cc:1090',
        'socks5://28006241:F1zcUqql@deimos.public.opennetwork.cc:1090',
        'socks5://telegram:telegram@sreju5h4.spry.fail:1080',
        'socks5://telegram:telegram@rmpufgh1.teletype.live:1080',
    ])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        apihelper.CONNECT_TIMEOUT = 2.5

    def set_proxy(self):
        apihelper.proxy = {'https': next(self.curr_proxy)}
        apihelper._get_req_session(reset=True)

    @staticmethod
    def run_carousel(pos, step):
        return (pos + step + 5) % 5

    def user_img_filename(self, user_id):
        return fr'{self.user_data_path}/{user_id}_image.jpg'

    def carousel_img_filename(self, pos):
        return fr'{self.examples_data_path}/{pos}.jpg'

    def user_img_preds_filename(self, user_id):
        return fr'{self.user_data_path}/{user_id}_image_preds.jpg'

    def save_user_img(self, user_id, downloaded_file):
        filename = self.user_img_filename(user_id)
        with open(filename, 'wb+') as new_file:
            new_file.write(downloaded_file)
        return True

    def captured_data_img(self, user_id):
        filename = self.user_img_filename(user_id)
        if path.exists(filename):
            return open(filename, 'rb')
        return None

    def user_carousel_img(self, user_id, step=0):
        pos = 0
        if user_id in self.user_carousel_pos_dict:
            pos = self.user_carousel_pos_dict[user_id]
        pos = self.run_carousel(pos, step)
        filename = self.carousel_img_filename(pos)
        if path.exists(filename):
            img = open(filename, 'rb')
            self.user_carousel_pos_dict[user_id] = pos
            return img
        return None
