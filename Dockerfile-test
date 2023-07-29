# Install Python
FROM python:3.10-slim

# Set working directory
WORKDIR /app
ENV PYTHONPATH=/app
ENV DATABASE_URL="postgresql://postgres:12345@db/restaurant"

# Install dependencies
COPY requirements.txt /app/

# Set environment variables
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /app/


EXPOSE 8000

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]