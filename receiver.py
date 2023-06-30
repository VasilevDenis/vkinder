import constants


class Receiver:
    def __init__(self, json: dict) -> None:
        self.correct = False
        self.keyboard = None
        self.from_id = None
        self.text = None
        if json:
            if json['secret'] == constants.SECRET_KEY:
                if json['type'] == 'message_new':
                    self._extract_only_important_data(json)
                    self.correct = True

    def _extract_only_important_data(self, json: dict) -> None:
        self.keyboard = json['object']['client_info']['keyboard']
        self.from_id = json['object']['message']['from_id']
        self.text = json['object']['message']['text'].strip()
