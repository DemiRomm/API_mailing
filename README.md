Документация по запуску API

1.	Создать новый проект python с виртуальным окружением

2.	Клонировать репозиторий и перейти в папку проекта:
git clone https://gitlab.com/dev6660336/notificationserviceapi.git
cd notificationserviceapi\NotificationServiceApi

3.	Установить зависимости:
pip install -r requirements.txt

4.	Создать и применить миграции:
python manage.py makemigrations
python manage.py migrate

5.	Запуск сервера Django:
python manage.py runserver

Документация по API после запуска сервера доступна по следующим адресам:
http://127.0.0.1:8000/swagger/
http://127.0.0.1:8000/docs/

6.	Запуск брокера redis в новом окне терминала:
cd notificationserviceapi\NotificationServiceApi
redis-server 

7.	Запуск воркера Celery в новом окне терминала:
cd notificationserviceapi\NotificationServiceApi
celery -A NotificationServiceApi worker --loglevel=info -P eventle

8.	Запуск задачи по рассылке уведомлений в новом окне терминала:
>>>python manage.py shell
>>> mailing_start()

9.	(Опционально) Включение Celery Beat для очередности рассылки (каждые 12 часов) в новом окне терминала:
cd notificationserviceapi\NotificationServiceApi
celery -A NotificationServiceApi beat -l info