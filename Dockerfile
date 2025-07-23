# Use a Python base image
FROM python:3.9-slim

# Set working directory inside the container
WORKDIR /app

# Copy everything from your local project folder into the container
COPY . /app

# Install required Python packages
RUN pip install --upgrade --no-cache-dir --use-deprecated=legacy-resolver -r requirements.txt

# Set default command to run prediction (adjust if needed)
CMD ["python", "predict.py"]