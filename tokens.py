import os

# Set your api tokens and keys through environmental variables
# (add lines to your .bashrc and restart terminal):
# export DEEP_AUTOENCODER_BOT_TOKEN='XXXXX:XXXXXXXXXXX'

default_bot = ''
bot = os.getenv('FMASK_DETECTOR_BOT_TOKEN', default_bot)
