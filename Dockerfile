# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install Node.js and npm to use PM2
RUN apt-get update && apt-get install -y nodejs npm

# Install PM2 to manage multiple processes
RUN npm install -g pm2

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose necessary ports
EXPOSE 8000 8501

# Copy PM2 configuration file
COPY ecosystem.config.js /app/ecosystem.config.js

# Run PM2 to start both Flask and Streamlit
CMD ["pm2-runtime", "start", "ecosystem.config.js"]
