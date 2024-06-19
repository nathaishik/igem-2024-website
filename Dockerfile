FROM python:3.11
WORKDIR /usr/src/app
COPY requirements.txt .

ENV POSTGRES_ENGINE=django.db.backends.postgresql
ENV POSTGRES_DATABASE=postgres
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=postgres
ENV POSTGRES_HOST=db
ENV POSTGRES_PORT=5432

RUN pip install -r requirements.txt
COPY . .
RUN ["python", "manage.py", "collectstatic", "--noinput"]
RUN ["python", "manage.py", "makemigrations", "notebook"]
# RUN ["python", "manage.py", "migrate"]
EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "wiki.wsgi:application"]