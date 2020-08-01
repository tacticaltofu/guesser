from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

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

def profile(request):
	if request.user.is_authenticated:
		correct = [post.id for post in request.user.profile.correct.all()]
		attempted = [post.id for post in request.user.profile.attempted.all()]
	else:
		correct = request.session.get('correct_id', [])
		attempted = request.session.get('attempt_id', [])
	context = {
		'num_correct': len(correct),
		'num_attempts': len(attempted),
	}
	return render(request, 'users/profile.html', context=context)

def userprofile(request, username):
	user = User.objects.get(username=username)
	correct = [post.id for post in user.profile.correct.all()]
	attempted = [post.id for post in user.profile.attempted.all()]
	context = {
		'num_correct': len(correct),
		'num_attempts': len(attempted),
	}
	return render(request, 'users/profile.html', context=context)