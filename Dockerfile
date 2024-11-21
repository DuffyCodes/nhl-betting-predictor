# Use a lightweight Python 3.9 base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install dependencies
RUN pip install mysql-connector-python pandas scikit-learn xgboost python-dotenv beautifulsoup4 matplotlib seaborn

# Copy all application code to the container
COPY . /app/

# Expose the application port
EXPOSE 5000

# Start the application
CMD ["python", "main.py"]
