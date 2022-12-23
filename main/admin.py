from django.contrib import admin
from .models import Post, Music
from review.models import Comment


class CommentInline(admin.TabularInline):
    model = Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ['title',]
    list_filter = ['title',]
    search_fields = ['title',]
    inlines = [CommentInline]


admin.site.register(Post, PostAdmin)
admin.site.register(Music)
