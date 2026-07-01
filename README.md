# AltisOneLabz LMS API

Backend API for Learning Management System (LMS) — Mentor Dashboard & Admin Panel.

Built with FastAPI, SQLAlchemy, and MySQL.

## Tech Stack

- Python 3.11+
- FastAPI
- SQLAlchemy ORM
- MySQL
- JWT Authentication (python-jose)
- Passlib + Bcrypt

## Project Structure
app/
├── api/          # Dependencies (get_current_user, require_admin, require_mentor)
├── core/         # Security (JWT, password hashing)
├── database/     # Database connection & config
├── models/       # SQLAlchemy models
├── routers/      # API endpoints (auth, mentor, admin)
├── schemas/      # Pydantic schemas
├── services/     # Business logic
├── utils/        # Pagination
└── main.py

## Installation

1. Clone the repository
```bash
git clone https://github.com/username/repo-name.git
cd repo-name
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Copy environment variables
```bash
cp .env.example .env
```

4. Fill in `.env` with your values

## Environment Variables
DATABASE_URL=mysql+pymysql://user:password@localhost:3306/dbname
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRED_MINUTES=30
REFRESH_TOKEN_EXPIRED_DAYS=7

## Database Setup

Run your MySQL server, create a database, then run the app once — SQLAlchemy will auto-create all tables.

```sql
CREATE DATABASE lms_db;
```

## Running the Application

```bash
uvicorn main:app --reload
```

API will be available at `http://localhost:8000`

Swagger documentation at `http://localhost:8000/docs`

## API Documentation

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /auth/login | Login (returns access & refresh token) |
| POST | /auth/refresh | Get new access token |
| GET | /auth/me | Get current user info |

### Mentor Dashboard
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /mentor/students | Get students assigned to mentor |
| GET | /mentor/assignments | Get mentor's assignments |
| POST | /mentor/assignments | Create new assignment |
| GET | /mentor/submissions | Get submissions to review |
| PATCH | /mentor/submissions/{id} | Grade & review submission |

### Admin Panel
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /admin/mentors | Get all mentors |
| POST | /admin/mentors | Create new mentor |
| PUT | /admin/mentors/{id} | Update mentor |
| DELETE | /admin/mentors/{id} | Delete mentor |
| GET | /admin/dashboard | Get dashboard statistics |

## Default Credentials

Buat admin pertama langsung lewat database:
```sql
INSERT INTO users (name, email, password, role) 
VALUES ('Admin', 'admin@lms.com', '<bcrypt-hashed-password>', 'admin');
```

## Bonus Features

- Pagination — semua endpoint GET support `?page=1&limit=10`
- Role-based Dependencies — `require_admin` dan `require_mentor` di `api/deps.py`
