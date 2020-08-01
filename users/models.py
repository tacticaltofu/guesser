from django.db import models
from punchline.models import Post
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	bio = models.TextField(max_length=500, null=True, blank=True)
	correct = models.ManyToManyField(Post, related_name='correct', null=True, blank=True)
	attempted = models.ManyToManyField(Post, related_name='attempted', null=True, blank=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
	instance.profile.save()