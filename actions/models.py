from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# Create your models here.


class Action(models.Model):
    """Модель для хранения пользовательских действий.
    
    Столбец user привязывается к стандартной модели пользователя Django,
    столбец verb хранит данные о действиях пользователя в текстовом виде,
    столбец created - дату создания, которая добавляется автоматически.  
    """
    user = models.ForeignKey('auth.User',
                             related_name='actions',
                             db_index=True,
                             on_delete=models.CASCADE)
    #Внешний ключ для модели ContentType
    target_ct = models.ForeignKey(ContentType,
                                  blank=True,
                                  null=True,
                                  related_name='target_obj',
                                  on_delete=models.CASCADE)
    
    #Поле хранящее идентификатор на связанный объект
    target_id = models.PositiveIntegerField(null=True,
                                            blank=True,
                                            db_index=True)
    #Поле для обращения к связанному объекту на основании его типа и id 
    target = GenericForeignKey('target_ct', 'target_id')
    verb = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True,
                                   db_index=True)
    
    class Meta:
        ordering = ('-created',)