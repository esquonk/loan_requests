# coding: utf-8
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from oauth2_provider.models import Application


def create_auth_client(sender, instance=None, created=False, **kwargs):
    """
    Creates client_id and client_secret for authenticated users
    """
    if created:
        Application.objects.create(user=instance,
                                   client_type=Application.CLIENT_CONFIDENTIAL,
                                   authorization_grant_type=Application.GRANT_PASSWORD)


post_save.connect(create_auth_client, sender=User)
