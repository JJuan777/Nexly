from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings
from datetime import datetime, timezone, timedelta

class UserManager(BaseUserManager):
    def create_user(self, nombre, correo, password=None):
        if not correo:
            raise ValueError("El usuario debe tener un correo electrónico")
        user = self.model(correo=self.normalize_email(correo), nombre=nombre)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, nombre, correo, password=None):
        user = self.create_user(nombre=nombre, correo=correo, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    iduser = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    correo = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)  # Campo para la imagen de perfil
    banner_picture = models.ImageField(upload_to='banner_pictures/', null=True, blank=True)  # Campo para la imagen de banner

    objects = UserManager()

    USERNAME_FIELD = 'correo'
    REQUIRED_FIELDS = ['nombre']

    def __str__(self):
        return self.correo

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to='post_images/', null=True, blank=True)
    video = models.FileField(upload_to='post_videos/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    original_post = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='reposts')

    def __str__(self):
        if self.original_post:
            return f'{self.user.nombre} compartió un post de {self.original_post.user.nombre}'
        return f'Post by {self.user.nombre} on {self.created_at}'

    def get_original_post(self):
        if self.original_post:
            return self.original_post.get_original_post()
        return self

    def time_since_posted(self):
        now = datetime.now(timezone.utc)
        diff = now - self.created_at

        if diff < timedelta(minutes=1):
            return "hace un momento"
        elif diff < timedelta(hours=1):
            minutes = diff.seconds // 60
            return f"hace {minutes} minutos"
        elif diff < timedelta(days=1):
            hours = diff.seconds // 3600
            return f"hace {hours} horas"
        elif diff < timedelta(days=2):
            return "hace 1 día"
        else:
            days = diff.days
            return f"hace {days} días"
        
class EtiquetasPost(models.Model):
    etiqueta = models.CharField(max_length=50)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='etiquetas')

    def __str__(self):
        return self.etiqueta

class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f'Like by {self.user.nombre} on Post {self.post.id}'

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.nombre} on Post {self.post.id}'

    def time_since_commented(self):
        now = datetime.now(timezone.utc)
        diff = now - self.created_at

        if diff < timedelta(minutes=1):
            return "hace un momento"
        elif diff < timedelta(hours=1):
            minutes = diff.seconds // 60
            return f"hace {minutes} minutos"
        elif diff < timedelta(days=1):
            hours = diff.seconds // 3600
            return f"hace {hours} horas"
        elif diff < timedelta(days=2):
            return "hace 1 día"
        else:
            days = diff.days
            return f"hace {days} días"

class CommentLike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'comment')

    def __str__(self):
        return f'Like by {self.user.nombre} on Comment {self.comment.id}'
    
class FollowRequest(models.Model):
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_requests', on_delete=models.CASCADE)
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='received_requests', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_accepted = models.BooleanField(default=False)

    class Meta:
        unique_together = ('from_user', 'to_user')

    def __str__(self):
        return f'Solicitud de {self.from_user.nombre} a {self.to_user.nombre}'
    
class Story(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='stories/', null=True, blank=True)  # Campo para la imagen del story
    created_at = models.DateTimeField(auto_now_add=True)  # Fecha de creación

    def __str__(self):
        return f'Story de {self.user.nombre} creado el {self.created_at}'
    
    def time_since_posted(self):
        now = datetime.now(timezone.utc)
        diff = now - self.created_at

        if diff < timedelta(minutes=1):
            return "hace un momento"
        elif diff < timedelta(hours=1):
            minutes = diff.seconds // 60
            return f"hace {minutes} minutos"
        elif diff < timedelta(days=1):
            hours = diff.seconds // 3600
            return f"hace {hours} horas"
        elif diff < timedelta(days=2):
            return "hace 1 día"
        else:
            days = diff.days
            return f"hace {days} días"
        
class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Mensaje de {self.sender.nombre} a {self.receiver.nombre} el {self.created_at}'

    def time_since_sent(self):
        now = datetime.now(timezone.utc)
        diff = now - self.created_at

        if diff < timedelta(minutes=1):
            return "hace un momento"
        elif diff < timedelta(hours=1):
            minutes = diff.seconds // 60
            return f"hace {minutes} minutos"
        elif diff < timedelta(days=1):
            hours = diff.seconds // 3600
            return f"hace {hours} horas"
        elif diff < timedelta(days=2):
            return "hace 1 día"
        else:
            days = diff.days
            return f"hace {days} días"