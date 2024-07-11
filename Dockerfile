FROM python:3.10-slim

COPY . .
RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["gunicorn", "-w", "1", "garlight.run:app", "-b", "0.0.0.0:5000"]
