# Use Python 3.10-slim to ensure compatibility with TensorFlow versions
FROM python:3.10-slim

# Upgrade pip to the latest version
RUN pip install --upgrade pip

# Set environment variables
ENV PYTHONBUFFERED True
ENV APP_HOME /app

# Set working directory
WORKDIR $APP_HOME

# Copy application files
COPY . ./

# Install requirements with TensorFlow fallback
RUN pip install -r requirements.txt || \
    (sed -i 's/tensorflow-intel==2.17.0/tensorflow==2.17.0/' requirements.txt && pip install -r requirements.txt)

# Default command to run the application
CMD ["python", "app.py"]
