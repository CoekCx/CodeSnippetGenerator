FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Set the working directory to /app/src where the .env file is located
WORKDIR /app/src

CMD ["python", "-m", "main"] 