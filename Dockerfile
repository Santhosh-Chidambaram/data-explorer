# Use the official Python 3.12 slim image
FROM python:3.12.8-slim

# Set the working directory inside the container
WORKDIR /data-explorer

# Copy the requirements file to the container
COPY ./requirements.txt /data-explorer/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r /data-explorer/requirements.txt

# Copy the application code to the container
COPY ./app /data-explorer/app

# Copy the app templates
COPY ./templates /data-explorer/templates

# Expose port 80 for the application
EXPOSE 80

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
