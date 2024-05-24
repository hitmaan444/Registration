from django.db.models.signals import pre_save, post_save, pre_delete
from .models import User,Profile
from django.dispatch import receiver


@receiver(pre_save, sender=User)
def create_profile(sender, instance, **kwargs):

    print('signal test created')
    profile = Profile.objects.create()
    instance.profile = profile




