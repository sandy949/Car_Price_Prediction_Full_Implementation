# Use official Python 3.11 base image
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy requirements first (for layer caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files
COPY . .

# Expose port (adjust if your app uses a different one)
EXPOSE 5000

# Run the app (ensure backend/app.py is the actual entry point)
CMD ["python", "backend/app.py"]
