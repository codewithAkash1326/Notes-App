# Notes-App
# Notes Management API

A professional, production-ready backend for a Notes Management application built with **FastAPI**, **SQLAlchemy ORM**, and **PostgreSQL**. This project features secure JWT authentication, collaborative note sharing, and an advanced archiving system.

## 🚀 Features

### 🔐 Authentication & Security
*   **User Registration & Login**: Secure password hashing using `pwdlib`.
*   **JWT Authentication**: Stateless authentication with expiration and secure token management.
*   **Granular Authorization**: Strict ownership checks for all sensitive operations.

### 📝 Note Management
*   **Full CRUD**: Create, read, update, and delete personal notes.
*   **Archive System**: 
    *   Owners can archive notes to hide them from the main list.
    *   Archived notes are automatically hidden from collaborators.
    *   Restore functionality to bring notes back to active status.
*   **Note Sharing**: Collaborative features allowing users to share notes with others via email.

### 🛠 Technical Architecture
*   **Dependency Injection**: Utilizes FastAPI's DI system for database sessions and authentication helpers.
*   **Database Migrations**: Integrated with Alembic for version-controlled schema updates.
*   **Configuration Management**: Uses Pydantic Settings for environment-based configuration (`.env`).

## 🛠 Tech Stack

*   **Framework**: FastAPI
*   **Database**: PostgreSQL
*   **ORM**: SQLAlchemy
*   **Migrations**: Alembic
*   **Auth**: JWT (PyJWT) & pwdlib
*   **Validation**: Pydantic v2

## 🏁 Getting Started

### Prerequisites
*   Python 3.9+
*   PostgreSQL

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd notes-app
   ```

2. **Set up Environment Variables**:
   Create a `.env` file in the root directory:
   ```env
   DB_URL=postgresql://user:password@localhost:5432/notes_db
   TOKEN_SECRET_KEY=your_super_secret_key
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run Migrations**:
   ```bash
   alembic upgrade head
   ```

5. **Start the Server**:
   ```bash
   uvicorn main:app --reload
   ```

## 📖 API Documentation
Once the server is running, you can access the interactive documentation:
*   **Swagger UI**: `http://127.0.0.1:8000/docs`
*   **ReDoc**: `http://127.0.0.1:8000/redoc`

## 👤 Author
**Akash Chaudhary** - akashchaudhary48898@gmail.com
