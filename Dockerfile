
# HomeValue AI - FastAPI Backend
# Python version compatible with the trained ML model

FROM python:3.12-slim

# Python runtime configuration
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Application directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy only the files needed by the backend
COPY api/ ./api/
COPY src/ ./src/
COPY models/ ./models/

# Default FastAPI port
EXPOSE 8000

# Start the API, supporting cloud-provided PORT values
CMD ["sh", "-c", "exec python -m uvicorn api.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
