#! usr/bin/sh

# migrate
python manage.py migrate
#generate events
python -c "import os; \
    from django.core.wsgi import get_wsgi_application; \
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'private_events.settings'); \
    application = get_wsgi_application(); \
    from apps.core.utils import lorem_ipsum; \
    lorem_ipsum(25)"
