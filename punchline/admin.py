from django.contrib import admin
from .models import Post, Response
from users.models import Profile

# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
	list_display = ('short_title', 'author', 'date_posted', 'score')

@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
	list_display = ('short_content', 'author', 'date_posted', 'score')

admin.site.register(Profile)
