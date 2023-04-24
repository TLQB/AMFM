ARG PYTHON_VERSION=3.7-slim-buster

FROM python:${PYTHON_VERSION}

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Convert file install unoconv 
RUN apt-get update && apt-get install -y unoconv
ENV PYTHONPATH ${PYTHONPATH}:/usr/lib/python3/dist-packages

RUN mkdir -p /code

WORKDIR /code

COPY requirements.txt /tmp/requirements.txt

RUN set -ex && \
    pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt && \
    rm -rf /root/.cache/

COPY . /code/

# RUN python manage.py collectstatic --noinput

EXPOSE 8000

# replace demo.wsgi with <project_name>.wsgi
CMD ["gunicorn", "--bind", ":8000", "--workers", "2", "mcapi.wsgi"]
