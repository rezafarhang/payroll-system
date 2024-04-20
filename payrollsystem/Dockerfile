FROM python:3.9-slim-bullseye
RUN apt-get update
ENV PYTHONUNBUFFERED 1
RUN mkdir /app
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
#    && apt-get update \
#	&& apt-get install -y gdal-bin \
#	&& apt-get install -y python3-gdal
CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]