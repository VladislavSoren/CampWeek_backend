FROM python:3.11.6-slim-bullseye

WORKDIR /app

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

RUN chmod +x ./prestart.sh
ENTRYPOINT ["./prestart.sh"]

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
