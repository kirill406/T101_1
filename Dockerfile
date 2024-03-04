FROM python:3.11-slim
MAINTAINER Kirill 2020-4-04-Bor <kirillmolinillo@gmail.com>
ENV REFRESHED_AT 2024-02-12
RUN set -e

COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app
WORKDIR /code/app
#CMD ["python3", "main.py", "&&", "pytest"]
CMD ["pytest"]
