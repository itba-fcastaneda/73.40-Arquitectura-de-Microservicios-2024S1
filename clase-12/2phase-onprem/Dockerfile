FROM python:3.11.5-bookworm

WORKDIR /root

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

ARG APP_FILE_PATH

COPY ${APP_FILE_PATH} app.py

CMD ["python", "app.py"]