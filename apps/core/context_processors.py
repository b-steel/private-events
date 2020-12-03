from .models import User
def invites(request):
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user.username)
        return {'invites': user.events_invited_to.all()}
    else:
        return {'invites': []}