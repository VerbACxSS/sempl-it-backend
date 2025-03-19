FROM bitnami/python:3.12.8

# Move in server folder
WORKDIR /server

# Copy requirements.txt and install all dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy all files in server directory
COPY . .

# Expose server port
EXPOSE 30010

# Run FastAPI application
CMD ["uvicorn", "app.app:app", "--host=0.0.0.0"]
