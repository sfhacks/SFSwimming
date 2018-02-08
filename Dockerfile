# Use an official Python runtime as a parent image
FROM python:3.6.2

# Set the working directory to /app
WORKDIR /code

# Copy the current directory contents into the container at /app
ADD . /code

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5000
