# Stage 1
# FROM python:3-slim-buster AS builder
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8 as builder

WORKDIR /koyeb-nb2

RUN python3 -m venv venv
ENV VIRTUAL_ENV=/koyeb-nb2/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# COPY requirements.txt .
# RUN /koyeb-nb2/venv/bin/python3 -m pip install --upgrade pip && pip install -r requirements.txt

# try poetry
COPY poetry.lock pyproject.toml ./
RUN /koyeb-nb2/venv/bin/python3 -m pip install --upgrade pip \
&& pip install poetry \
&& poetry config virtualenvs.create false \
&& poetry install --no-dev --no-interaction --no-ansi

# Stage 2
# FROM python:3-slim-buster AS runner
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8 as runner

WORKDIR /koyeb-nb2

RUN apt-get update \
&& apt-get install -y supervisor

EXPOSE 8680

COPY --from=builder /koyeb-nb2/venv venv
COPY gocqhttp.conf /etc/supervisor/conf.d
# COPY nonebot.conf /etc/supervisor/conf.d
COPY . .

ENV VIRTUAL_ENV=/koyeb-nb2/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
# not necessary?
ENV APP=koyeb-nb2/bot.py

# CMD ["python", "-m" , "flask", "run", "--host=0.0.0.0"]
# CMD ["python3", "bot.py"]
# CMD ["uvicorn", "--port", "8680", "bot:app"]
# CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/supervisord.conf", "-n"]

# CMD ["sh", "-c", "/usr/bin/supervisord", "-c", "/etc/supervisor/supervisord.conf", ";", "uvicorn", "--port", "8680", "bot:app"]
CMD /usr/bin/supervisord -c /etc/supervisor/supervisord.conf ; uvicorn --host 0.0.0.0 --port 8680 bot:app
