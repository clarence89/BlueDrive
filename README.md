# BlueDrive

## Features

1. REST API for Posts, Comments, and Authors
2. JWT Authentication (login, refresh)
3. Filtering, searching, and ordering of posts
4. Docker support (dev & prod)
5. Database seeding for easy testing
6. Postman collection for manual testing
7. Pagination support
8. Swagger API docs

---

## Setup

Clone the repository:

```bash
git clone https://github.com/clarence89/BlueDrive.git
cd BlueDrive
```

Create a `.env` file:

```env
DATABASE_NAME=bluedrive
DATABASE_USER=bluedrive_user
DATABASE_PASSWORD=bluedrive_pass
DATABASE_HOST=db
DATABASE_PORT=5432

SECRET_KEY=supersecretkey
DEBUG=True
ALLOWED_HOSTS=*

SIMPLE_JWT_ACCESS_TOKEN_LIFETIME=5
SIMPLE_JWT_REFRESH_TOKEN_LIFETIME=1
```

---

## Docker

### Dev

```bash
docker-compose up --build
docker compose up --build
```

- Access: [http://localhost:8000](http://localhost:8000)
- Debug port: `5678` (debugpy)

---

## Database Migration and Seeding

Apply migrations:

```bash
docker-compose run web python manage.py migrate
docker compose run web python manage.py migrate
```

Seed the database:

```bash
docker-compose run web python manage.py initial_seed
docker compose run web python manage.py initial_seed
```

> Seeds default users, authors, and posts. You can extend the command to generate 100 posts/comments.

---

## Running the Project

For dev (with hot reload and debug):

```bash
docker-compose up
```

---

## Testing

Run tests with pytest:

```bash
docker-compose run web pytest
```

> Ensure `pytest-django` is installed.

---

## Postman Collection

- [BlueDrive Postman Collection](https://thealphadevs.postman.co/workspace/Team-Workspace~9bf3e20a-c514-4036-8bc4-192264d2700c/collection/29014621-deaf2dcc-f21d-4b12-99b5-d0d6af391643?action=share&creator=29014621&active-environment=29014621-23f2205f-0008-49f4-8469-3ab65363d106)

### Login Script for Postman

---

## API Endpoints

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/api/token/` | POST | No | Get JWT token |
| `/api/token/refresh/` | POST | No | Refresh JWT token |
| `/api/posts/` | GET | Optional | List active posts (filters: title, author_name, published_date) |
| `/api/posts/<id>/` | GET | Optional | Post detail with nested comments |
| `/api/posts/create/` | POST | Required | Create post (author only) |
| `/api/posts/<id>/edit/` | PUT | Required | Edit post (author only) |
| `/api/posts/<id>/delete/` | DELETE | Required | Delete post (author only, sets `active=False`) |
| `/api/comments/create/` | POST | Optional | Create comment on a post (user optional) |
| `/api/authors/` | GET, POST | Optional/Required | List or create authors |
| `/api/authors/<id>/edit/` | PUT | Required | Edit author info |
| `/api/authors/<id>/delete/` | DELETE | Required | Delete author |

---

## Notes

1. **Swagger** is available at `/swagger/` (if `drf-yasg` installed) for API docs.
2. **Seeding** is required for initial testing.
3. **Pagination** is applied on post lists for performance.
