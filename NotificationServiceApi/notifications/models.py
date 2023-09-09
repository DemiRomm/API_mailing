from django.db import models


class Mailing(models.Model):
    start_send = models.DateTimeField('Дата и время запуска рассылки')
    stop_send = models.DateTimeField('Дата и время окончания рассылки')
    text_mail = models.TextField('Текст сообщения')
    mobile_code = models.CharField('Код мобильного оператора', max_length=10)
    tag = models.CharField('Тег', max_length=20)

    def __str__(self):
        return self.text_mail


class Client(models.Model):
    phone = models.PositiveIntegerField('Номер телефона', unique=True)
    mobile_code = models.CharField('Код мобильного оператора', max_length=10)
    tag = models.CharField('Тег', max_length=20)
    gmt = models.CharField('Часовой пояс', max_length=5)

    def __str__(self):
        return self.phone


class Message(models.Model):
    STATUS_CHOICES = (('Отправлено', 'Отправлено'), ('Не отправлено', 'Не отправлено'))
    datetime_send = models.DateTimeField('Дата и время создания (отправки)', auto_now_add=True)
    status = models.CharField('Статус отправки', max_length=13, choices=STATUS_CHOICES)
    mailing_id = models.ForeignKey(Mailing, on_delete=models.CASCADE, related_name='messages')
    client_id = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='messages')
