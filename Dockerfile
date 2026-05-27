FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Run the app using gunicorn and bind to the port Hugging Face uses (7860)
CMD ["gunicorn", "-b", "0.0.0.0:7860", "app:app"]
