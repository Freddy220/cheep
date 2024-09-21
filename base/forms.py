# base/forms.py

from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']  # Incluye los campos a quieras editar
#Este formulario utiliza el modelo Post y permitirá editar los campos title y content
#El formulario genera automáticamente los inputs de HTML basados en estos campos.