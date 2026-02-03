FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

RUN rm -rf /app/instance && mkdir -p /app/instance && chmod -R 777 /app/instance

EXPOSE 5000

RUN ls -l /app && ls -l /app/instance

RUN python -c "from app import initDB; initDB()"

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]