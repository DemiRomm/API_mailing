from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from .models import Client, Message, Mailing
from .serializers import ClientSerializer, MessageSerializer, MailingSerializer, MailingListSerializer
from .tasks import mailing_start


class MailingViewSet(viewsets.ModelViewSet):
    queryset = Mailing.objects.all()
    serializer_class = MailingSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ('mobile_code', 'tag')

    def get_serializer_class(self):
        if self.action == 'list':
            return MailingListSerializer
        return MailingSerializer

    @action(detail=False, url_path='test_start')
    def test_start(*args, **kwargs):
        mailing_start()


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filter_backends = [DjangoFilterBackend]


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ('mobile_code', 'tag')
