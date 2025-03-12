# Use Python as the base image
FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django project files
COPY . .

# Set environment variables for Django
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

# Collect static files
RUN python manage.py collectstatic --noinput

# Start Django server
CMD gunicorn --bind 0.0.0.0:8080 LargeEnglish.wsgi:application
