import random

from django.shortcuts import render, redirect, get_object_or_404

from django.views import generic
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

from punchline.models import Post, Response
from punchline.forms import GuessPunchlineForm

# Create your views here.

def index(request):
	num_posts = Post.objects.all().count()
	return HttpResponseRedirect(reverse('guess', args=[random.randint(1, num_posts)]))

def guess(request, pk):
	post_to_guess = get_object_or_404(Post, pk=pk)

	correct = request.session.get('correct_id', [])
	attempted = request.session.get('attempt_id', [])

	answered_already = False
	for post_id in attempted:
		if post_id == pk:
			answered_already = True

	if request.method == 'POST':
		form = GuessPunchlineForm(request.POST)
		if form.is_valid():
			attempted.append(pk)
			request.session['attempt_id'] = attempted
			if form.cleaned_data['punchline'] == post_to_guess.punchline:
				correct.append(pk)
				request.session['correct_id'] = correct
				messages.success(request, f'Correct')
			else:
				messages.error(request, f'Incorrect')
			comment = Response.objects.create(post=post_to_guess, content=form.cleaned_data['punchline'])
			return HttpResponseRedirect(reverse('post-detail', args=[pk]))
	else:
		form = GuessPunchlineForm()
	context = {
		'post_to_guess': post_to_guess,
		'form': form,
		'num_correct': len(correct),
		'num_attempts': len(attempted),
		'answered_already': answered_already
	}

	return render(request, 'guess.html', context=context)

class PostDetailView(generic.DetailView):
	model = Post

	def get_context_data(self, **kwargs):
		context = super(PostDetailView, self).get_context_data(**kwargs)
		attempted = self.request.session.get('attempt_id', [])
		answered_already = False
		for post_id in attempted:
			if post_id == self.kwargs['pk']:
				answered_already = True
		context['answered_already'] = answered_already
		return context