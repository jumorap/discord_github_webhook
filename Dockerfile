FROM python:3.11.8-alpine3.18

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

WORKDIR /app

COPY . .

ARG PORT

ENV PORT=$PORT

RUN pip install -r requirements.txt

EXPOSE $PORT

CMD ["python", "app.py"]
