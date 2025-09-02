from django.contrib import admin
from .models import Author, Post, Comment


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "user")


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "status", "active", "published_date")
    list_filter = ("status", "active", "published_date")
    search_fields = ("title", "content")
    ordering = ("-published_date",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("post", "user", "created")
    list_filter = ("created",)
    search_fields = ("content",)
