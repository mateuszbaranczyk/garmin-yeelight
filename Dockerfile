FROM python:3.10-slim

COPY . .
RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["flask", "--app", "yeelight-endpoints.py", "run", "--host", "0.0.0.0"]
