from django.db.models.signals import post_save #importing post_save signal
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile
# post_save is a signal which is fired when an object is saved
# receiver is function that performs some task after receivng a signal
@receiver(post_save,sender=User)
def create_profile(sender,instance,created,**kwargs): # here our receiver is post_save
	if created: #
		Profile.objects.create(user=instance)
@receiver(post_save,sender=User)
def save_profile(sender,instance,**kwargs):
	instance.profile.save()

# After this , import this signal into ready function of users' app.py file