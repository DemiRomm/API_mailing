from rest_framework import serializers
from .models import Mailing, Client, Message


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'

    def validate_phone(self, number):
        if str(number)[0] != '7':
            raise serializers.ValidationError('Неверный формат номера. Введите номер в формате 7XXXXXXXXXX.')
        return number


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'


class MailingSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(read_only=True, many=True)

    class Meta:
        model = Mailing
        fields = (
            'id',
            'start_send',
            'stop_send',
            'text_mail',
            'mobile_code',
            'tag',
            'messages'
        )


class MailingListSerializer(serializers.ModelSerializer):
    sent_msg = serializers.SerializerMethodField(read_only=True)
    unsent_msg = serializers.SerializerMethodField(read_only=True)

    def get_sent_msg(self, msg):
        return msg.messages.filter(status='Отправлено').count()

    def get_unsent_msg(self, msg):
        return msg.messages.filter(status='Не отправлено').count()

    class Meta:
        model = Mailing
        fields = (
            'id',
            'start_send',
            'stop_send',
            'text_mail',
            'mobile_code',
            'tag',
            'sent_msg',
            'unsent_msg'
        )
