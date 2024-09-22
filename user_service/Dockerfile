FROM python:3.11


# Set the working directory
WORKDIR /app

# Copy the application code
COPY . /app

# Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Apply database migrations
# RUN python manage.py makemigrations && python manage.py migrate

# Set environment variable
ENV PYTHONUNBUFFERED=1

# Expose the desired port
EXPOSE 8000

# Use Gunicorn with wait-for-it
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]
