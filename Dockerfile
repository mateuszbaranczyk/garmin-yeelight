FROM python:3.10-slim

COPY . .
RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["gunicorn", "yeelight-endpoints:app", "-b", "0.0.0.0:5000"]
