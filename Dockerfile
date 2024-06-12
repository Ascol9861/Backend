# Use an official Python runtime as a parent image
FROM python:3.9

# Set environment variables
ENV DB_HOST='34.30.91.14'
ENV DB_NAME='postgres'
ENV DB_USER='postgres'
ENV DB_PASSWORD='root'

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt flask-cors

# Make port 80 available to the world outside this container
EXPOSE 80

# Run app.py when the container launches
CMD ["python", "app.py"]
