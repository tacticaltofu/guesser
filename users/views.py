from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

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
	correct = request.session.get('correct_id', [])
	attempted = request.session.get('attempt_id', [])
	context = {
		'num_correct': len(correct),
		'num_attempts': len(attempted),
	}
	return render(request, 'users/profile.html', context=context)