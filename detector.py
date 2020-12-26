from os import system
from bot_utils.common import bot

cfg_path = fr'data/cfg'
detector_path = fr'libs/darknet'
pred_output = 'predictions.jpg'


def predict(user_id):
    predict_command = fr'./{detector_path}/darknet detector test \
                         ./{cfg_path}/obj.data ./{cfg_path}/yolov4-obj.cfg ./{cfg_path}/yolov4_face_mask.weights \
                         {bot.user_img_filename(user_id)} -i 0 -thresh 0.45'
    move_command = fr'mv {pred_output} {bot.user_img_preds_filename(user_id)}'
    if 0 == system(fr'{predict_command} && {move_command}'):
        return open(bot.user_img_preds_filename(user_id), 'rb')
    return None
