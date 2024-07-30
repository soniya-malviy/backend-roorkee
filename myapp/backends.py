from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.core.mail.backends.smtp import EmailBackend

UserModel = get_user_model()

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get('email')
        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        return None

    def get_user(self, user_id):
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None

# myapp/backends.py


class CustomEmailBackend(EmailBackend):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def open(self):
        if self.connection:
            return False
        try:
            self.connection = self.connection_class(self.host, self.port, **self.connection_params)
            self.connection.set_debuglevel(int(self.debug_level))
            if self.use_tls:
                self.connection.ehlo()
                self.connection.starttls()
                self.connection.ehlo()
            if self.username and self.password:
                self.connection.login(self.username, self.password)
            return True
        except Exception:
            if not self.fail_silently:
                raise
            return False