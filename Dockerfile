# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /home/site/wwwroot

# Copy the current directory contents into the container at /home/site/wwwroot
COPY . /home/site/wwwroot

# Install Node.js and npm to use PM2
RUN apt-get update && apt-get install -y nodejs npm

# Install PM2 to manage multiple processes
RUN npm install -g pm2

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose necessary ports
EXPOSE 8000 8501

# Run PM2 to start both Flask and Streamlit
CMD ["pm2-runtime", "start", "ecosystem.config.js"]
