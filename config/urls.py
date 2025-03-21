from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.contrib.auth import views as auth_views
from blog.views import logout_view

urlpatterns += [
    # path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('login/', auth_views.LoginView.as_view(
        template_name='blog/login.html',
        redirect_authenticated_user=True,  # Évite la reconnexion si déjà connecté
        next_page='profile'  # Redirige vers /profile/ après connexion
    ), name='login'),
    path('logout/', logout_view, name='logout'),
]