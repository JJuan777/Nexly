from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Post
from .models import Comment
from .models import Story

class LoginForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}))

class RegisterForm(UserCreationForm):
    nombre = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}))
    correo = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo'}))
    profile_picture = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('nombre', 'correo', 'password1', 'password2', 'profile_picture')


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': '¿Qué estás pensando?'})
        }
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escribe un comentario...'})
        }

class BannerUploadForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['banner_picture']

class ProfilePictureUploadForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['profile_picture']

class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ['image']