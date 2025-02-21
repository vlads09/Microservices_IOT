# Use an official Python image as the base image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the application when the container starts
CMD ["python", "adapter.py"]
