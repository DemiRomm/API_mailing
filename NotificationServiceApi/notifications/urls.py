from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import ClientViewSet, MessageViewSet, MailingViewSet

app_name = 'notifications'

router = DefaultRouter()
router.register('mailings', MailingViewSet)
router.register('clients', ClientViewSet)
router.register('messages', MessageViewSet)

urlpatterns = [
    path('', include(router.urls))
]
