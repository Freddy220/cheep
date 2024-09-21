from django.contrib import admin
from .models import Post  # Cambiado a Post con mayúscula

# Aquí puedes registrar el modelo en el admin si aún no lo has hecho
admin.site.register(Post)


