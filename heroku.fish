set APPNAME ''

heroku stack:set container --app=$APPNAME

heroku config:set DJANGO_SECRET_KEY='' \
    DJANGO_DEBUG=1 \ 
    DJANGO_ALLOWED_HOSTS='.herokuapp.com'