from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Author, Post, Comment
from .serializers import (
    AuthorSerializer,
    AuthorCreateUpdateSerializer,
    PostListSerializer,
    PostDetailSerializer,
    PostCreateSerializer,
    PostEditSerializer,
    CommentCreateSerializer,
)
from .permissions import IsAuthorOwner
from .filters import PostFilter


class AuthorListAPI(generics.ListAPIView):
    serializer_class = AuthorSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['name', 'email']

    def get_queryset(self):
        if self.request.user.is_staff:
            return Author.objects.all()
        return Author.objects.filter(user=self.request.user)


class AuthorCreateAPI(generics.CreateAPIView):
    serializer_class = AuthorCreateUpdateSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]


class AuthorDetailAPI(generics.RetrieveAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsAuthorOwner]


class AuthorUpdateAPI(generics.UpdateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorCreateUpdateSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsAuthorOwner]


class AuthorDeleteAPI(generics.DestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsAuthorOwner]


class PostListAPI(generics.ListAPIView):
    queryset = Post.objects.filter(active=True)
    serializer_class = PostListSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.AllowAny]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = PostFilter
    search_fields = ['title', 'content', 'author__name']
    ordering_fields = ['published_date', 'title', 'author__name']
    ordering = ['-published_date']


class PostDetailAPI(generics.RetrieveAPIView):
    queryset = Post.objects.filter(active=True)
    serializer_class = PostDetailSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.AllowAny]


class PostCreateAPI(generics.CreateAPIView):
    serializer_class = PostCreateSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]


class PostEditAPI(generics.UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostEditSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]


class PostDeleteAPI(generics.DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def perform_destroy(self, instance):
        if instance.author.user != self.request.user:
            raise PermissionDenied("You can only delete your own posts.")
        instance.active = False
        instance.save()


class CommentCreateAPI(generics.CreateAPIView):
    serializer_class = CommentCreateSerializer
    permission_classes = [permissions.AllowAny]
