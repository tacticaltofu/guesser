from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Profile

from django.contrib.auth.models import User

from .forms import UserRegisterForm

# Create your views here.
def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			messages.success(request, f'Your account has been created! You can now login!')
			return redirect('login')
	else:
		form = UserRegisterForm()
	context = {'form': form}
	return render(request, 'users/register.html', context=context)

def profile(request, username):
	user = get_object_or_404(User, username=username)
	correct = [post.id for post in user.profile.correct.all()]
	attempted = [post.id for post in user.profile.attempted.all()]

	context = {
		'user': user,
		'num_correct': len(correct),
		'num_attempts': len(attempted),
	}
	return render(request, 'users/profile.html', context=context)

def leaderboard(request):
	profiles = Profile.objects.annotate(num_correct=Count('correct')).order_by('-num_correct')
	context = {
		'profiles': profiles,
	}
	return render(request, 'leaderboard.html', context=context)