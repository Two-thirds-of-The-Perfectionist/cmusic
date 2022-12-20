from django.contrib import admin
from .models import Post, Music, PlayList
from review.models import Comment, PostLike, PostFavorite, CommentLike


class CommentInline(admin.TabularInline):
    model = Comment


class PostLikeInline(admin.TabularInline):
    model = PostLike


class PostFavoriteInline(admin.TabularInline):
    model = PostFavorite


class CommentLikeInLine(admin.TabularInline):
    model = CommentLike


class PostAdmin(admin.ModelAdmin):
    list_display = ['title',]
    list_filter = ['post',]
    search_fields = ['like_filter', 'post_filter']
    inlines = [CommentInline]


admin.site.register(Post, PostAdmin)
admin.site.register(Music)
admin.site.register(PlayList)
admin.site.register(PostFavorite)
# admin.site.register(Post)




