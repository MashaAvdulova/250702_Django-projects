from django.db.models.signals import post_save, post_delete
from .models import Profile
from django.dispatch import receiver
from django.contrib.auth.models import User

# @receiver(post_save, sender=Profile)
# def profile_update(sender, instance, created, **kwargs):
#     print('Profile saved')
#     print('Instance', instance)
#     print('Created', created)

# @receiver(post_save, sender=Profile)
def create_profile(sender, instance, created, **kwargs):
    print('Profile saved')
    if created:
        user = instance
        profile = Profile.object.create(
            user = user,
            username = user.username,
            email = user.email,
            name = user.First_name,
        )

# @receiver(post_delete, sender=Profile)
# def profile_delete(sender, instance, **kwargs):
#     print('Delete user>>>')

# @receiver(post_delete, sender=Profile)
def delete_user(sender, instance, **kwargs):
    user = instance.user
    user.delete()


# вместо вызова функций можно используем декторатор
post_save.connect(create_profile, sender=Profile)
post_delete.connect(delete_user, sender=Profile)