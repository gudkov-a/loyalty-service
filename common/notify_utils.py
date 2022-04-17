from typing import Tuple


class NotifyHandler:

    def __init__(self, brand_name: str, user_name: str):
        self._brand_name = brand_name
        self._user_name = user_name

    def _compose_text(self) -> Tuple[str, str]:
        title = 'Notification of getting discount code'
        msg = f'Dear {self._brand_name} your customer with user login {self._user_name} now have a discount code!'
        return title, msg

    def notify(self):
        """
        Here we can use email, WhatsApp, Telegram or anything else
        """
        title, msg = self._compose_text()
        """
        Implementation is required
        """
