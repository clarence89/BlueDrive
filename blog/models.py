from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Author(models.Model):
    name = models.CharField(max_length=100)
    # Should i make this nullable? as per assessment in CreateApi of Post it should be using author_name and not author_id
    email = models.EmailField(unique=True)
    # Different Pen Names? if it is then good. if not should be onetoone? i'll stick with the requirements
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = "Author"
        verbose_name_plural = "Authors"

    def __str__(self):
        return self.name


class Post(models.Model):
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("published", "Published"),
    ]

    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="posts")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="draft")
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        ordering = ["-published_date"]
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["active"]),
            models.Index(fields=["-published_date"]),
        ]

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
        ordering = ["-created"]
        indexes = [
            models.Index(fields=["-created"]),
        ]

    def __str__(self):
        return f"Comment by {self.user or 'Anonymous'} on {self.post.title[:20]}"
