FROM python:3.8.6
WORKDIR /app
COPY . .

RUN pip install -U setuptools
RUN pip install -r requirements.txt
RUN python manage.py migrate

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]

EXPOSE 8000