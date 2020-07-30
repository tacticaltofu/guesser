from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('post/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
	path('post/<int:pk>/guess/', views.guess, name='guess'),
]