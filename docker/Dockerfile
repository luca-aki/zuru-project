FROM python:3.7.3
MAINTAINER akshay@localhost

COPY ./ /

WORKDIR /

RUN pip install -r requirements.txt

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]