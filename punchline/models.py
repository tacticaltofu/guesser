from django.db import models
from django.urls import reverse
from django.template.defaultfilters import truncatechars
from django.contrib.auth.models import User

# Create your models here.

class Post(models.Model):
	title = models.CharField(max_length=100)
	setup = models.TextField()
	punchline = models.CharField(max_length=100)
	score = models.IntegerField(default=0)
	author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	date_posted = models.DateTimeField(auto_now_add=True)
	
	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('post-detail', args=[str(self.id)])

	@property
	def short_title(self):
		return truncatechars(self.title, 30)
	
	@property
	def short_punchline(self):
		return truncatechars(self.punchline, 30)

class Response(models.Model):
	post = models.ForeignKey('Post', on_delete=models.SET_NULL, null=True)
	content = models.CharField(max_length=100)
	score = models.IntegerField(default=0)
	author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	date_posted = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.content

	@property
	def short_content(self):
		return truncatechars(self.content, 30)

	class Meta:
		ordering = ['-date_posted']