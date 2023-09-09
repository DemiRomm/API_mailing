from time import sleep
from django.utils import timezone
from datetime import datetime
import requests
from .models import Mailing, Client, Message
from celery import shared_task
import logging

logging.basicConfig(
    level=logging.DEBUG,
    filename='app_log.log',
    format='[%(asctime)s: %(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)


TIME_SLEEP = 5
API_TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MjUwMDkwNTEsImlzcyI6ImZhYnJpcXVlIiwibmFtZSI6Imh0dHBzOi8vdC5tZS93aW5nc29mbGliZXJ0eXkifQ.ErqdV0rpJctG0pkbnl5M61l8Qd9H6PU_d3_2Oso1bho'


def send_message(message_id, client, text_mail):
    headers = {'Authorization': f'Bearer {API_TOKEN}'}
    json = {
        "id": message_id,
        "phone": client,
        "text": text_mail
    }
    try:
        response = requests.post(
            f'https://probe.fbrq.cloud/v1/send/{message_id}',
            headers=headers,
            json=json
        )
        logger.info('Отправка сообщения через внешний API завершена')
        if response.status_code == 200:
            return 'Успешно'
        else:
            return 'Ошибка'
    except Exception as err:
        logging.error(f'Сбой при отправке сообщения: {err}')
        return 'Ошибка. Сбой при отправке сообщения'


@shared_task()
def mailing_start():
    logging.debug('Старт новой рассылки')
    message_id = [1]
    success_mailing_list = []

    while True:
        try:
            mailings = Mailing.objects.all()
            for mailing in mailings:
                now = timezone.make_aware(datetime.now())
                if mailing.start_send <= now and mailing.stop_send >= now and \
                        mailing.id not in success_mailing_list:
                    mailing_id = mailing
                    tag = mailing.tag
                    mobile_code = mailing.mobile_code
                    text_mail = mailing.text_mail
                    clients = Client.objects.filter(
                        tag=tag
                    ).filter(
                        mobile_code=mobile_code
                    )
                    for client in clients:
                        client_id = client
                        if send_message(message_id[0], int(client.id), text_mail == 'Успешно'):
                            Message.objects.create(
                                status='Отправлено',
                                mailing_id=mailing_id,
                                client_id=client_id
                            )
                        else:
                            Message.objects.create(
                                status='Не отправлено',
                                mailing_id=mailing_id,
                                client_id=client_id
                            )
                        message_id[0] += 1
                    success_mailing_list.append(mailing_id.id)
            logging.debug('Рассылка завершена')
            sleep(TIME_SLEEP)
        except Exception as err:
            logging.error(f'Сбой в работе программы: {err}')
            logging.debug('Перезапуск...')
            sleep(TIME_SLEEP)
