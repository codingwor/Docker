# Base image: official lightweight Python 3.11 image (Debian-slim variant)
# Everything you build is layered ON TOP of this image
FROM python:3.11-slim

# Sets the working directory inside the container.
# All subsequent commands (COPY, RUN, CMD) run relative to this path.
# If the folder doesn't exist, Docker creates it.
WORKDIR /app

# Copy requirements.txt from your local machine into the container's /app folder
# Done BEFORE copying the rest of the code intentionally (explained below)
COPY requirements.txt .

# Run pip install during the BUILD process (not at runtime)
# --no-cache-dir keeps the image smaller by not storing pip's download cache
RUN pip install --no-cache-dir -r requirements.txt

# Now copy the rest of your application code into /app
COPY . .

# Documents that the container listens on port 5000
# This is purely informational/documentation — does NOT actually publish the port
EXPOSE 5000

# The command that runs when the container STARTS (not during build)
# This keeps the container alive and running your app
CMD ["python", "app.py"]