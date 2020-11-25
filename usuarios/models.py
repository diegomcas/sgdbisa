"""
Modelos de la aplicación usuarios
"""
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwards):

    # Genera automaticamente el token de usuario cuando el usuario se crea.
    # Agrega automáticamente el usuario al grupo 'Dibujante'
    # https://www.django-rest-framework.org/api-guide/authentication/

    print(f'sender= {sender}')

    if created:
        Token.objects.create(user=instance)
        dibu_group = Group.objects.get(name='Operario Especialista')
        dibu_group.user_set.add(instance)
