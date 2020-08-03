from datetime import datetime

from django.test import TestCase

from punchline.models import Post, Response
from django.contrib.auth.models import User
# Create your tests here.

class PostModelTest(TestCase):
	@classmethod
	def setUpTestData(cls):
		setup = 'A giant fly has attacked the local police...'
		punchline = 'Police have called the SWAT team.'
		Post.objects.create(title=setup, setup=setup, punchline=punchline)

		setup = 'It is hard to say what my wife does...'
		punchline = 'She sells seashells by the seashore.'
		author = User.objects.create(username='kevin')
		Post.objects.create(title=setup, setup=setup, punchline=punchline, author=author)

		user = User.objects.create(username='bob')

	def test_title_max_length(self):
		post = Post.objects.get(id=1)
		max_length = post._meta.get_field('title').max_length
		self.assertEquals(max_length, 100)

	def test_punchline_max_length(self):
		post = Post.objects.get(id=1)
		max_length = post._meta.get_field('punchline').max_length
		self.assertEquals(max_length, 100)

	def test_no_author(self):
		post = Post.objects.get(id=1)
		self.assertEquals(post.author, None)

	def test_correct_author(self):
		post = Post.objects.get(id=2)
		self.assertEquals(post.author, User.objects.get(username='kevin'))

	def test_incorrect_author(self):
		post = Post.objects.get(id=2)
		self.assertFalse(post.author == User.objects.get(username='bob'))

	def test_score(self):
		post = Post.objects.get(id=1)
		self.assertEquals(post.score, 0)

	def test_date_posted(self):
		post = Post.objects.get(id=1)
		self.assertEquals(post.date_posted.date(), datetime.today().date())

	def test_get_absolute_url(self):
		post = Post.objects.get(id=1)
		self.assertEquals(post.get_absolute_url(), '/punchline/post/1/')

class ResponseModelTest(TestCase):
	@classmethod
	def setUpTestData(cls):
		setup = 'A giant fly has attacked the local police...'
		punchline = 'Police have called the SWAT team.'
		Post.objects.create(title=setup, setup=setup, punchline=punchline)

		content = 'Unfortunately the SWAT team was not there.'
		response = Response.objects.create(post=Post.objects.get(id=1), content=content)

		author = User.objects.create(username='bob')
		content = 'But they could not SWAT it away.'
		response = Response.objects.create(post=Post.objects.get(id=1), content=content, author=author)

		author = User.objects.create(username='jim')

	def test_no_author(self):
		response = Response.objects.get(id=1)
		self.assertEquals(response.author, None)

	def test_correct_author(self):
		response = Response.objects.get(id=2)
		self.assertEquals(response.author, User.objects.get(username='bob'))

	def test_incorrect_author(self):
		response = Response.objects.get(id=2)
		self.assertFalse(response.author == User.objects.get(username='jim'))

	def test_score(self):
		response = Response.objects.get(id=1)
		self.assertEquals(response.score, 0)

	def test_date_posted(self):
		response = Response.objects.get(id=1)
		self.assertEquals(response.date_posted.date(), datetime.today().date())