FROM python:3.11

# Install FFmpeg
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    apt-get clean

# Set the working directory and copy files to it
WORKDIR /SUBERATOR
COPY . /SUBERATOR

# Install dependencies from txt file
RUN pip install -r requirements.txt

# Expose the port the app runs on
EXPOSE 5000

# Command to run your Flask application. tells Docker how to run flask app
CMD ["python", "app.py"]
