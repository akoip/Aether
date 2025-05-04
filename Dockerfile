
# Dockerfile to build assistant container
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose any required ports
EXPOSE 5000

# Run the assistant script
CMD ["python", "assistant.py"]
