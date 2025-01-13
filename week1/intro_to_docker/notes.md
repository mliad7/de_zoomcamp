### Build an Image

```cmd
docker build -t <image_name> .
```

### Starts a new container from the specified image.

```cmd
docker run -it <image-name>
```

Explanation

- `docker run`: Starts a new container from the specified image.
- `-i`: Keeps the container's standard input (STDIN) open, even if you're not attached to the container.
- `-t`: Allocates a pseudo-TTY (terminal interface), making it interactive.
- `<image-name>`: The name or ID of the Docker image to use.

### Dockerfile Creation

```dockerfile
# Use an official base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose a port
EXPOSE 5000

# Command to run the application
CMD ["python", "app.py"]
```

