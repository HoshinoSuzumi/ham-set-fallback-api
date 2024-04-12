FROM python:3.12

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

EXPOSE 80

COPY ./ /app/

CMD [ "uvicorn", "app:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80" ]