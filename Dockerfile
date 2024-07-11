FROM python:3.10-slim

WORKDIR /app

COPY . .
RUN pip install -r requirements.txt

WORKDIR /app/garlight
EXPOSE 5000
ENV PYTHONPATH=/app

CMD ["gunicorn", "-w", "1", "run:create_app()", "-b", "0.0.0.0:5000"]
