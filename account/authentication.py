from django.contrib.auth.models import User


class EmailAuthBackend(object):
    """ Backend аутентификации по email.
    
    Каждое введённое имя проверяется на соответствие не только в столбце 'username',
    но и в столбце e-mail. Введённый логин соответсвует какому-либо электронному
    адресу, функция возвращает объект пользователя по указанному e-mail.
    В противном случае такого пользователя не существует.
    """

    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
            return None
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

