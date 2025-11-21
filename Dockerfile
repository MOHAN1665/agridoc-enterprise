FROM python:3.10-slim

WORKDIR /app

# Copy requirements first
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code
COPY . .

# Expose port
EXPOSE 8080

# Run command
CMD ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]