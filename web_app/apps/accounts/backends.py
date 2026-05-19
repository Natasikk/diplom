from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()


class EmailOrUsernameBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if not username or not password:
            return None

        user = User.objects.filter(Q(username=username) | Q(email=username)).first()

        if user and user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None