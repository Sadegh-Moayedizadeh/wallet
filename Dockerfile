FROM python:3.8-slim

ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH ./src

WORKDIR /code

COPY . /code/

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["python", "src/wallet/manage.py", "runserver", "0.0.0.0:8000"]
