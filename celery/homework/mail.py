import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from PIL.Image import Image

from config import SMTP_HOST, SMTP_PORT, SMTP_PASSWORD, SMTP_USER


def send_email(order_id: str, receiver: str, filename: str):
    """
    Отправляет пользователю `receiver` письмо по заказу `order_id` с приложенным файлом `filename`

    Вы можете изменить логику работы данной функции
    """
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)

        email = MIMEMultipart()
        email['Subject'] = f'Изображения. Заказ №{order_id}'
        email['From'] = SMTP_USER
        email['To'] = receiver

        with open(filename, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())

        image_name = filename.split('/')[1][2:]

        encoders.encode_base64(part)
        part.add_header(
            'Content-Disposition',
            f'attachment; filename={image_name}'
        )
        email.attach(part)
        text = email.as_string()

        server.sendmail(SMTP_USER, receiver, text)


def send_newsletter(receiver: str):
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)

        email = MIMEMultipart()
        email['Subject'] = f'BlurImage. Еженедельная рассылка'
        email['From'] = SMTP_USER
        email['To'] = receiver

        text = """
        <html>
            <body>
                <p>Добрый день!<br>
                Это еженедельная рассылка от сервиса BlurImage.<br>
                Не забывайте про нас, и пользуйтесь нашим сервисом по чаще.<br>
                По любым вопросам обращайтесь в ответе на это письмо.
                </p>
            </body>
        </html>
        """

        part = MIMEText(text, "html")
        email.attach(part)

        server.sendmail(SMTP_USER, receiver, email.as_string())
