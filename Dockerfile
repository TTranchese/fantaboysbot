FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Avvia come worker (long polling)
CMD ["python", "-m", "botcalcio.main"]
