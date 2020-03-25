from django.contrib.contenttypes.models import ContentType
from .models import Action

#Позволяет создавать пользовательскую активность 
def create_action(user, verb, target=None):
    action = Action(user=user, verb=verb, target=target)
    action.save()