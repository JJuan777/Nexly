from django.contrib import admin
from .models import User, Post, Like, Comment, CommentLike, FollowRequest

class UserAdmin(admin.ModelAdmin):
    list_display = ('iduser', 'correo', 'nombre', 'profile_picture', 'is_admin', 'is_active')
    search_fields = ('correo', 'nombre')
    list_filter = ('is_admin', 'is_active')
    ordering = ('correo',)
    filter_horizontal = ()

class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'content', 'created_at')
    search_fields = ('user__correo', 'content')
    list_filter = ('created_at',)
    ordering = ('-created_at',)

class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created_at')
    search_fields = ('user__correo', 'post__id')
    list_filter = ('created_at', 'post')
    ordering = ('-created_at',)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'post', 'content', 'created_at')
    search_fields = ('user__correo', 'post__id', 'content')
    list_filter = ('created_at', 'post')
    ordering = ('-created_at',)

class CommentLikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'comment', 'created_at')
    search_fields = ('user__correo', 'comment__id')
    list_filter = ('created_at', 'comment')
    ordering = ('-created_at',)

class FollowRequestAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'to_user', 'created_at', 'is_accepted')
    search_fields = ('from_user__correo', 'to_user__correo')
    list_filter = ('created_at', 'is_accepted')
    ordering = ('-created_at',)

admin.site.register(User, UserAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(CommentLike, CommentLikeAdmin)
admin.site.register(FollowRequest, FollowRequestAdmin)
