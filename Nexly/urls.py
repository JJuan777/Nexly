from django.urls import path
from .views import login_view, register_view, nexly_view, logout_view, like_post, share_post, like_comment, delete_post, edit_post
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', nexly_view, name='nexly'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('like/<int:post_id>/', like_post, name='like_post'),
    path('share/<int:post_id>/', share_post, name='share_post'),
    path('like_comment/<int:comment_id>/', like_comment, name='like_comment'),
    path('delete_post/<int:post_id>/', delete_post, name='delete_post'),
    path('edit-post/<int:post_id>/', edit_post, name='edit_post'),
    path('profile/<str:nombre>/', views.profile_view, name='profile'),
    path('send_follow_request/<int:user_id>/', views.send_follow_request, name='send_follow_request'),
    path('accept_follow_request/<int:request_id>/', views.accept_follow_request, name='accept_follow_request'),
    path('reject_follow_request/<int:request_id>/', views.reject_follow_request, name='reject_follow_request'),
    path('follow_requests/', views.follow_requests, name='follow_requests'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
