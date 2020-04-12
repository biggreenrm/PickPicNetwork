from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.


class Profile(models.Model):
    """ Модель Profile.
    
    Модель, расширяющая стандартную пользовательскую модель Django методом "один к одному".
    По сути своей представляет дополнительную таблицу, которая связана по полю "user"
    со стандартной моделью, добавляя столбцы с датой рождения и фото.
    """
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to="users/%Y/%m/%d/", blank=True)

    def __str__(self):
        return "Profile for user {}".format(self.user.username)


class Contact(models.Model):
    """ Модель Contact.
    
    Представляет собой таблицу из трёх столбцов. Первые два ссылаются на зарегистрированных пользователей
    из стандартной модели Django (используя внешний ключ), где "user_from" - подписчик, "user_to" - тот,
    на кого подписываются. Третий столбец модели является полем с датой создания связи.
    """
    
    user_from = models.ForeignKey('auth.User',
                                  related_name='rel_from_set',
                                  on_delete=models.CASCADE)
    user_to = models.ForeignKey('auth.User',
                                related_name='rel_to_set',
                                on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    
    # Обратный порядок отображения полей модели
    class Meta:
        ordering = ('-created',)
    
    # Переопределение образа отображения модели    
    def __str__(self):
        return '{} follows {}'.format(self.user_from, self.user_to)

# Динамическое добавление поля в класс User
# Обусловлено тем, что User в данном случае - встроенная модель
# Существуют и другие варианты расширения модели
User.add_to_class('following',
                  models.ManyToManyField('self',
                                         through=Contact,
                                         related_name='followers',
                                         symmetrical=False))