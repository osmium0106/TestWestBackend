# TestWestBackend

TestWestBackend is a Django-based backend for managing educational questions, supporting a hierarchical structure (Grade > Subject > Chapter > Topic > Subtopic > Question) and advanced features like bulk upload, tagging, and JWT authentication. The project is ready for both local and Dockerized development, and exposes a REST API for integration with frontend clients.

## Database Structure

The database is organized as follows:

- **Grade**: Represents a school grade (e.g., 6th, 7th, 8th).
- **Subject**: Linked to a Grade. (e.g., Mathematics, Science)
- **Chapter**: Linked to a Subject. (e.g., Algebra, Biology)
- **Topic**: Linked to a Chapter. Has a `tag` field (Foundation/Advanced).
- **Subtopic**: Linked to a Topic. (e.g., "Definition of a Set")
- **Question**: Linked to a Subtopic. Fields:
  - `text`: The question text
  - `question_type`: MCQ, MSQ, Short, Long
  - `difficulty`: Easy, Medium, Hard
  - `option_a`, `option_b`, `option_c`, `option_d`: Options for MCQ/MSQ
  - `correct_answer`: For MCQ (a/b/c/d), for MSQ (comma-separated, e.g., a,b,d)
  - `explanation`: Text explanation for the answer

## Features
- JWT authentication for secure API access
- Bulk upload of questions via admin (with downloadable Excel template)
- Advanced filtering and search for questions
- CORS enabled for frontend integration
- Swagger/OpenAPI documentation at `/swagger/`
- Admin interface for all models at `/admin/`

## How to Run This Project

### 1. Using Docker (Recommended)

**Prerequisites:**
- Docker and Docker Compose installed

**Steps:**
1. Clone the repository and navigate to the project directory.
2. Build and start the containers:
   ```powershell
   docker compose up --build -d
   ```
3. Apply migrations:
   ```powershell
   docker compose exec web python manage.py migrate
   ```
4. Create a superuser (for admin access):
   ```powershell
   docker compose exec web python manage.py createsuperuser
   ```
5. Access the app:
   - Admin: http://localhost:8000/admin/
   - API docs: http://localhost:8000/swagger/
   - Bulk upload: Use the admin interface for questions

### 2. Running Locally Without Docker

**Prerequisites:**
- Python 3.11+
- PostgreSQL (or use SQLite by editing `core/settings.py`)

**Steps:**
1. Clone the repository and navigate to the project directory.
2. (Optional but recommended) Create and activate a virtual environment:
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   ```
3. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
4. Set up your database in `core/settings.py` (default is PostgreSQL; you can switch to SQLite for quick testing).
5. Apply migrations:
   ```powershell
   python manage.py migrate
   ```
6. Create a superuser:
   ```powershell
   python manage.py createsuperuser
   ```
7. Run the development server:
   ```powershell
   python manage.py runserver
   ```
8. Access the app:
   - Admin: http://localhost:8000/admin/
   - API docs: http://localhost:8000/swagger/

## Bulk Upload Template
- Download the sample Excel template from the admin bulk upload page or at `/api/questions/download-template/`.
- Use `subtopic_name` (not ID) to link questions to subtopics.
- Fill in options and correct answers for MCQ/MSQ only; leave blank for short/long.

## API Endpoints
- All endpoints are under `/api/` (see Swagger docs for details)
- JWT login: `/api/user/login/`
- Questions CRUD and bulk upload: `/api/questions/questions/` and `/api/questions/questions/bulk_upload/`

## Notes
- CORS is enabled for `http://localhost:5173` (for frontend integration)
- PostgreSQL is used by default in Docker; you can switch to SQLite for local quick tests
- All models are available in the Django admin for manual management

---
This backend is ready for integration with any frontend and supports scalable question management for educational platforms.