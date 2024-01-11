# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8000 for Gunicorn
EXPOSE 8000

# Command to run your application using Gunicorn
CMD ["gunicorn", "-c", "gunicorn_conf.py", "-b", "0.0.0.0:8000", "src.main:app"]
