# 🎬 IMDB Clone API – Django REST Framework

This project is a movie review and watchlist REST API built with Django and Django REST Framework (DRF).
It allows users to browse movies, streaming platforms, post reviews, and authenticate securely using JWT.

The API is designed as a backend service that can be consumed by a frontend application (React, mobile app, etc.).

LIVE API DOCS - https://imdb-clone-904k.onrender.com

# 🚀 Features
🔐 Authentication

- User registration

- JWT authentication (access & refresh tokens)

- Token rotation and expiry handling

- Protected endpoints using IsAuthenticated

🎥 Streaming Platforms

- Create, retrieve, update, delete streaming platforms (admin-only)

- Each platform contains multiple movies/watchlists

📺 Watchlist (Movies)

- Create and manage movie watchlists

- Assign movies to streaming platforms

- Public movie listing

- Search movies by title or platform name

- Pagination support

⭐ Reviews & Ratings

- Authenticated users can review movies

- One review per user per movie

- Rating system (1–5)

- Automatic average rating calculation

- Retrieve reviews by:

  - Movie

  - User

- Update & delete reviews (owner-only)

🔒 Permissions & Safety

- Implemented TDD best practices for endpoints

- Admin-only write access for platforms and movies

- Review ownership enforcement

- Read-only access for unauthenticated users

- Validation for duplicate reviews

# 🧱 Tech Stack

- Python

- Django

- Django REST Framework

- PostgreSQL

- Simple JWT

# ⚙️ Installation & Setup

1️⃣ Clone the repository

- git clone https://github.com/jais380/IMDB-Clone.git

- cd IMDB-Clone

2️⃣ Create a virtual environment


- python -m venv venv

- source venv/bin/activate  or  On Windows: venv\Scripts\activate

3️⃣ Install dependencies


- pip install -r requirements.txt

4️⃣ Configure PostgreSQL

Update your DATABASES settings in settings.py:


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '<YOUR_DATABASE_NAME>',
        'USER': '<YOUR_USERNAME>',
        'PASSWORD': '<YOUR_PASSWORD>',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

5️⃣ Run migrations

- python manage.py makemigrations

- python manage.py migrate

6️⃣ Create superuser


- python manage.py createsuperuser

7️⃣ Run the server


- python manage.py runserver

# 🔑 Authentication Endpoints

Register


`POST /account/register/`

Obtain JWT Token


`POST /account/api/token/`

Refresh Token


`POST /account/api/token/refresh/`

Logout


`POST /account/logout/`

# 🎥 Streaming Platform Endpoints

| Method | Endpoint            | Description              |
| ------ | ------------------- | ------------------------ |
| GET    | `/api/stream/`      | List streaming platforms |
| POST   | `/api/stream/`      | Create platform (admin)  |
| GET    | `/api/stream/<id>/` | Retrieve platform        |
| PUT    | `/api/stream/<id>/` | Update platform (admin)  |
| DELETE | `/api/stream/<id>/` | Delete platform (admin)  |


# 📺 Watchlist (Movies) Endpoints

| Method | Endpoint           | Description          |
| ------ | ------------------ | -------------------- |
| GET    | `/api/watch/`      | List movies          |
| POST   | `/api/watch/`      | Create movie (admin) |
| GET    | `/api/watch/<id>/` | Retrieve movie       |
| PUT    | `/api/watch/<id>/` | Update movie (admin) |
| DELETE | `/api/watch/<id>/` | Delete movie (admin) |


⭐ Review Endpoints

| Method | Endpoint                              | Description              |
| ------ | ------------------------------------- | ------------------------ |
| GET    | `/api/<movie_id>/reviews/`            | List reviews for a movie |
| POST   | `/api/<movie_id>/review/create/`      | Create review (auth)     |
| GET    | `/api/review/<id>/`                   | Retrieve review          |
| PUT    | `/api/review/<id>/`                   | Update review (owner)    |
| DELETE | `/api/review/<id>/`                   | Delete review (owner)    |
| GET    | `/api/user/<username>/reviews/`       | Reviews by user          |


# 🧠 Business Rules

- One review per user per movie

- Ratings must be between 1 and 5

- Average rating updates automatically

- Only review owners can edit/delete

- Only admins can manage platforms and movies

# 📌 Future Improvements

- Better rating recalculation logic

- Favorites / watch later feature

- Comments on reviews

- Movie genres

- Frontend integration

- Docker support

# 👤 Author

Jude

Backend Developer (Django / DRF)

# 📜 License

This project is open-source and available under the MIT License.
