FROM python:3.11
COPY . /usr/src/app
WORKDIR /usr/src/app
RUN pip install -r requirements.txt
RUN ["python", "manage.py", "migrate"]
EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "wiki.wsgi:application"]