FROM python:3.11
COPY . /usr/src/app
WORKDIR /usr/src/app
RUN pip install -r requirements.txt
ENV DEBUG=False
ENV SECRET_KEY=
RUN ["python", "manage.py", "migrate"]
RUN ["python", "manage.py", "collectstatic", "--noinput"]
EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "wiki.wsgi_prod:application"]