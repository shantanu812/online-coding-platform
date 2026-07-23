# Online Coding Platform

A robust backend service for an online code judging platform. This platform enables users to solve algorithmic problems, participate in contests, and view their rankings on a leaderboard. The system includes a secure, multi-language execution engine to compile and run submitted code against hidden test cases.

## 🚀 Features

*   **Multi-Language Judge:** Compiles and executes code submissions in C++, Java, and Python using dedicated executors.
*   **Contest Management:** Allows creation and management of coding contests.
*   **Leaderboard System:** Tracks user performance and generates competitive leaderboards.
*   **Problem & Test Case Handling:** Full CRUD support for coding problems and their associated test cases.
*   **Authentication:** Secure user registration and login using JWT-based authentication.
*   **Resource Monitoring:** Built-in resource monitoring to ensure submitted code does not exceed time or memory limits.

## 🛠️ Tech Stack

*   **Framework:** Python backend structure designed for a modern API framework like FastAPI.
*   **ORM & Database Migrations:** Uses Alembic for database migrations and schema versioning.
*   **Architecture:** Utilizes a Repository-Service pattern for clean separation of concerns.

## 📁 Project Structure

*   `backend/app/api/`: Contains all REST API routing and versioned endpoints.
*   `backend/app/auth/`: Handles secure JWT generation and password hashing.
*   `backend/app/database/`: Manages database connection setup and active sessions.
*   `backend/app/judge/`: The core execution engine containing the compiler, comparator, and language-specific executors.
*   `backend/app/models/`: Database models representing Users, Problems, Submissions, Contests, and Test Cases.
*   `backend/app/repositories/`: Data access layer handling direct database queries.
*   `backend/app/schemas/`: Data validation models and API payload definitions.
*   `backend/app/services/`: Business logic layer orchestrating data flow between the API and database repositories.

## ⚙️ Local Setup

**1. Clone the repository**
```bash
git clone https://github.com/shantanu812/online-coding-platform.git
cd online-coding-platform/backend
```

**2. Set up environment variables**
Copy the example environment file and configure your local database and API credentials:
```bash
cp .env.example .env
```

**3. Install dependencies**
Install all required Python packages from the requirements file:
```bash
pip install -r requirements.txt
```

**4. Run Database Migrations**
Initialize your database schema to match the current models using Alembic:
```bash
alembic upgrade head
```

**5. Start the Server**
Launch the backend application from the main entry point:
```bash
python main.py
```

## 🔒 Requirements for Code Execution
To ensure the judge module functions correctly locally, ensure your host machine has the necessary system compilers and runtimes installed for the supported languages:
*   `g++` (for C++ execution)
*   `javac` and `java` (for Java execution)
*   `python3` (for Python execution)