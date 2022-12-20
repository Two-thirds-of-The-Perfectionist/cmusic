from django.contrib import admin
from .models import Post, Music, PlayList
from review.models import Comments, PostLikes, PostFavorites, CommentsLikes


class CommentsInline(admin.TabularInline):
    model = Comments


class PostLikesInline(admin.TabularInline):
    model = PostLikes


class PostFavoritesInline(admin.TabularInline):
    model = PostFavorites


class CommentsLikesInLine(admin.TabularInline):
    model = CommentsLikes


class PostAdmin(admin.ModelAdmin):
    list_display = ['title',]
    list_filter = ['post',]
    search_fields = ['like_filter', 'post_filter']
    inlines = [CommentsInline]


admin.site.register(Post, PostAdmin)
admin.site.register(Music)
admin.site.register(PlayList)
admin.site.register(PostFavorites)
# admin.site.register(Post)




