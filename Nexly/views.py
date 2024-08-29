from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import LoginForm
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required
from .models import Post, Like, Comment, CommentLike
from .forms import PostForm, CommentForm, BannerUploadForm  
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.shortcuts import redirect
from .models import FollowRequest
from django.db.models import Count

def login_view(request):
    form = LoginForm(data=request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            correo = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=correo, password=password)
            if user is not None:
                login(request, user)
                return redirect("nexly")
            else:
                form.add_error(None, "Correo o contraseña incorrectos")
    return render(request, "login.html", {"form": form})

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('nexly')
        else:
            print(form.errors)  # Esto te ayudará a ver cualquier error en el formulario
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def nexly_view(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('index')
    else:
        form = PostForm()
    
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'index.html', {'form': form, 'posts': posts})

def logout_view(request):
    logout(request)
    return redirect('login')  # Redirige al inicio de sesión después de cerrar sesión

@login_required
def nexly_view(request):
    if request.method == 'POST':
        if 'post_content' in request.POST:
            form = PostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.user = request.user
                post.save()
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({'status': 'success', 'post_id': post.id})
                return redirect('nexly')
        elif 'comment_content' in request.POST:
            post_id = request.POST.get('post_id')
            post = get_object_or_404(Post, id=post_id)
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.user = request.user
                comment.post = post
                comment.save()
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({'status': 'success', 'comment_id': comment.id})
                return redirect('nexly')

    elif request.method == 'GET':
        show_following_posts = request.GET.get('filter') == 'following'
        if show_following_posts:
            followed_users = FollowRequest.objects.filter(
                from_user=request.user, is_accepted=True).values_list('to_user_id', flat=True)
            posts = Post.objects.filter(user_id__in=followed_users).order_by('-created_at')
        else:
            posts = Post.objects.all().order_by('-created_at')

        # Obtener las 5 publicaciones más destacadas (con más likes)
        top_posts = Post.objects.annotate(like_count=Count('like')).order_by('-like_count')[:5]

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return render(request, 'post_list.html', {'posts': posts})

        form = PostForm()
        comment_form = CommentForm()

        return render(request, 'index.html', {
            'form': form,
            'comment_form': comment_form,
            'posts': posts,
            'show_following_posts': show_following_posts,
            'top_posts': top_posts,  # Añadido para pasar las publicaciones destacadas al contexto
        })
    
@login_required
def like_post(request, post_id):
    post = Post.objects.get(id=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        like.delete()
    return redirect('nexly')

@login_required
def share_post(request, post_id):
    original_post = get_object_or_404(Post, id=post_id)
    
    # Crear una nueva publicación como una copia de la publicación original
    shared_post = Post.objects.create(
        user=request.user,
        content=original_post.content,
        shared_post=original_post
    )
    
    return redirect('nexly')
@login_required
def share_post(request, post_id):
    post_to_share = get_object_or_404(Post, id=post_id)
    
    # Obtener la publicación original, si es una publicación compartida, de lo contrario usar la misma publicación
    original_post = post_to_share.get_original_post()
    
    # Crear una nueva publicación como una copia de la publicación original
    shared_post = Post.objects.create(
        user=request.user,
        content=original_post.content,
        original_post=original_post
    )
    
    return redirect('nexly')

@login_required
def like_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    like, created = CommentLike.objects.get_or_create(user=request.user, comment=comment)
    if not created:
        like.delete()
    return redirect('nexly')

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.user == request.user:
        post.delete()
    return redirect('nexly')

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        if post.user == request.user:
            content = request.POST.get('content')
            post.content = content
            post.save()
            return JsonResponse({'content': post.content})
    return JsonResponse({'error': 'Unauthorized'}, status=403)

from django.shortcuts import render, get_object_or_404
from .models import User  # Importa el modelo de usuario si es necesario

from django.templatetags.static import static  # Importar el tag static

@login_required
def profile_view(request, nombre):
    # Verificar si el usuario existe
    user = get_object_or_404(User, nombre=nombre)
    
    # Obtener las publicaciones del usuario
    posts = Post.objects.filter(user=user).order_by('-created_at')
    
    # Contador de solicitudes aceptadas (seguidores)
    accepted_follow_requests_count = FollowRequest.objects.filter(
        to_user=user, is_accepted=True).count()

    # Contador de seguidos por el usuario actual
    followed_count = FollowRequest.objects.filter(
        from_user=request.user, is_accepted=True).count()

    # Contador de publicaciones del usuario específico
    posts_count = posts.count()

    # Verificar si el usuario actual ya sigue al perfil y la solicitud ha sido aceptada
    is_following = FollowRequest.objects.filter(
        from_user=request.user, to_user=user, is_accepted=True).exists()

    if request.method == 'POST':
        if 'post_content' in request.POST:
            form = PostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.user = request.user
                post.save()
                return redirect('profile', nombre=nombre)
        elif 'comment_content' in request.POST:
            post_id = request.POST.get('post_id')
            post = get_object_or_404(Post, id=post_id)
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.user = request.user
                comment.post = post
                comment.save()
                return redirect('profile', nombre=nombre)
        elif 'unfollow' in request.POST:
            # Deshacer seguimiento
            FollowRequest.objects.filter(
                from_user=request.user, to_user=user, is_accepted=True).delete()
            return redirect('profile', nombre=nombre)
        elif 'update_banner' in request.POST:
            banner_form = BannerUploadForm(request.POST, request.FILES, instance=request.user)
            if banner_form.is_valid():
                banner_form.save()
                return redirect('profile', nombre=nombre)
    else:
        form = PostForm()
        comment_form = CommentForm()
        banner_form = BannerUploadForm(instance=request.user)

    # Obtener las URLs de las imágenes de perfil y banner del usuario
    profile_picture_url = user.profile_picture.url if user.profile_picture else None
    banner_picture_url = user.banner_picture.url if user.banner_picture else None

    # Agregar la URL de la imagen de banner por defecto
    default_banner_url = static('images/default-banner.jpg')

    context = {
        'nombre': user.nombre,
        'iduserP': user.iduser,
        'posts': posts,
        'form': form,
        'comment_form': comment_form,
        'banner_form': banner_form,
        'accepted_follow_requests_count': accepted_follow_requests_count,
        'followed_count': followed_count,
        'posts_count': posts_count,
        'is_following': is_following,
        'profile_pictureP': profile_picture_url,
        'banner_pictureP': banner_picture_url,
        'default_banner_url': default_banner_url,
    }
    return render(request, 'profile.html', context)

@login_required
def send_follow_request(request, user_id):
    to_user = get_object_or_404(User, iduser=user_id)
    follow_request, created = FollowRequest.objects.get_or_create(from_user=request.user, to_user=to_user)
    if not created:
        return JsonResponse({'error': 'Ya has enviado una solicitud a este usuario'}, status=400)
    return JsonResponse({'message': 'Solicitud enviada correctamente'})

@login_required
def accept_follow_request(request, request_id):
    follow_request = get_object_or_404(FollowRequest, id=request_id, to_user=request.user)
    follow_request.is_accepted = True
    follow_request.save()
    return JsonResponse({'message': 'Solicitud aceptada'})

@login_required
def reject_follow_request(request, request_id):
    follow_request = get_object_or_404(FollowRequest, id=request_id, to_user=request.user)
    follow_request.delete()
    return JsonResponse({'message': 'Solicitud rechazada'})
@login_required
def follow_requests(request):
    follow_requests = FollowRequest.objects.filter(to_user=request.user, is_accepted=False)
    return render(request, 'follow_requests.html', {
        'follow_requests': follow_requests
    })
