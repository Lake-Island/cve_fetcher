# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Explicitly copy the tools.txt file to /app
COPY tools.txt /app/tools.txt

# Install necessary packages
RUN apt-get update && \
    apt-get install -y gnupg cron && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Install Python dependencies
RUN pip install --no-cache-dir \
    requests \
    tinydb \
    python-dotenv \
    Flask \
    plotly \
    pandas

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Copy and set the entrypoint script
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# Run the entrypoint script
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
