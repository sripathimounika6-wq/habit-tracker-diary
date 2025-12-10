FROM python:3.11-slim

# Create a non-root user
RUN addgroup --system appgroup && adduser --system appuser --ingroup appgroup

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Change permissions so non-root can access
RUN chown -R appuser:appgroup /app

# Switch to non-root user
USER appuser

# Start your app
CMD ["python", "app/main.py"]
