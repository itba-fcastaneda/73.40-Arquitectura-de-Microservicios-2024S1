FROM python:3.11

RUN groupadd -g 999 python \
    && useradd -r -u 999 -g python python \
    && mkdir -p /usr/app \
    && chown python:python /usr/app

WORKDIR /usr/app

COPY --chown=python:python requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY --chown=python:python . .

USER 999

CMD ["nameko", "run", "--config", "config.yml", "airports"]