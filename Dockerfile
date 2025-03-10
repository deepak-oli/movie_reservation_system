# Dockerfile
FROM python:3.10

# Set work directory
WORKDIR /code

COPY requirements.txt . 
# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . /code/

# Development-specific dependencies
ARG INSTALL_DEBUGPY=false
RUN if [ "$INSTALL_DEBUGPY" = "true" ]; then pip install debugpy; fi