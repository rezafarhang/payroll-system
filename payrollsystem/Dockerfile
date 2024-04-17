FROM python:3.9-slim-bullseye
RUN apt-get update
ENV PYTHONUNBUFFERED 1
RUN mkdir /app
WORKDIR /app
COPY payrollsystem /app
RUN pip install -r requirements.txt
CMD ["python", "manage.py", "runserver"]
