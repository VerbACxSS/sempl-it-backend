FROM bitnami/python:3.12.8

# Move in server folder
WORKDIR /server

# Copy requirements.txt and install all dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy all files in server directory
COPY . .

# Run FastAPI application
CMD ["uvicorn", "app.app:app", "--host=0.0.0.0", "--port=30010", "--log-level=info", "--workers=2", "--timeout_keep_alive=120"]