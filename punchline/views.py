import random

from django.shortcuts import render, redirect, get_object_or_404

from django.views import generic
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib import messages

from django.contrib.auth.models import User

from punchline.models import Post, Response
from punchline.forms import GuessPunchlineForm

from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from similarity.similar import similar
# Create your views here.

def index(request):
	post_list = [post.id for post in Post.objects.all()]
	if request.user.is_authenticated:
		attempted = [post.id for post in request.user.profile.attempted.all()]
	else:
		attempted = request.session.get('attempt_id', [])
	unattempted_list = []
	for post_id in post_list:
		if post_id not in attempted:
			unattempted_list.append(post_id)

	if unattempted_list:
		return HttpResponseRedirect(reverse('guess', args=[random.choice(unattempted_list)]))
	else:
		messages.warning(request, 'You have guessed the punchline for every post! Time to create your own!')
		return HttpResponseRedirect(reverse('create_post'))

def guess(request, pk):
	post_to_guess = get_object_or_404(Post, pk=pk)

	if request.user.is_authenticated:
		correct = [post.id for post in request.user.profile.correct.all()]
		attempted = [post.id for post in request.user.profile.attempted.all()]
	else:
		correct = request.session.get('correct_id', [])
		attempted = request.session.get('attempt_id', [])

	answered_already = False
	for post_id in attempted:
		if post_id == pk:
			answered_already = True

	if post_to_guess.author == request.user:
		answered_already = True

	if request.method == 'POST':
		form = GuessPunchlineForm(request.POST)
		if form.is_valid():
			attempted.append(pk)
			if request.user.is_authenticated:
				request.user.profile.attempted.add(post_to_guess)
			else:
				request.session['attempt_id'] = attempted
			if similar(form.cleaned_data['punchline'], post_to_guess.punchline, 70):
				correct.append(pk)
				if request.user.is_authenticated:
					request.user.profile.correct.add(post_to_guess)
				else:
					request.session['correct_id'] = correct
				messages.success(request, 'Correct')
			else:
				messages.error(request, 'Incorrect')
			if request.user.is_authenticated:
				comment = Response.objects.create(post=post_to_guess, content=form.cleaned_data['punchline'], author=request.user)
			else:
				Response.objects.create(post=post_to_guess, content=form.cleaned_data['punchline'])
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
		if self.request.user.is_authenticated:
			attempted = [post.id for post in self.request.user.profile.attempted.all()]
		else:
			attempted = self.request.session.get('attempt_id', [])
		answered_already = False
		for post_id in attempted:
			if post_id == self.kwargs['pk']:
				answered_already = True
		if self.request.user == self.get_object().author:
			answered_already = True
		context['answered_already'] = answered_already
		return context

class PostCreate(LoginRequiredMixin, CreateView):
	model = Post
	fields = ['title', 'setup', 'punchline']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super(PostCreate, self).form_valid(form)

	def get_success_url(self):
		return reverse('post-detail', args=[self.object.id])

class PostUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Post
	fields = ['title', 'setup', 'punchline']

	def get_success_url(self):
		return reverse('post-detail', args=[self.object.id])

	def test_func(self):
		post = self.get_object()
		return self.request.user == post.author

class PostDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Post
	success_url = reverse_lazy('index')

	def test_func(self):
		post = self.get_object()
		return self.request.user == post.author