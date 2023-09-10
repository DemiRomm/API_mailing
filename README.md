# Документация по запуску API

***

### 1.	Создать новый проект python с виртуальным окружением

### 2.	Клонировать репозиторий и перейти в папку проекта:

```bash
git clone https://gitlab.com/dev6660336/notificationserviceapi.git
```
```bash
cd notificationserviceapi\NotificationServiceApi
```

### 3.	Установить зависимости:
```bash
pip install -r requirements.txt
```
### 4.	Создать и применить миграции:
```bash
python manage.py makemigrations
```
```bash
python manage.py migrate
```
### 5.	Запуск сервера Django:
```bash
python manage.py runserver
```
### 6. Документация по API после запуска сервера доступна по следующим адресам:

* http://127.0.0.1:8000/swagger/

* http://127.0.0.1:8000/docs/

### 7.	Запуск брокера redis в новом окне терминала:
```bash
cd notificationserviceapi\NotificationServiceApi
```
```bash
redis-server 
```
### 8.	Запуск воркера Celery в новом окне терминала:
```bash
cd notificationserviceapi\NotificationServiceApi
```
```bash
celery -A NotificationServiceApi worker --loglevel=info -P eventlet
```
### 9.	Запуск задачи по рассылке уведомлений в новом окне терминала:
```bash
python manage.py shell
```
```bash
from notifications.tasks import mailing_start
```
```bash
mailing_start()
```
### 10.	(Опционально) Включение Celery Beat для очередности рассылки (каждые 12 часов) в новом окне терминала:
```bash
cd notificationserviceapi\NotificationServiceApi
```
```bash
celery -A NotificationServiceApi beat -l info
```