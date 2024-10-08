from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import LoginForm
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required
from .models import Post, Like, Comment, CommentLike
from .forms import PostForm, CommentForm, BannerUploadForm, ProfilePictureUploadForm, StoryForm
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.shortcuts import redirect
from .models import FollowRequest, Story, EtiquetasPost
from django.db.models import Count
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.db.models import Q
import random
from django.contrib.auth.models import User
from .models import Message
from django.templatetags.static import static  
from .models import User  
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string


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
def upload_story(request):
    if request.method == 'POST':
        form = StoryForm(request.POST, request.FILES)
        if form.is_valid():
            story = form.save(commit=False)
            story.user = request.user
            story.save()
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'status': 'success', 'story_id': story.id})
            return redirect('nexly')
    return redirect('nexly')

@login_required
def nexly_view(request):
    if request.method == 'POST':
        if 'post_content' in request.POST:
            form = PostForm(request.POST, request.FILES)  # Agregar request.FILES para manejar los archivos
            if form.is_valid():
                post = form.save(commit=False)
                post.user = request.user

                # Guardar la imagen o video si están presentes
                if 'photo' in request.FILES:
                    post.photo = request.FILES['photo']
                elif 'video' in request.FILES:
                    post.video = request.FILES['video']

                post.save()

                # Obtener etiquetas desde el formulario (suponiendo que se envían en un campo llamado 'tags')
                etiquetas = request.POST.get('tags', '').split(',')
                for etiqueta in etiquetas:
                    etiqueta = etiqueta.strip()
                    if etiqueta:  # Evita etiquetas vacías
                        EtiquetasPost.objects.create(post=post, etiqueta=etiqueta)

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

        # Obtener las stories
        stories = Story.objects.order_by('-created_at')[:10]  # Muestra las últimas 10 stories

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return render(request, 'post_list.html', {'posts': posts})

        form = PostForm()
        comment_form = CommentForm()
        story_form = StoryForm()  # Añadido para pasar el formulario de historias al contexto

        return render(request, 'index.html', {
            'form': form,
            'comment_form': comment_form,
            'story_form': story_form,  # Pasar el formulario de historias
            'posts': posts,
            'show_following_posts': show_following_posts,
            'top_posts': top_posts,
            'stories': stories,
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


@login_required
def profile_view(request, nombre):
    # Verificar si el usuario existe
    user = get_object_or_404(User, nombre=nombre)
    
    # Obtener las publicaciones del usuario
    posts = Post.objects.filter(user=user).order_by('-created_at')

    # Contadores de seguimiento y publicaciones
    accepted_follow_requests_count = FollowRequest.objects.filter(
        to_user=user, is_accepted=True).count()
    followed_count = FollowRequest.objects.filter(
        from_user=request.user, is_accepted=True).count()
    posts_count = posts.count()

    # Verificar si el usuario actual sigue al perfil y si la solicitud ha sido aceptada
    is_following = FollowRequest.objects.filter(
        from_user=request.user, to_user=user, is_accepted=True).exists()

    if request.method == 'POST':
        if 'post_content' in request.POST:
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                post = form.save(commit=False)
                post.user = request.user
                post.image = request.FILES.get('image')  # Manejar imagen
                post.video = request.FILES.get('video')  # Manejar video
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
        elif 'update_profile_picture' in request.POST:
            profile_form = ProfilePictureUploadForm(request.POST, request.FILES, instance=request.user)
            if profile_form.is_valid():
                profile_form.save()
                return redirect('profile', nombre=nombre)
    else:
        form = PostForm()
        comment_form = CommentForm()
        banner_form = BannerUploadForm(instance=request.user)
        profile_form = ProfilePictureUploadForm(instance=request.user)

    # Obtener las URLs de las imágenes de perfil y banner del usuario
    profile_picture_url = user.profile_picture.url if user.profile_picture else None
    banner_picture_url = user.banner_picture.url if user.banner_picture else None

    # URL de la imagen de banner por defecto
    default_banner_url = static('images/default-banner.jpg')

    context = {
        'nombre': user.nombre,
        'iduserP': user.iduser,
        'posts': posts,
        'form': form,
        'comment_form': comment_form,
        'banner_form': banner_form,
        'profile_form': profile_form,
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
    
    if created:
        request.session['follow_request_message'] = 'Solicitud enviada exitosamente.'
    else:
        request.session['follow_request_message'] = 'Ya has enviado una solicitud este usuario.'
    
    return redirect(reverse('profile', args=[to_user.nombre]))
@require_POST
@login_required
def clear_follow_request_message(request):
    if 'follow_request_message' in request.session:
        del request.session['follow_request_message']
    return JsonResponse({'status': 'success'})

@login_required
def accept_follow_request(request, request_id):
    follow_request = get_object_or_404(FollowRequest, id=request_id, to_user=request.user)
    follow_request.is_accepted = True
    follow_request.save()
    
    # Guarda el mensaje en la sesión
    request.session['follow_request_message'] = 'Solicitud aceptada.'

    return redirect('follow_requests')

@login_required
def reject_follow_request(request, request_id):
    follow_request = get_object_or_404(FollowRequest, id=request_id, to_user=request.user)
    follow_request.delete()
    
    # Guarda el mensaje en la sesión
    request.session['follow_request_message'] = 'Solicitud rechazada.'

    return redirect('follow_requests')
@login_required
def follow_requests(request):
    # Obtener solicitudes de seguimiento pendientes
    follow_requests = FollowRequest.objects.filter(to_user=request.user, is_accepted=False)

    # Obtener los usuarios que el usuario ya sigue o que le han enviado una solicitud
    following_or_requested = FollowRequest.objects.filter(
        Q(from_user=request.user) | Q(to_user=request.user)
    ).values_list('to_user_id', 'from_user_id')

    following_or_requested_ids = [user_id for user_id, _ in following_or_requested]

    # Obtener 5 usuarios aleatorios que no estén en la lista anterior
    # Y contar cuántas solicitudes de seguimiento han sido aceptadas (es decir, seguidores)
    recommended_users = User.objects.exclude(
        Q(iduser__in=following_or_requested_ids) | Q(iduser=request.user.iduser)
    ).annotate(follower_count=Count('received_requests', filter=Q(received_requests__is_accepted=True))).order_by('?')[:5]

    return render(request, 'follow_requests.html', {
        'follow_requests': follow_requests,
        'recommended_users': recommended_users
    })

@require_POST
@login_required
def clear_follow_request_message(request):
    if 'follow_request_message' in request.session:
        del request.session['follow_request_message']
    return JsonResponse({'status': 'success'})

@login_required
def inbox(request):
    messages_received = Message.objects.filter(receiver=request.user)
    messages_sent = Message.objects.filter(sender=request.user)

    all_conversations = {}
    
    for message in messages_received:
        key = (message.sender.iduser, message.receiver.iduser)
        if key not in all_conversations or message.created_at > all_conversations[key]['last_message_time']:
            all_conversations[key] = {
                'user': message.sender,
                'last_message': message.content,
                'last_message_time': message.created_at,
                'is_sent': False
            }
    
    for message in messages_sent:
        key = (message.receiver.iduser, message.sender.iduser)
        if key not in all_conversations or message.created_at > all_conversations[key]['last_message_time']:
            all_conversations[key] = {
                'user': message.receiver,
                'last_message': message.content,
                'last_message_time': message.created_at,
                'is_sent': True
            }
    
    if 'q' in request.GET:
        query = request.GET['q']
        users = User.objects.filter(nombre__icontains=query).exclude(iduser=request.user.iduser)
    else:
        users = User.objects.exclude(iduser=request.user.iduser)

    context = {
        'conversations': sorted(all_conversations.values(), key=lambda x: x['last_message_time'], reverse=True),
        'users': users,
    }
    return render(request, 'inbox.html', context)


@login_required
def send_message(request, user_id):
    receiver = User.objects.get(id=user_id)

    if request.method == 'POST':
        content = request.POST.get('content')
        Message.objects.create(sender=request.user, receiver=receiver, content=content)
        return redirect('inbox')

    return render(request, 'send_message.html', {'receiver': receiver})

@login_required
def conversation(request, user_id):
    receiver = User.objects.get(iduser=user_id)
    messages = Message.objects.filter(sender=request.user, receiver=receiver) | Message.objects.filter(sender=receiver, receiver=request.user)
    messages = messages.order_by('created_at')

    if request.method == 'POST':
        content = request.POST.get('content')
        Message.objects.create(sender=request.user, receiver=receiver, content=content)
        return redirect('conversation', user_id=user_id)

    return render(request, 'conversation.html', {'receiver': receiver, 'messages': messages})