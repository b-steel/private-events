FROM python:3.8-alpine

# set workdir
WORKDIR /usr/src/app

# install requirements
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copy project 
COPY . .

# migrate
RUN python manage.py migrate
#generate events
RUN python -c "import os; \
    from django.core.wsgi import get_wsgi_application; \
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'private_events.settings'); \
    application = get_wsgi_application(); \
    from apps.core.utils import lorem_ipsum; \
    lorem_ipsum(25)"

# CMD gunicorn --bind 0.0.0.0:8000 test_api.wsgi:application
CMD python manage.py runserver 0.0.0.0:8080

