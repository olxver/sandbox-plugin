FROM python:3.9-slim

# Set a working directory
WORKDIR /app

# Copy the docker-kill.py file
COPY docker-kill.py /app

# Update pip
RUN pip install -U pip

# Copy the requirements.txt file
COPY requirements.txt /app

# Install the Python dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Start the docker-kill.py script in the background
CMD ["python", "/app/docker-kill.py"]
