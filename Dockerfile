FROM python:3.10
LABEL authors="notmhmd"

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate && gunicorn DjangoJobs.wsgi:application --workers=4 --threads=4 --bind 0.0.0.0:8000"]