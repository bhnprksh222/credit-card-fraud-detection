# Use a lightweight Python image
FROM python:3.9-slim

# Set working directory inside the container
WORKDIR /app

# Copy dependencies and install
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt 


# Copy all backend files
COPY . ./

# Expose the FastAPI application port
EXPOSE 8000

# Set environment variables
ENV FASTAPI_ENV=development
ENV DATABASE_URL=postgres://postgres:postgres@db:5432/postgres
ENV FASTAPI_DEBUG=1

# Run FastAPI application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

