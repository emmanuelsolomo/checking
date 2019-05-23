from django.contrib.auth.signals import user_logged_in
from django.core.signals import request_finished
from django.dispatch import receiver
from netsoul.auth_helper import _auth_completed, store_user

@receiver(user_logged_in)
def on_login(sender, user, request, **kwargs):
    print('User just logged in....')




#request_finished.connect(_auth_completed)
