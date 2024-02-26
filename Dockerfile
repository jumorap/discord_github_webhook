FROM python:3.11.8-alpine3.18

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

EXPOSE $PORT

CMD ["python", "manage.py", "runserver", "0.0.0.0:5012"]
