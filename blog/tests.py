import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import datetime, timedelta
from django.utils import timezone
from blog.models import Author, Post, Comment


@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user():
    return User.objects.create_user(username="user1", password="pass1234")

@pytest.fixture
def user2():
    return User.objects.create_user(username="user2", password="pass1234")

@pytest.fixture
def author(user):
    return Author.objects.create(name="Author One", email="author1@example.com", user=user)

@pytest.fixture
def author2(user2):
    return Author.objects.create(name="Author Two", email="author2@example.com", user=user2)

@pytest.fixture
def post(author):
    return Post.objects.create(
        title="Post 1",
        content="Content 1",
        published_date=timezone.now(),
        author=author,
        status="published",
        active=True,
    )

@pytest.fixture
def inactive_post(author):
    return Post.objects.create(
        title="Inactive Post",
        content="Inactive Content",
        published_date=timezone.now(),
        author=author,
        status="published",
        active=False,
    )

@pytest.fixture
def jwt_token(user):
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)

@pytest.fixture
def jwt_client(api_client, jwt_token):
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")
    return api_client

@pytest.mark.django_db
def test_post_list_shows_only_active(api_client, post, inactive_post):
    response = api_client.get("/api/posts/")
    assert response.status_code == 200, "Post list API did not return 200 OK"
    data = response.json()
    post_ids = [p["id"] for p in data]
    assert post.id in post_ids, "Active post is missing from the list"
    assert inactive_post.id not in post_ids, "Inactive post should not appear in list"

@pytest.mark.django_db
def test_post_list_filter_by_date(api_client, post, author):
    Post.objects.create(
        title="Post 2",
        content="Content 2",
        published_date=timezone.now() - timedelta(days=5),
        author=author,
        status="published",
        active=True,
    )
    start_date = (timezone.now() - timedelta(days=1)).date()
    end_date = timezone.now().date()
    response = api_client.get(f"/api/posts/?published_date_after={start_date}&published_date_before={end_date}")
    assert response.status_code == 200, "Post list filtering by date failed"
    data = response.json()
    for p in data:
        pub_date = datetime.fromisoformat(p["published_date"].replace("Z",""))
        assert start_date <= pub_date.date() <= end_date, f"Post {p['id']} published date not in range"

@pytest.mark.django_db
def test_create_post_as_author(jwt_client, author):
    payload = {
        "title": "New Post",
        "content": "Test content",
        "published_date": timezone.now().isoformat(),
        "author": author.id
    }
    response = jwt_client.post("/api/posts/create/", payload, format='json')
    assert response.status_code == 201, "Failed to create post as author"
    data = response.json()
    assert data["title"] == "New Post", "Created post title mismatch"
    assert data["author"] == author.id, "Created post author mismatch"

@pytest.mark.django_db
def test_edit_post_as_author(jwt_client, post):
    payload = {"title": "Edited Title", "content": "Edited Content", "active": True}
    response = jwt_client.put(f"/api/posts/{post.id}/edit/", payload, format='json')
    assert response.status_code == 200, "Failed to edit post as author"
    post.refresh_from_db()
    assert post.title == "Edited Title", "Post title did not update"
    assert post.content == "Edited Content", "Post content did not update"

@pytest.mark.django_db
def test_delete_post_as_author(jwt_client, post):
    response = jwt_client.delete(f"/api/posts/{post.id}/delete/")
    assert response.status_code == 204, "Failed to delete post"
    post.refresh_from_db()
    assert post.active is False, "Post active field not set to False after delete"

@pytest.mark.django_db
def test_create_comment_logged_in(jwt_client, post):
    payload = {"post": post.id, "content": "Logged-in comment"}
    response = jwt_client.post("/api/comments/create/", payload, format='json')
    assert response.status_code == 201, "Failed to create comment as logged-in user"
    data = response.json()
    assert data["content"] == "Logged-in comment", "Comment content mismatch"

@pytest.mark.django_db
def test_create_comment_anonymous(api_client, post):
    payload = {"post": post.id, "content": "Anonymous comment"}
    response = api_client.post("/api/comments/create/", payload, format='json')
    assert response.status_code == 201, "Failed to create comment as anonymous user"
    data = response.json()
    assert data["content"] == "Anonymous comment", "Comment content mismatch"
