class MsgTemplate:
    @staticmethod
    def start_respond():
        with open('data/cmd_start.html', 'r', encoding='utf-8') as file:
            return file.read()

    @staticmethod
    def help_respond():
        with open('data/cmd_help.html', 'r', encoding='utf-8') as file:
            return file.read()

    @staticmethod
    def get_photo_respond(success=True):
        if success:
            return "Fantastic! Now try /captured_image"
        else:
            return "Oooops! Try another photo"

    @staticmethod
    def captured_image_error(success=True, exception_occurred=False):
        if exception_occurred:
            return "Oooops! Something went wrong..."
        elif not success:
            return 'Error! You should send an image firstly'
        else:
            return ""

    @staticmethod
    def carousel_error(success=True, exception_occurred=False):
        if exception_occurred or not success:
            return "Oooops! Something went wrong..."
        else:
            return ""

    @staticmethod
    def prediction_start_notice():
        return 'Calculating! Please wait ~6s'

    @staticmethod
    def prediction_end_notice():
        return 'We\'ve done! Wanna do it again?'

    @staticmethod
    def default_respond():
        return 'Try /help to get a full description of bot commands'
