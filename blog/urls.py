from django.urls import path
from .views import (
    AuthorListAPI,
    AuthorCreateAPI,
    AuthorDetailAPI,
    AuthorUpdateAPI,
    AuthorDeleteAPI,
    PostListAPI,
    PostDetailAPI,
    PostCreateAPI,
    PostEditAPI,
    PostDeleteAPI,
    CommentCreateAPI,
)

urlpatterns = [
    path("authors/", AuthorListAPI.as_view(), name="api_author_list"),
    path("authors/create/", AuthorCreateAPI.as_view(), name="api_author_create"),
    path("authors/<int:pk>/", AuthorDetailAPI.as_view(), name="api_author_detail"),
    path("authors/<int:pk>/edit/", AuthorUpdateAPI.as_view(), name="api_author_update"),
    path("authors/<int:pk>/delete/", AuthorDeleteAPI.as_view(), name="api_author_delete"),

    path("posts/", PostListAPI.as_view(), name="api_post_list"),
    path("posts/create/", PostCreateAPI.as_view(), name="api_post_create"),
    path("posts/<int:pk>/", PostDetailAPI.as_view(), name="api_post_detail"),
    path("posts/<int:pk>/edit/", PostEditAPI.as_view(), name="api_post_edit"),
    path("posts/<int:pk>/delete/", PostDeleteAPI.as_view(), name="api_post_delete"),

    path("comments/create/", CommentCreateAPI.as_view(), name="api_comment_create"),
]
