FROM python:3.10-slim

WORKDIR /app

COPY . .
RUN pip install -r requirements.txt

WORKDIR /app/garlight
EXPOSE 5000
ENV PYTHONPATH=/app
ENV LIV_ID=$LIV_ID
ENV BED_ID=$BED_ID

CMD ["gunicorn", "-w", "1", "run:create_app()", "-b", "0.0.0.0:5000"]
