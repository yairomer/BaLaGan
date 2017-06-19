# Use an official Python runtime as a base image
FROM python:2.7-slim

# install systems packages
RUN apt-get update && \
    apt-get install -y -qq \
        python-virtualenv

# Install python packages
COPY requirements.txt /root/
RUN pip install -U pip && \
    pip install -r /root/requirements.txt

# Set the working directory
WORKDIR /app
ADD . /app

# Make port 80 available to the world outside this container
EXPOSE 80

# Run app.py when the container launches
CMD ["python", "app.py"]
