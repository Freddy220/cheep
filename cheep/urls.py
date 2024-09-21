from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static

urlpatterns =[
    path('admin/',admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
     path('accounts/login/', auth_views.LoginView.as_view(), name='login'),  # Ruta de login
    path('',include('base.urls')),# Incluye las URLs de la app 'base
    
]


# Agrega las siguientes líneas para servir archivos de medios durante el desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)