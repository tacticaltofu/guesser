from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('post/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
	path('post/<int:pk>/guess/', views.guess, name='guess'),
	path('post/create/', views.PostCreate.as_view(), name='create_post'),
	path('post/<int:pk>/update/', views.PostUpdate.as_view(), name='update_post'),
	path('post/<int:pk>/delete/', views.PostDelete.as_view(), name='delete_post'),
]