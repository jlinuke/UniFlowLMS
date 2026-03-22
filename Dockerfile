FROM python:3.12-slim

# Prevent Python from writing .pyc files and buffering stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies specifically
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Collect static files for production to serve via WhiteNoise
# We pass a dummy SECRET_KEY so Django doesn't fail during build
RUN SECRET_KEY=django-insecure-docker-build-key python manage.py collectstatic --noinput

# Expose port and run Gunicorn (Evaluate Railway's dynamic $PORT)
EXPOSE 8000
CMD gunicorn uniflow_lms.wsgi:application --bind 0.0.0.0:$PORT
