from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from blog.models import Author, Post, Comment
from django.utils import timezone
import random
from faker import Faker

fake = Faker()

class Command(BaseCommand):
    help = "Seed the database with initial data: users, authors, posts, comments"

    def handle(self, *args, **kwargs):
        user1, created = User.objects.get_or_create(username="user1")
        if created:
            user1.set_password("pass1234")
            user1.save()

        user2, created = User.objects.get_or_create(username="user2")
        if created:
            user2.set_password("pass1234")
            user2.save()

        author1, _ = Author.objects.get_or_create(
            user=user1, defaults={"name": "Author One", "email": "author1@example.com"}
        )
        author2, _ = Author.objects.get_or_create(
            user=user2, defaults={"name": "Author Two", "email": "author2@example.com"}
        )

        authors = [author1, author2]

        posts = []
        for i in range(100):
            author = random.choice(authors)
            post, created = Post.objects.get_or_create(
                title=fake.sentence(nb_words=6),
                author=author,
                defaults={
                    "content": fake.paragraph(nb_sentences=5),
                    "published_date": fake.date_time_between(start_date="-1y", end_date="now", tzinfo=timezone.get_current_timezone()),
                    "status": random.choice(["draft", "published"]),
                    "active": True,
                }
            )
            posts.append(post)

        for post in posts:
            num_comments = random.randint(1, 5)
            for _ in range(num_comments):
                user = random.choice([user1, user2, None])  # None = anonymous
                Comment.objects.get_or_create(
                    post=post,
                    content=fake.sentence(nb_words=12),
                    user=user
                )

        self.stdout.write(self.style.SUCCESS("Database seeded successfully with 100 posts and comments!"))
