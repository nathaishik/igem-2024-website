FROM python:3.11
COPY . /usr/src/app
WORKDIR /usr/src/app
RUN pip install -r requirements.txt
RUN ["python", "manage.py", "migrate"]
CMD ["gunicorn", "--bind", "iisc-bengaluru-iisc-bengaluru-5dfbea53.koyeb.app:8000", "wiki.wsgi_prod:application"]