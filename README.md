# 📌 Project Name
Django + Celery + RabbitMQ + Docker + Keycloak

A **scalable Django backend** with **Celery** for background tasks, **Redis** as a message broker, and **Docker Compose** for containerized deployment.

---

## 📖 Features
✅ Django-based backend  
✅ Celery for background tasks  
✅ RabbitMQ for message queuing  
✅ Docker Compose for easy deployment  
✅ Keycloak for user management  
✅ PostgreSQL as the database  

---

## 🛠 Installation Guide

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/notmhmd/django-jobs.git
cd django-jobs
```

---

### 2️⃣ Setup Environment Variables
Create a `.env` file in the root directory:

```env
# Database
POSTGRES_DB=mydatabase
POSTGRES_USER=myuser
POSTGRES_PASSWORD=mypassword
POSTGRES_HOST=db
POSTGRES_PORT=5432
DATABASE_URL:=postgres


# RabbitMQ (for Celery)
CELERY_BROKER_URL=amqp://guest:guest@rabbitmq:5672/

# Django
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=True
DJANGO_ENV: "development"


# Keycloak
KEYCLOAK_SERVER_URL=http://keycloak:8080
KEYCLOAK_REALM=myrealm
KEYCLOAK_CLIENT_ID=client-id
KEYCLOAK_CLIENT_SECRET=client-secret

# File Storage
USE_AWS=True (if you are an AWS fanboy)
USE_GCS=True (if you are Google fanboy)
```

---

### 3️⃣ Run the Project with Docker
Ensure **Docker** and **Docker Compose** are installed. Then, run:

```bash
docker-compose up --build
```

This will start:
- **Django App** (on `http://localhost:8000/`)
- **RabbitMQ** (on `5672`)
- **KeyCloak** (on `8080`)
- **Celery Worker** (for background tasks)

---

## 📂 Project Structure
```
django-jobs/
│── DjangoJobs/          # Django Project
│   ├── settings/        # Django Settings
│   ├── celery.py        # Celery Configuration
│   ├── urls.py          # URL Configuration
│   ├── wsgi.py          # WSGI Application
│
│── candidates/          # Candidate App
│── docker-compose.yml   # Docker Compose Config
│── Dockerfile           # Dockerfile
│── requirements.txt     # Dependencies
│── README.md            # This file
│── .env.example         # Example Environment Variables
```

---

## 📦 Running Celery Tasks
You can **manually trigger a Celery task** using the Django shell:

```bash
docker-compose exec django_app python manage.py shell
```
```python
from candidate.tasks import register_candidate_task
register_candidate_task.delay()
```

---

## 🚀 Deployment
For **production**, modify the `.env` file:
- Set `DJANGO_DEBUG=False`
- Use **AWS S3** or **GCS** for file storage
- Secure database credentials

Then, run:

```bash
docker-compose up --build -d
```

---

## 🐛 Troubleshooting
❌ **Database Connection Error?**  
Ensure PostgreSQL is running:  
```bash
docker-compose ps
```

❌ **Celery Not Running?**  
Restart the worker manually:
```bash
docker-compose restart celery_worker
```

❌ **Migrations Not Applied?**  
Run:
```bash
docker-compose exec django_app python manage.py migrate
```

---

## 🎯 Conclusion
This setup ensures a **scalable**, **containerized**, and **background task-enabled** Django project. 🚀

💡 **Need Help?** Open an issue or contact me! 😊
