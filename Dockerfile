FROM python:3.12-alpine as builder

WORKDIR /app
COPY ./requirements.txt /app/requirements.txt

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple && \
  pip wheel --no-cache-dir --no-deps --wheel-dir /data/python_wheels -r requirements.txt

FROM python:3.12-alpine

LABEL maintainer="hoshinosuzumi"
LABEL org.opencontainers.image.source=https://github.com/HoshinoSuzumi/ham-set-fallback-api

WORKDIR /app

COPY --from=builder /data/python_wheels /data/python_wheels

RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple && \
  pip install --no-cache /data/python_wheels/* && \
  rm -rf /data/python_wheels

EXPOSE 80

COPY ./ /app/

CMD [ "uvicorn", "app:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80" ]