import datetime
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from .models import Action


# Функция, позволяющая создавать записи о пользовательской активности
def create_action(user, verb, target=None):
    
    #Поиск похожего действия совершенного в течении последней минуты
    now = timezone.now()
    last_minute = now - datetime.timedelta(seconds=60)
    similiar_actions = Action.objects.filter(user_id=user.id, verb=verb, created__gte=last_minute)
    if target:
        target_ct = ContentType.objects.get_for_model(target)
        similiar_actions = similiar_actions.filter(target_ct=target_ct,
                                                   target_id=target.id)
    
    # Если похожее действие не найдено - создать новое
    if not similiar_actions:
        action = Action(user=user, verb=verb, target=target)
        action.save()
        return True
    return False
