from flask_mail import Mail


class AppMail(Mail):

    def send(self, message):
        with self.connect() as connection:
            message.send(connection)
