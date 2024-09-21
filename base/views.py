from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from .forms import PostForm  # Importa el formulario
from django.http import HttpResponseForbidden
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import PostSerializer


def no_permission(request):
    return render(request, 'no_permission.html')


def new_post(request):
    if request.method == 'POST':
        Post.objects.create(
            title=request.POST.get('title'),
            content=request.POST.get('content'),
            author=request.user  # Asegúrate de que se guarde el autor del post
        )
        return redirect('home')
    return render(request, 'ejemplo.html')


def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.author != request.user:
        return render(request, 'no_permission.html', {'message': 'No tienes permiso para editar este post'})

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirige a la página de inicio u otra vista
    else:
        form = PostForm(instance=post)

    return render(request, 'edit_post.html', {'form': form, 'post': post})


def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        post.delete()
        return redirect('home')
    return render(request, 'delete_post.html', {'post': post})


def perfil(request):
    return render(request, 'perfil.html')


def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '¡Registro exitoso! Bienvenido.')
            return redirect('perfil')
    else:
        form = UserCreationForm()
    return render(request, 'registration/registro.html', {'form': form})


def home(request):
    posts = Post.objects.all().order_by('-created_at')  # Obtener todos los posts ordenados por fecha
    return render(request, 'home.html', {'posts': posts})


# Vistas para la funcionalidad normal
@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return redirect('post_detail', post_id=post_id)


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'post_detail.html', {
        'post': post,
        'like_count': post.like_count()  # Pasar el conteo de likes
    })


# Vistas para la API (separadas de las vistas normales)
@api_view(['GET', 'PUT', 'DELETE'])
def api_post_detail(request, post_id):
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PostSerializer(post)
        return Response(serializer.data)

    elif request.method == 'PUT':
        if request.user != post.author:
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        if request.user != post.author:
            return Response(status=status.HTTP_403_FORBIDDEN)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def api_like_post(request, post_id):
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return Response({'likes': post.likes.count()})


@api_view(['GET'])
def api_post_list(request):
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)
