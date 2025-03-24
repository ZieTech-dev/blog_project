from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('article/create/', views.create_article, name='create_article'),
    path('article/<int:article_id>/', views.article_detail, name='article_detail'),
    path('like/<int:article_id>/', views.like_article, name='like_article'),
    path('article/<int:article_id>/favorite/', views.favorite_article, name='favorite_article'),
    path('profile/', views.user_profile, name='profile'),
    path('check-notifications/', views.check_notifications, name='check_notifications'),
    path('mark-notifications-read/', views.mark_notifications_read, name='mark_notifications_read'),
    path('search-suggestions/', views.search_suggestions, name='search_suggestions'),
    path('article/<int:article_id>/comments/', views.article_comments, name='article_comments'),  # Nouvelle route
    path('article/<int:article_id>/comment/', views.add_comment, name='add_comment'),
]