from django.contrib import admin
from .models import Post, Comment, Teg


class CommentInLine(admin.TabularInline):
    model = Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    list_filter = ('status', 'teg', 'created', 'publish', 'author')
    search_fields = ('title', 'body', 'teg')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    ordering = ('-status', '-publish')
    inlines = [CommentInLine]
# admin.site.register(Post)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')


@admin.register(Teg)
class Teg(admin.ModelAdmin):
    search_fields = ('teg',)
