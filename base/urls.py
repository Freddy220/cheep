from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('post/new/', views.new_post, name='new_post'),
    path('post/edit/<int:post_id>/', views.edit_post, name='edit_post'),
    path('post/delete/<int:post_id>/', views.delete_post, name='delete_post'),
    path('registro/', views.registro, name='registro'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),

    # Agregar ruta me gusta
    path('post/like/<int:post_id>/', views.like_post, name='like_post'),

    # Ruta post_detail
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),

    path('perfil/', views.perfil, name='perfil'),
    # URL para la vista home
    path('post/no_permission/', views.no_permission, name='no_permission'),

    # Rutas para API (usar vistas separadas)
    path('api/posts/', views.api_post_list, name='api_post_list'),
    path('api/posts/<int:post_id>/', views.api_post_detail, name='api_post_detail'),
    path('api/posts/<int:post_id>/like/', views.api_like_post, name='api_like_post'),
]





    



  
   






