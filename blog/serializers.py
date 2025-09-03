from rest_framework import serializers
from .models import Author, Post, Comment


class AuthorSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Author
        fields = ["id", "name", "email", "user"]


class AuthorCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["name", "email"]

    def create(self, validated_data):
        request = self.context.get("request")
        if request is None:
            raise serializers.ValidationError("Request context is missing")
        return Author.objects.create(user=request.user, **validated_data)


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "content", "user", "created"]


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["post", "content"]

    def validate(self, data):
        post = data.get("post")
        if not post.active:
            raise serializers.ValidationError("Cannot comment on inactive posts.")
        return data

    def create(self, validated_data):
        request = self.context.get("request")

        if request is None:
            raise serializers.ValidationError("Request context is missing")
        
        user = request.user if request.user.is_authenticated else None
        return Comment.objects.create(user=user, **validated_data)


class PostListSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source="author.name", read_only=True)

    class Meta:
        model = Post
        fields = ["id", "title", "content", "published_date", "author_name"]


class PostDetailSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source="author.name", read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "content",
            "published_date",
            "author_name",
            "status",
            "active",
            "comments",
        ]


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["title", "content", "published_date", "author"]

    def validate_author(self, value):
        request = self.context.get("request")
        if request is None:
            raise serializers.ValidationError("Request context is missing")
        
        if value.user != request.user:
            raise serializers.ValidationError("You can only post as your own author profile.")
        return value


class PostEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["title", "content", "active"]

    def validate(self, data):
        request = self.context.get("request")
        if request is None:
            raise serializers.ValidationError("Request context is missing")
        
        if self.instance is None:
            raise serializers.ValidationError("Instance is missing")
        
        if self.instance.author.user != request.user:
            raise serializers.ValidationError("You can only edit your own posts.")
        return data
