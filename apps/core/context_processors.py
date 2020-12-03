from .models import User
from django.utils import timezone

def invites(request):
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user.username)
        return {'invites': user.events_invited_to.all().filter(date__gte=timezone.now())}
    else:
        return {'invites': []}