# Todo List API

A RESTful API built with FastAPI, designed to allow users to manage their personal to-do lists. This project is developed to practice backend development skills, inspired by the roadmap.sh project, and utilizes SQLite for data persistence.

## 🎯 Project Overview

This project provides a complete solution for user authentication and managing to-do items. It serves as a practical application of FastAPI for building robust and efficient backend services.

## 🚀 Features

- **User Authentication**: Secure user registration and login using JWT tokens
- **Todo Management**: Create, read, update, and delete (CRUD) operations for personal to-do items
- **User Management**: Basic user profile functionalities
- **SQLite Database**: Lightweight and easy-to-use database for data storage
- **FastAPI**: Leveraging FastAPI's speed, automatic documentation, and developer-friendly features

## 🛠️ Tech Stack

- **Framework**: FastAPI
- **Database**: SQLite
- **ORM**: SQLModel
- **Authentication**: PyJWT, Passlib (with bcrypt)
- **Development Tools**: Ruff, pre-commit

## 📁 Project Structure

```
├── app/
│   ├── api/                  # API routes and dependencies
│   │   ├── deps.py           # Dependency injection for DB sessions and authentication
│   │   ├── main.py           # Main API router setup
│   │   └── routes/           # Individual API endpoint definitions
│   │       ├── items.py      # Endpoints for managing to-do items
│   │       ├── login.py      # Endpoints for user authentication (login/token)
│   │       └── users.py      # Endpoints for user-related operations
│   ├── core/                 # Core application utilities
│   │   ├── db.py             # Database connection and session handling
│   │   └── security.py       # Security-related functions (password hashing, JWT)
│   ├── crud.py               # CRUD operations for database models
│   ├── models.py             # Database models (SQLModel) for users and items
│   └── main.py               # Main FastAPI application instance
├── pyproject.toml            # Project metadata and dependencies
├── README.md
└── uv.lock
```

## 🚦 Getting Started

### Prerequisites

- Python 3.12+
- `uv` (recommended package manager)

### Installation

1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd todo-list-api
   ```

2. **Install dependencies**:
   ```bash
   uv sync
   ```

3. **Install development dependencies (optional)**:
   ```bash
   uv sync --group dev
   ```

### Running the Application

1. **Start the development server**:
   ```bash
   uv run fastapi dev app/main.py
   ```
   The API will be accessible at `http://localhost:8000`.

2. **Access API Documentation**:
   - Interactive Swagger UI: `http://localhost:8000/docs`
   - ReDoc: `http://localhost:8000/redoc`
   - Scalar: `http://localhost:8000/scalar`


## 📚 API Endpoints

### Authentication
- `POST /token` - Login and get access token (OAuth2 password flow)

### User Management
- `POST /users/` - Register a new user

### Todo Items (Todos)
- `GET /todos/` - Get all todo items for current user (with pagination: `skip` and `limit` parameters)
- `POST /todos/` - Create a new todo item
- `GET /todos/{id}` - Get a specific todo item by UUID
- `PATCH /todos/{id}` - Update a todo item by UUID
- `DELETE /todos/{id}` - Delete a todo item by UUID

### Authentication Requirements

Most endpoints require authentication via Bearer token:
- All `/todos/*` endpoints require a valid JWT token
- The `/users/` POST endpoint (registration) is public
- The `/token` endpoint is used to obtain the JWT token

### Request/Response Examples

**Create a new user:**
```json
POST /users/
{
  "email": "user@example.com",
  "password": "securepassword"
}
```

**Login to get token:**
```json
POST /token
Content-Type: application/x-www-form-urlencoded

username=user@example.com&password=securepassword
```

**Create a todo:**
```json
POST /todos/
Authorization: Bearer <your-jwt-token>
{
  "title": "Learn FastAPI",
  "description": "Complete the FastAPI tutorial"
}
```

## 🔧 Development

### Code Quality

This project uses Ruff for linting and formatting:

```bash
# Run linting
uv run ruff check

# Run formatting
uv run ruff format

# Fix auto-fixable issues
uv run ruff check --fix
```

### Pre-commit Hooks

Install pre-commit hooks for automatic code quality checks:

```bash
uv run pre-commit install
```

## 🗄️ Database

The application uses SQLite as the database with SQLModel as the ORM. The database file will be created automatically when you first run the application.

### Models

- **User**: User account information with email and hashed password
- **Item**: Todo items linked to users with UUID identifiers

## 🔐 Security

- Passwords are hashed using bcrypt via Passlib
- JWT tokens for stateless authentication
- Input validation with Pydantic models
- SQL injection protection via SQLModel ORM
- User-specific data isolation (users can only access their own todos)

## 📝 License

This project is open source and available under the [MIT License](LICENSE).


## 📖 Learning Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)
- [roadmap.sh Backend Developer Roadmap](https://roadmap.sh/backend)
- [Project Idea](https://roadmap.sh/projects/todo-list-api)

---

**Note**: This project was developed as a learning exercise to practice backend development skills.
